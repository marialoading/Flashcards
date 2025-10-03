<template>
  <div class="cute-dashboard">
    <Header :show-logout="true" />

    <div class="cute-panel">
      <h2 class="cute-subtitle">>>> CREATE NEW DECK</h2>
      <div class="cute-form">
        <input 
          v-model="newTitle" 
          placeholder="DECK TITLE..." 
          class="pixel-input"
          maxlength="50"
        />
        <Button 
          @click="createDeck" 
          :disabled="creating || !newTitle.trim()"
          variant="green"
        >
          {{ creating ? 'CREATING...' : 'CREATE DECK' }}
        </Button>
      </div>
      <p v-if="err" class="error-message">{{ err }}</p>
    </div>

    <div class="cute-section">
      <h2 class="cute-section-title">YOUR DECKS</h2>
      
      <StateDisplay 
        :loading="loading" 
        :isEmpty="decks.length === 0" 
        loadingText="LOADING DECKS..."
        icon="DECK"
        title="NO DECKS FOUND"
        message="CREATE YOUR FIRST DECK TO START LEARNING!"
      >
        <ul class="deck-list">
          <li v-for="d in decks" :key="d.id" class="deck-card" :data-progress="d.progress ? d.progress.mastery_percentage : 0">
          <div class="deck-info">
            <router-link :to="`/deck/${d.id}`" class="deck-title">
              {{ d.title }}
            </router-link>
            
            <!-- Progress Statistics -->
            <div v-if="d.progress" class="stats-display">
              <div class="stat-badges">
                <span class="stat-badge">{{ d.progress.total_cards }} CARDS</span>
                <span class="stat-badge">{{ d.progress.mastered_cards }} MASTERED</span>
              </div>
              
              <!-- Box Distribution -->
              <div v-if="d.progress.box_distribution" class="box-distribution">
                <span class="box-label">BOXES:</span>
                <div class="box-stats">
                  <span v-for="(count, box) in d.progress.box_distribution" :key="box" class="box-stat">
                    {{ String(box).replace('box_', '') }}: {{ count }}
                  </span>
                </div>
              </div>
              
              <!-- Progress Bar -->
              <div class="progress-section">
                <span class="progress-label">MASTERY:</span>
                <div class="progress-bar">
                  <div 
                    class="progress-fill" 
                    :style="{ width: `${d.progress.mastery_percentage}%` }"
                  >
                    <!-- Animated Character on Progress Bar -->
                    <div class="progress-character">
                      <img src="/src/assets/white_stand.png" class="character-stand white-char" alt="Character" />
                      <img src="/src/assets/white_run.png" class="character-run white-char" alt="Character Running" />
                      <img src="/src/assets/orange_stand.png" class="character-stand orange-char" alt="Orange Character" />
                      <img src="/src/assets/orange_run.png" class="character-run orange-char" alt="Orange Character Running" />
                    </div>
                  </div>
                </div>
                <span class="progress-value">{{ d.progress.mastery_percentage }}%</span>
              </div>
            </div>
            
            <div v-else-if="d.progress === null" class="loading-stats">
              LOADING STATS...
            </div>
          </div>
          
          <div class="deck-actions">
            <Button 
              @click="startStudy(d.id)" 
              variant="purple"
            >
              STUDY
            </Button>
            <Button 
              @click="router.push(`/deck/${d.id}`)" 
              variant="cyan"
            >
              EDIT
            </Button>
            <Button 
              @click="deleteDeck(d.id, d.title)" 
              variant="red"
            >
              DELETE
            </Button>
          </div>
        </li>
        </ul>
      </StateDisplay>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useAuth } from '../composables/useAuth'
import StateDisplay from '../components/StateDisplay.vue'
import Button from '../components/Button.vue'
import Header from '../components/Header.vue'

interface DeckProgress {
  total_cards: number
  mastered_cards: number
  studied_cards: number
  mastery_percentage: number
  study_percentage: number
  avg_box_level: number
  box_distribution?: { [key: string]: number }
}

interface Deck {
  id: number
  title: string
  progress?: DeckProgress | null
}

const { router, getApiBase, getApiHeaders, handleAuthError, getToken } = useAuth()
const decks = ref<Array<Deck>>([])
const newTitle = ref('')
const err = ref('')
const loading = ref(false)
const creating = ref(false)

async function loadDeckProgress(deckId: number): Promise<DeckProgress | null> {
  try {
    const res = await fetch(`${getApiBase()}/decks/${deckId}/progress`, {
      headers: getApiHeaders()
    })
    if (res.status === 401) {
      handleAuthError()
      return null
    }
    if (!res.ok) {
      return null
    }
    return await res.json()
  } catch (e) {
    console.error('Error loading deck progress:', e)
    return null
  }
}

async function load(): Promise<void> {
  err.value = ''
  loading.value = true
  try {
    const res = await fetch(`${getApiBase()}/decks`, {
      headers: getApiHeaders()
    })
    if (res.status === 401) {
      handleAuthError()
      return
    }
    if (!res.ok) {
      err.value = 'Konnte Stapel nicht laden'
      return
    }
    const data = await res.json()
    decks.value = (data.decks || []).map((deck: any) => ({
      ...deck,
      progress: null
    }))
    
    for (const deck of decks.value) {
      deck.progress = await loadDeckProgress(deck.id)
    }
  } catch (e) {
    err.value = 'Network error'
  } finally {
    loading.value = false
  }
}

async function createDeck(): Promise<void> {
  if (!newTitle.value.trim()) {
    return
  }
  creating.value = true
  try {
    const res = await fetch(`${getApiBase()}/decks`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', ...getApiHeaders() },
      body: JSON.stringify({ title: newTitle.value.trim() })
    })
    if (res.status === 401) {
      handleAuthError()
      return
    }
    if (!res.ok) {
      err.value = 'could not create deck'
      return
    }
    newTitle.value = ''
    await load()
  } catch (e) {
    err.value = 'Network error'
  } finally {
    creating.value = false
  }
}

function startStudy(deckId: number) {
  router.push(`/deck/${deckId}/study`)
}

async function deleteDeck(deckId: number, deckTitle: string): Promise<void> {
  const confirmed = confirm(`Are you sure you want to delete "${deckTitle}"?\n\nThis action cannot be undone and will delete all cards in this deck.`)
  if (!confirmed) {
    return
  }
  
  try {
    const res = await fetch(`${getApiBase()}/decks/${deckId}`, {
      method: 'DELETE',
      headers: getApiHeaders()
    })
    if (res.status === 401) {
      handleAuthError()
      return
    }
    if (!res.ok) {
      err.value = 'could not delete deck'
      return
    }

    await load()
  } catch (e) {
    err.value = 'Network error'
  }
}

onMounted(() => {
  const { router, getToken } = useAuth()
  if (!getToken()) {
    router.push('/login')
    return
  }
  load()
})
</script>

<style scoped>

.cute-dashboard {
  min-height: 100vh;
  background: linear-gradient(135deg, #f8e6ff 0%, #e6f3ff 50%, #fff0e6 100%);
  padding: 20px;
  font-family: 'Fredoka One', sans-serif;
  max-width: 1200px;
  margin: 0 auto;
}

.cute-panel {
  background: rgba(255, 255, 255, 0.9);
  border-radius: 15px;
  padding: 30px;
  margin-bottom: 30px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
  border: 3px solid #dda0dd;
}

.cute-subtitle {
  color: #efadff;
  font-size: 1.5rem;
  margin-bottom: 20px;
  text-align: center;
  font-weight: 600;
  text-shadow: 1px 1px 0 rgba(255,255,255,0.8);
  -webkit-text-stroke: 0.1px #000;
}

.cute-form {
  display: flex;
  gap: 15px;
  align-items: center;
  flex-wrap: wrap;
  justify-content: center;
}

.error-message {
  color: #d63384;
  text-align: center;
  margin-top: 15px;
  font-weight: bold;
  font-size: 1.1rem;
  background: linear-gradient(145deg, #ffcccb, #ff6b6b);
  border: 3px solid #8b0000;
  padding: 15px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}


.cute-section {
  margin-top: 40px;
}

.cute-section-title {
  font-size: 2rem;
  color: #f4a9ff;
  text-align: center;
  margin-bottom: 30px;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
  font-weight: 600;
  -webkit-text-stroke: 0.1px #000;
}


.deck-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 25px;
}

.deck-card {
  background: linear-gradient(145deg, #fefefe, #fff8ff);
  border-radius: 20px;
  border: 2px solid #dda0dd;
  padding: 25px;
  box-shadow: 
    0 0 0 2px rgba(221,160,221,0.3),
    0 6px 0 #dda0dd,
    0 10px 25px rgba(221,160,221,0.2);
  transition: all 0.3s ease;
  position: relative;
  overflow: visible;
  display: flex;
  flex-direction: column;
  min-height: 280px;
}

.deck-card::before {
  content: '';
  position: absolute;
  top: -2px;
  left: -2px;
  right: -2px;
  bottom: -2px;
  background: linear-gradient(45deg, #ff9dff, #b8f2ff, #ffc8dd, #fff2b8);
  background-size: 300% 300%;
  animation: cardGlow 6s ease infinite;
  z-index: -1;
  opacity: 0.4;
  border-radius: 20px;
}

@keyframes cardGlow {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}

.deck-card:hover {
  transform: translateY(-8px);
  box-shadow: 
    0 0 0 3px #ffd700,
    0 12px 0 #000,
    0 16px 25px rgba(0,0,0,0.4);
}


.deck-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  margin-bottom: 20px;
}

.deck-title {
  display: block;
  font-size: 1.4rem;
  color: #eac1ff;
  text-decoration: none;
  font-weight: 600;
  margin-bottom: 20px;
  text-align: center;
  text-shadow: 1px 1px 0 rgba(255,255,255,0.5);
  transition: all 0.3s ease;
  -webkit-text-stroke: 0.1px #000;
}

.deck-title:hover {
  color: #2d5f3f;
  text-shadow: 
    2px 2px 0 #000,
    -1px -1px 0 #000,
    1px -1px 0 #000,
    -1px 1px 0 #000,
    1px 1px 0 #000;
  transform: scale(1.05);
}


.stats-display {
  margin-top: 15px;
}

.stat-badges {
  display: flex;
  gap: 8px;
  margin-bottom: 15px;
  flex-wrap: wrap;
  justify-content: center;
}

.stat-badge {
  background: linear-gradient(145deg, #ffe4f2, #ffeeff);
  color: #8b5a8c;
  padding: 6px 12px;
  border-radius: 15px;
  font-size: 0.8rem;
  font-weight: 600;
  border: 2px solid #dda0dd;
  text-shadow: 1px 1px 0 rgba(255,255,255,0.8);
  box-shadow: 0 2px 0 #dda0dd, 0 4px 8px rgba(221,160,221,0.3);
}

.box-distribution {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 15px;
  align-items: center;
}

.box-label {
  font-size: 0.85rem;
  font-weight: 600;
  color: #d78ad9;
  text-shadow: 1px 1px 0 rgba(255,255,255,0.8);
}

.box-stats {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
  justify-content: center;
}

.box-stat {
  background: linear-gradient(145deg, #fff2e6, #ffe8cc);
  color: #b8860b;
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
  border: 2px solid #daa520;
  text-shadow: 1px 1px 0 rgba(255,255,255,0.6);
  box-shadow: 0 1px 0 #daa520, 0 2px 4px rgba(218,165,32,0.2);
}

.progress-section {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-direction: column;
}

.progress-label, .progress-value {
  font-size: 0.9rem;
  font-weight: 600;
  color: #664466;
  text-align: center;
  text-shadow: 1px 1px 0 rgba(255,255,255,0.5);
}

.progress-bar {
  width: 100%;
  height: 25px;
  background: rgba(221,160,221,0.2);
  border: 2px solid #dda0dd;
  border-radius: 15px;
  box-shadow: inset 0 2px 4px rgba(221,160,221,0.3);
  position: relative;
  overflow: visible;
  margin: 8px 0;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #ff9dff, #b8f2ff);
  border-radius: 13px;
  box-shadow: 0 0 10px rgba(255,157,255,0.5);
  position: relative;
  transition: width 0.3s ease;
}

.loading-stats {
  font-size: 0.9rem;
  font-weight: 600;
  color: #9370db;
  margin-top: 15px;
  text-align: center;
  text-shadow: 1px 1px 0 rgba(255,255,255,0.5);
}

.deck-actions {
  display: flex;
  gap: 12px;
  margin-top: auto;
  padding-top: 20px;
  justify-content: center;
  flex-wrap: wrap;
}


.progress-character {
  position: absolute;
  right: -20px;
  top: 50%;
  transform: translateY(-50%);
  width: 48px;
  height: 48px;
  z-index: 2;
  overflow: visible;
}

.character-stand,
.character-run {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  image-rendering: pixelated;
  image-rendering: -moz-crisp-edges;
  image-rendering: crisp-edges;
  transition: opacity 0.2s ease;
}

.character-stand.white-char {
  opacity: 1;
}

.character-stand.orange-char {
  opacity: 0;
}

.character-run {
  opacity: 0;
}


.deck-card:nth-child(even) .character-stand.white-char {
  opacity: 0;
}

.deck-card:nth-child(even) .character-stand.orange-char {
  opacity: 1;
}

.deck-card[data-progress="0"]:hover .progress-character {
  animation: runInPlace 1s infinite ease-in-out;
}

.deck-card:hover .progress-character {
  animation: runAcrossBar 4s infinite ease-in-out;
}

.deck-card:hover .character-stand.white-char {
  opacity: 1;
  animation: spriteAlternate 0.6s infinite;
}

.deck-card:hover .character-run.white-char {
  opacity: 0;
  animation: spriteAlternate 0.6s infinite;
  animation-delay: 0.3s;
}

.deck-card:hover .character-stand.orange-char {
  opacity: 0;
}

.deck-card:hover .character-run.orange-char {
  opacity: 0;
}

.deck-card:nth-child(even):hover .character-stand.white-char {
  opacity: 0;
}

.deck-card:nth-child(even):hover .character-run.white-char {
  opacity: 0;
}

.deck-card:nth-child(even):hover .character-stand.orange-char {
  opacity: 1;
  animation: spriteAlternate 0.6s infinite;
}

.deck-card:nth-child(even):hover .character-run.orange-char {
  opacity: 0;
  animation: spriteAlternate 0.6s infinite;
  animation-delay: 0.3s;
}

@keyframes runInPlace {
  0% {
    right: -20px;
    transform: translateY(-50%) scaleX(1);
  }
  100% {
    right: -20px;
    transform: translateY(-50%) scaleX(1);
  }
}

@keyframes runAcrossBar {
  0% {
    right: -20px;
    transform: translateY(-50%) scaleX(-1);
  }
  25% {
    right: 50%;
    transform: translateY(-50%) scaleX(-1);
  }
  49% {
    right: calc(100% - 48px);
    transform: translateY(-50%) scaleX(-1);
  }
  51% {
    right: calc(100% - 48px);
    transform: translateY(-50%) scaleX(1);
  }
  75% {
    right: 50%;
    transform: translateY(-50%) scaleX(1);
  }
  99% {
    right: -20px;
    transform: translateY(-50%) scaleX(1);
  }
  100% {
    right: -20px;
    transform: translateY(-50%) scaleX(-1);
  }
}

@keyframes spriteAlternate {
  0% {
    opacity: 1;
    filter: brightness(1);
  }
  50% {
    opacity: 0;
    filter: brightness(1.2);
  }
  100% {
    opacity: 1;
    filter: brightness(1);
  }
}

/* Responsive Design */
@media (max-width: 768px) {
  .cute-dashboard {
    padding: 15px;
  }

  .cute-header {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    padding: 20px;
    gap: 10px;
  }

  .cute-title {
    position: static;
    transform: none;
    font-size: 2rem;
    pointer-events: auto;
  }

  .cute-form {
    flex-direction: column;
    align-items: stretch;
  }

  .deck-list {
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 20px;
  }

  .deck-card {
    min-height: 250px;
    padding: 20px;
  }

  .deck-actions {
    flex-direction: column;
    gap: 10px;
  }

  .stat-badges {
    gap: 6px;
    flex-direction: column;
    align-items: center;
  }

  .cute-section-title {
    font-size: 1.7rem;
  }

  .cute-subtitle {
    font-size: 1.3rem;
  }

  .progress-character {
    width: 40px;
    height: 40px;
    right: 3px;
  }

  .progress-bar {
    height: 22px;
  }
}

@media (max-width: 480px) {
  .deck-list {
    grid-template-columns: 1fr;
  }
  
  .deck-card {
    min-height: 300px;
    padding: 20px;
  }
  
  .deck-title {
    font-size: 1.2rem;
  }
  
  .progress-character {
    width: 35px;
    height: 35px;
    right: 2px;
  }
  
  .progress-bar {
    height: 20px;
  }
}
</style>
