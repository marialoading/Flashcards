<template>
  <div class="cute-deck">
    <Header :page-title="title || 'Loading...'">
      <template #page-actions>
        <Button 
          @click="startStudy" 
          variant="purple"
        >
          Study Mode
        </Button>
        <BackButton to="/" text="Back" />
      </template>
    </Header>

    <div class="add-card-panel">
      <h2 class="panel-subtitle">Create New Card</h2>
      <div class="add-card-form">
        <div class="input-group">
          <label class="form-label">Front Side</label>
          <input 
            v-model="front" 
            placeholder="Enter question or prompt..." 
            class="form-input"
            maxlength="500"
          />
        </div>
        <div class="input-group">
          <label class="form-label">Back Side</label>
          <input 
            v-model="back" 
            placeholder="Enter answer or explanation..." 
            class="form-input"
            maxlength="500"
          />
        </div>
        <Button 
          @click="addCard" 
          :disabled="adding || !front.trim() || !back.trim()"
          variant="green"
        >
          {{ adding ? 'Adding...' : 'Add Card' }}
        </Button>
      </div>
      <div v-if="err" class="error-message">{{ err }}</div>
    </div>

    <div class="cards-section">
      <h2 class="section-title">
        Cards in Deck ({{ cards.length }})
      </h2>
      
      <StateDisplay 
        :loading="loading" 
        :isEmpty="cards.length === 0" 
        loadingText="LOADING CARDS..."
        icon="📚"
        title="NO CARDS FOUND"
        message="CREATE YOUR FIRST CARD TO START LEARNING!"
      >
        <ul class="cards-list">
          <li v-for="c in cards" :key="c.id" class="card-item">
            <button class="delete-btn" @click="deleteCard(c.id)" title="Karte löschen">×</button>
            <div class="card-content">
              <div class="card-side front">
                <span class="side-label">Front</span>
                <span class="side-text">{{ c.front }}</span>
              </div>
              <div class="card-divider"></div>
              <div class="card-side back">
                <span class="side-label">Back</span>
                <span class="side-text">{{ c.back }}</span>
              </div>
            </div>
          </li>
        </ul>
      </StateDisplay>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useAuth } from '../composables/useAuth'
import StateDisplay from '../components/StateDisplay.vue'
import BackButton from '../components/BackButton.vue'
import Button from '../components/Button.vue'
import Header from '../components/Header.vue'

const route = useRoute()
const { router, getApiBase, getApiHeaders, handleAuthError, getToken } = useAuth()
const id = Number(route.params.id)
const title = ref<string>('')
const cards = ref<Array<{ id: number; front: string; back: string }>>([])
const front = ref<string>('')
const back = ref<string>('')
const err = ref<string>('')
const loading = ref<boolean>(false)
const adding = ref<boolean>(false)

async function load(): Promise<void> {
  err.value = ''
  loading.value = true
  try {
    const res = await fetch(`${getApiBase()}/decks/${id}/cards`, {
      headers: getApiHeaders()
    })
    if (res.status === 401) {
      handleAuthError()
      return
    }
    if (res.status === 404) {
      err.value = 'deck not found'
      return
    }
    if (!res.ok) {
      err.value = 'card not found'
      return
    }
    const data = await res.json()
    cards.value = data.cards || []

    // title
    const dres = await fetch(`${getApiBase()}/decks`, { headers: getApiHeaders() })
    if (dres.ok) {
      const dd = await dres.json()
      const found = (dd.decks || []).find((x: any) => x.id === id)
      if (found) {
        title.value = found.title
      }
    }
  } catch (e) {
    err.value = 'Netzwerkfehler'
  } finally {
    loading.value = false
  }
}

async function addCard(): Promise<void> {
  if (!front.value.trim() || !back.value.trim()) {
    return
  }
  adding.value = true
  try {
    const res = await fetch(`${getApiBase()}/decks/${id}/cards`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', ...getApiHeaders() },
      body: JSON.stringify({ front: front.value.trim(), back: back.value.trim() })
    })
    if (res.status === 401) {
      handleAuthError()
      return
    }
    if (res.status === 404) {
      err.value = 'deck not found'
      return
    }
    if (!res.ok) {
      err.value = 'card not found'
      return
    }
    front.value = ''
    back.value = ''
    await load()
  } catch (e) {
    err.value = 'Netzwerkfehler'
  } finally {
    adding.value = false
  }
}

async function deleteCard(cardId: number): Promise<void> {
  if (!confirm('are you sure to delete it?')) return
  try {
    const res = await fetch(`${getApiBase()}/cards/${cardId}`, {
      method: 'DELETE',
      headers: getApiHeaders()
    })
    if (res.status === 401) {
      handleAuthError()
      return
    }
    if (!res.ok) {
      err.value = 'could not delete card'
      return
    }
    await load()
  } catch (e) {
    err.value = 'Network error'
  }
}

function startStudy(): void {
  router.push(`/deck/${id}/study`)
}

onMounted(() => {
  if (!getToken()) {
    router.push('/login')
    return
  }
  load()
})
</script>

<style scoped>
.cute-deck {
  min-height: 100vh;
  background: linear-gradient(135deg, #f8e6ff 0%, #e6f3ff 50%, #fff0e6 100%);
  padding: 20px;
  font-family: 'Fredoka One', sans-serif;
  max-width: 1000px;
  margin: 0 auto;
}


.add-card-panel {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 20px;
  border: 3px solid #dda0dd;
  padding: 30px;
  margin-bottom: 30px;
  box-shadow: 
    0 0 0 2px rgba(221,160,221,0.3),
    0 8px 16px rgba(0,0,0,0.1),
    inset 0 1px 0 rgba(255,255,255,0.9);
  position: relative;
}

.add-card-panel::before {
  content: '';
  position: absolute;
  top: -3px;
  left: -3px;
  right: -3px;
  bottom: -3px;
  background: linear-gradient(45deg, #ff9dff, #b8f2ff, #ffc8dd, #fff2b8);
  background-size: 300% 300%;
  animation: panelGlow 8s ease infinite;
  z-index: -1;
  opacity: 0.4;
  border-radius: 20px;
}

@keyframes panelGlow {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}

.panel-subtitle {
  color: #e57dff;
  font-size: 1.4rem;
  margin-bottom: 25px;
  text-align: center;
  font-weight: 600;
  text-shadow: 1px 1px 0 rgba(255,255,255,0.8);
  -webkit-text-stroke: 0.1px #000;
}

.add-card-form {
  display: grid;
  gap: 20px;
  max-width: 600px;
  margin: 0 auto;
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
  text-align: center;
}

.form-label {
  font-size: 1rem;
  font-weight: 600;
  color: #8b4a9c;
  text-shadow: 1px 1px 0 rgba(255,255,255,0.8);
}

.form-input {
  width: 100%;
  padding: 15px 20px;
  font-family: 'Fredoka One', sans-serif;
  font-size: 0.95rem;
  font-weight: 500;
  background: rgba(255, 255, 255, 0.9);
  border: 3px solid #dda0dd;
  border-radius: 15px;
  color: #664466;
  text-align: center;
  transition: all 0.3s ease;
  box-shadow: 
    inset 0 2px 4px rgba(221,160,221,0.1),
    0 2px 8px rgba(0,0,0,0.05);
}

.form-input:focus {
  outline: none;
  border-color: #ff9dff;
  background: rgba(255, 255, 255, 1);
  box-shadow: 
    inset 0 2px 4px rgba(221,160,221,0.1),
    0 0 0 3px rgba(255, 157, 255, 0.3),
    0 8px 25px rgba(255, 157, 255, 0.2);
  transform: translateY(-2px);
}

.form-input::placeholder {
  color: #b8a8b8;
  font-style: italic;
}

.submit-button {
  width: 100%;
  max-width: 300px;
  margin: 10px auto 0;
  padding: 16px 25px;
  font-family: 'Fredoka One', sans-serif;
  font-size: 1rem;
  font-weight: 600;
  background: linear-gradient(135deg, #ff9dff, #dda0dd);
  border: 3px solid #ff9dff;
  border-radius: 20px;
  color: #fff;
  text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
  cursor: pointer;
  transition: all 0.3s ease;
  text-transform: capitalize;
  letter-spacing: 1px;
  box-shadow: 
    0 6px 0 #cc7acc,
    0 12px 20px rgba(221,160,221,0.3);
}

.submit-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 
    0 8px 0 #cc7acc,
    0 16px 25px rgba(221,160,221,0.4);
  background: linear-gradient(135deg, #ffb3ff, #e6b3e6);
}

.submit-button:active:not(:disabled) {
  transform: translateY(2px);
  box-shadow: 
    0 3px 0 #cc7acc,
    0 6px 15px rgba(221,160,221,0.3);
}

.submit-button:disabled {
  background: linear-gradient(135deg, #ccc, #999);
  border-color: #ccc;
  cursor: not-allowed;
  transform: none;
  box-shadow: 
    0 3px 0 #999,
    0 6px 12px rgba(0,0,0,0.1);
}

.error-message {
  background: linear-gradient(135deg, #ffcccb, #ff9999);
  border: 3px solid #ff6b6b;
  border-radius: 15px;
  color: #8b0000;
  padding: 15px 20px;
  margin-top: 20px;
  font-weight: 600;
  text-align: center;
  font-size: 0.9rem;
  box-shadow: 
    0 4px 0 #cc4444,
    0 8px 20px rgba(255,107,107,0.2);
  text-shadow: 1px 1px 0 rgba(255,255,255,0.3);
}


.cards-section {
  margin-top: 40px;
}

.section-title {
  font-size: 1.8rem;
  color: #ea96ff;
  text-align: center;
  margin-bottom: 30px;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
  font-weight: 600;
  -webkit-text-stroke: 0.1px #000;
}

.cards-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: grid;
  gap: 20px;
}

.card-item {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 20px;
  border: 3px solid #dda0dd;
  padding: 25px;
  box-shadow: 
    0 0 0 2px rgba(221,160,221,0.3),
    0 8px 20px rgba(0,0,0,0.1),
    inset 0 1px 0 rgba(255,255,255,0.9);
  transition: all 0.3s ease;
  position: relative;
}

.delete-btn {
  position: absolute;
  top: 15px;
  right: 15px;
  background: linear-gradient(135deg, #ff9ddd, #ff6bb3);
  color: white;
  border: none;
  border-radius: 50%;
  width: 24px;
  height: 24px;
  font-size: 16px;
  font-family: 'Fredoka One', sans-serif;
  font-weight: bold;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 6px rgba(255, 107, 179, 0.3);
  transition: all 0.2s ease;
  z-index: 10;
}

.delete-btn:hover {
  background: linear-gradient(135deg, #ff6bb3, #ff4d9d);
  transform: scale(1.1);
  box-shadow: 0 3px 8px rgba(255, 107, 179, 0.4);
}

.card-item::before {
  content: '';
  position: absolute;
  top: -3px;
  left: -3px;
  right: -3px;
  bottom: -3px;
  background: linear-gradient(45deg, #ff9dff, #b8f2ff, #ffc8dd, #fff2b8);
  background-size: 300% 300%;
  animation: cardGlow 8s ease infinite;
  z-index: -1;
  opacity: 0.3;
  border-radius: 20px;
}

@keyframes cardGlow {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}

.card-item:hover {
  transform: translateY(-5px);
  box-shadow: 
    0 0 0 3px #ffd700,
    0 12px 25px rgba(255,215,0,0.3),
    0 16px 35px rgba(0,0,0,0.2);
}

.card-content {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  gap: 25px;
  align-items: center;
}

.card-side {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 20px;
  background: rgba(255,255,255,0.6);
  border: 2px solid #dda0dd;
  border-radius: 15px;
  transition: all 0.3s ease;
}

.card-side.front {
  background: rgba(255,200,221,0.3);
  border-color: #ff9dff;
}

.card-side.back {
  background: rgba(184,242,255,0.3);
  border-color: #b8f2ff;
}

.card-side:hover {
  transform: scale(1.02);
  box-shadow: 0 4px 15px rgba(221,160,221,0.2);
}

.side-label {
  font-size: 0.85rem;
  font-weight: 600;
  color: #8b5a8c;
  text-shadow: 1px 1px 0 rgba(255,255,255,0.8);
  letter-spacing: 0.5px;
  text-transform: uppercase;
  text-align: center;
  -webkit-text-stroke: 0.1px #000;
}

.side-text {
  font-size: 1rem;
  color: #664466;
  line-height: 1.4;
  text-align: center;
  word-wrap: break-word;
}

.card-divider {
  color: #dda0dd;
  font-size: 1.5rem;
  text-align: center;
  text-shadow: 
    1px 1px 0 rgba(255,255,255,0.8),
    0 0 8px rgba(221,160,221,0.5);
  animation: dividerFloat 4s ease-in-out infinite;
}

@keyframes dividerFloat {
  0%, 100% { 
    transform: translateY(0px) rotate(0deg);
    opacity: 0.8;
  }
  50% { 
    transform: translateY(-3px) rotate(5deg);
    opacity: 1;
  }
}

/* Responsive Design */
@media (max-width: 768px) {
  .cute-deck {
    padding: 15px;
  }
  
  .add-card-panel {
    padding: 25px 20px;
  }
  
  .card-content {
    grid-template-columns: 1fr;
    gap: 15px;
    text-align: center;
  }
  
  .card-divider {
    transform: rotate(90deg);
    font-size: 1.2rem;
  }
  
  .section-title {
    font-size: 1.5rem;
  }
  
  .panel-subtitle {
    font-size: 1.2rem;
  }
}

@media (max-width: 480px) {
  .cute-deck {
    padding: 10px;
  }
  
  .card-item {
    padding: 20px 15px;
  }
  
  .card-side {
    padding: 15px;
  }
  
  .form-input {
    padding: 12px 15px;
    font-size: 0.9rem;
  }
  
  .submit-button {
    padding: 14px 20px;
    font-size: 0.9rem;
  }
}
</style>
