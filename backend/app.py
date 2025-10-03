import jwt
import hashlib
import psycopg2
from datetime import datetime, timedelta
from functools import wraps
from contextlib import contextmanager
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'dev-secret-key-flashcards'

def get_db_connection():
    return psycopg2.connect(
        host='db',  
        port=5432,
        database='flashcards',
        user='postgres',
        password='secret'
    )

@contextmanager
def db():
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        yield cur
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()

def check_deck_owner(deck_id, user_id):
    with db() as cur:
        cur.execute('SELECT 1 FROM decks WHERE id=%s AND user_id=%s', (deck_id, user_id))
        if not cur.fetchone():
            return jsonify({'error': 'Deck not found or access denied'}), 404
    return None

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def generate_token(user_id):
    return jwt.encode({'user_id': user_id, 'exp': datetime.utcnow() + timedelta(days=7)}, 
                     app.config['SECRET_KEY'], algorithm='HS256')

def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not token:
            return jsonify({'error': 'No token provided'}), 401
        try:
            request.user_id = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])['user_id']
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return jsonify({'error': 'Invalid token'}), 401
        return f(*args, **kwargs)
    return decorated

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json or {}
    username, email, password = data.get('username', '').strip(), data.get('email', '').strip(), data.get('password', '')
    
    if not all([username, email, password]):
        return jsonify({'error': 'Username, email, and password are required'}), 400
    
    try:
        with db() as cur:
            cur.execute('SELECT 1 FROM users WHERE username=%s OR email=%s', (username, email))
            if cur.fetchone():
                return jsonify({'error': 'Username or email already exists'}), 400
            
            cur.execute('INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s) RETURNING id', 
                       (username, email, hash_password(password)))
            user_id = cur.fetchone()[0]
            
        return jsonify({'token': generate_token(user_id), 'user_id': user_id})
    except Exception as e:
        return jsonify({'error': f'Registration failed: {str(e)}'}), 500

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json or {}
    username, password = data.get('username', '').strip(), data.get('password', '')
    
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400
    
    try:
        with db() as cur:
            cur.execute('SELECT id FROM users WHERE username=%s AND password_hash=%s', 
                       (username, hash_password(password)))
            user = cur.fetchone()
            
        if not user:
            return jsonify({'error': 'Invalid credentials'}), 401
        
        return jsonify({'token': generate_token(user[0]), 'user_id': user[0]})
    except Exception:
        return jsonify({'error': 'Login failed'}), 500

@app.route('/api/decks', methods=['POST'])
@auth_required
def create_deck():
    title = (request.json or {}).get('title')
    if not title:
        return jsonify({'error': 'title required'}), 400
    with db() as cur:
        cur.execute('INSERT INTO decks (user_id, title) VALUES (%s, %s) RETURNING id', (request.user_id, title))
        return jsonify({'id': cur.fetchone()[0], 'title': title})

@app.route('/api/decks', methods=['GET'])
@auth_required
def list_decks():
    with db() as cur:
        cur.execute('SELECT id, title FROM decks WHERE user_id=%s', (request.user_id,))
        return jsonify({'decks': [{'id': r[0], 'title': r[1]} for r in cur.fetchall()]})

@app.route('/api/decks/<int:deck_id>', methods=['DELETE'])
@auth_required
def delete_deck(deck_id):
    error = check_deck_owner(deck_id, request.user_id)
    if error:
        return error
    with db() as cur:
        cur.execute('DELETE FROM cards WHERE deck_id=%s', (deck_id,))
        cur.execute('DELETE FROM decks WHERE id=%s', (deck_id,))
    return jsonify({'message': 'Deck deleted successfully'})

@app.route('/api/decks/<int:deck_id>/cards', methods=['POST'])
@auth_required
def add_card(deck_id):
    error = check_deck_owner(deck_id, request.user_id)
    if error:
        return error
    data = request.json or {}
    front, back = data.get('front'), data.get('back')
    if not front or not back:
        return jsonify({'error': 'front and back required'}), 400
    with db() as cur:
        cur.execute('INSERT INTO cards (deck_id, front, back) VALUES (%s, %s, %s) RETURNING id', (deck_id, front, back))
        return jsonify({'id': cur.fetchone()[0], 'front': front, 'back': back})

@app.route('/api/decks/<int:deck_id>/cards', methods=['GET'])
@auth_required
def list_cards(deck_id):
    error = check_deck_owner(deck_id, request.user_id)
    if error:
        return error
    with db() as cur:
        cur.execute('SELECT id, front, back FROM cards WHERE deck_id=%s', (deck_id,))
        return jsonify({'cards': [{'id': r[0], 'front': r[1], 'back': r[2]} for r in cur.fetchall()]})

@app.route('/api/decks/<int:deck_id>/study/next', methods=['GET'])
@auth_required
def get_next_card_for_study(deck_id):
    error = check_deck_owner(deck_id, request.user_id)
    if error:
        return error
    
    try:
        with db() as cur:
            cur.execute("""
                SELECT c.id, c.front, c.back, COALESCE(cp.box_level, 1) as box_level
                FROM cards c
                LEFT JOIN card_progress cp ON c.id = cp.card_id AND cp.user_id = %s
                WHERE c.deck_id = %s AND (cp.next_review IS NULL OR cp.next_review <= NOW())
                ORDER BY CASE WHEN cp.next_review IS NULL THEN 0 ELSE 1 END, cp.next_review, RANDOM()
                LIMIT 1
            """, (request.user_id, deck_id))
            
            card = cur.fetchone()
            if not card:
                return jsonify({'card': None, 'message': 'Keine Karten zum Lernen verfügbar'})
            
            return jsonify({'card': {'id': card[0], 'front': card[1], 'back': card[2], 'box_level': card[3]}})
    except Exception as e:
        return jsonify({'error': 'Failed to get next card'}), 500

@app.route('/api/cards/<int:card_id>/review', methods=['POST'])
@auth_required
def review_card(card_id):
    correct = (request.json or {}).get('correct', False)
    
    try:
        with db() as cur:
           
            cur.execute('SELECT 1 FROM cards c JOIN decks d ON c.deck_id = d.id WHERE c.id = %s AND d.user_id = %s', 
                       (card_id, request.user_id))
            if not cur.fetchone():
                return jsonify({'error': 'Card not found or not owned'}), 404
            
           
            cur.execute('SELECT box_level, correct_count, incorrect_count FROM card_progress WHERE card_id = %s AND user_id = %s', 
                       (card_id, request.user_id))
            progress = cur.fetchone()
            
            box_level, correct_count, incorrect_count = progress or (1, 0, 0)

            new_box_level = min(box_level + 1, 5) if correct else 1
            correct_count += correct
            incorrect_count += not correct
            interval_days = {1: 1, 2: 3, 3: 7, 4: 14, 5: 30}[new_box_level]
            
            cur.execute("""
                INSERT INTO card_progress (card_id, user_id, box_level, last_reviewed, next_review, correct_count, incorrect_count)
                VALUES (%s, %s, %s, NOW(), NOW() + INTERVAL '%s days', %s, %s)
                ON CONFLICT (card_id, user_id) DO UPDATE SET 
                    box_level = EXCLUDED.box_level, last_reviewed = EXCLUDED.last_reviewed,
                    next_review = EXCLUDED.next_review, correct_count = EXCLUDED.correct_count,
                    incorrect_count = EXCLUDED.incorrect_count
            """, (card_id, request.user_id, new_box_level, interval_days, correct_count, incorrect_count))
            
            return jsonify({'success': True, 'new_box_level': new_box_level, 'next_review_days': interval_days})
    except Exception:
        return jsonify({'error': 'Failed to review card'}), 500

@app.route('/api/decks/<int:deck_id>/progress', methods=['GET'])
@auth_required
def get_deck_progress(deck_id):
    error = check_deck_owner(deck_id, request.user_id)
    if error:
        return error
    
    try:
        with db() as cur:
            cur.execute("""
                SELECT COUNT(c.id) as total, 
                       COUNT(CASE WHEN cp.box_level >= 5 THEN 1 END) as mastered,
                       COUNT(CASE WHEN cp.box_level IS NOT NULL THEN 1 END) as studied
                FROM cards c LEFT JOIN card_progress cp ON c.id = cp.card_id AND cp.user_id = %s
                WHERE c.deck_id = %s
            """, (request.user_id, deck_id))
            
            total, mastered, studied = cur.fetchone()
            total = total or 0
            
            cur.execute("""
                SELECT COALESCE(cp.box_level, 1) as box_level, COUNT(*) as count
                FROM cards c LEFT JOIN card_progress cp ON c.id = cp.card_id AND cp.user_id = %s
                WHERE c.deck_id = %s
                GROUP BY COALESCE(cp.box_level, 1)
                ORDER BY box_level
            """, (request.user_id, deck_id))
            
            box_distribution = {}
            for box_level, count in cur.fetchall():
                box_distribution[f'box_{int(box_level)}'] = count
            
            return jsonify({
                'total_cards': total,
                'mastered_cards': mastered or 0,
                'studied_cards': studied or 0,
                'mastery_percentage': round((mastered or 0) / total * 100, 1) if total else 0,
                'study_percentage': round((studied or 0) / total * 100, 1) if total else 0,
                'box_distribution': box_distribution
            })
    except Exception:
        return jsonify({'error': 'Failed to get deck progress'}), 500

@app.route('/api/cards/<int:card_id>', methods=['DELETE'])
@auth_required
def delete_card(card_id):
    try:
        with db() as cur:
            cur.execute("""
                SELECT d.user_id 
                FROM cards c 
                JOIN decks d ON c.deck_id = d.id 
                WHERE c.id = %s
            """, (card_id,))
            
            result = cur.fetchone()
            if not result:
                return jsonify({'error': 'Card not found'}), 404
            
            if result[0] != request.user_id:
                return jsonify({'error': 'Access denied'}), 403
            
            cur.execute('DELETE FROM cards WHERE id = %s', (card_id,))
            
            return jsonify({'message': 'Card deleted successfully'})
    except Exception:
        return jsonify({'error': 'Failed to delete card'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
