<template>
  <div class="study-container cute-study-container">
    <Header :page-title="`Study: ${deckTitle || 'Loading...'}`">
      <template #page-actions>
        <BackButton :to="`/deck/${deckId}`" text="Back to Deck" />
      </template>
    </Header>
    
    <div v-if="currentCard" class="card-container cute-card-container">
      <div v-if="!showAnswer" class="card-side cute-card-side">
        <div class="card-header cute-card-header">
          <h3 class="pixel-header h3 cute-question-title">Question</h3>
          <span class="box-level cute-box-level">Box {{ currentCard.box_level }}</span>
        </div>
        <div class="card-content cute-card-content">{{ currentCard.front }}</div>
        <div class="card-actions cute-card-actions">
          <Button @click="showAnswer = true" variant="yellow" class="cute-show-button">Show Answer</Button>
        </div>
      </div>
      
      <div v-else class="card-side cute-card-side">
        <div class="card-header cute-card-header">
          <h3 class="pixel-header h3 cute-answer-title">Answer</h3>
          <span class="box-level cute-box-level">Box {{ currentCard.box_level }}</span>
        </div>
        <div class="question-reminder cute-question-reminder">
          <strong>Question was:</strong> {{ currentCard.front }}
        </div>
        <div class="card-content answer cute-answer-content">{{ currentCard.back }}</div>
        <div class="card-actions rating-actions cute-rating-actions">
          <Button @click="rate(false)" :disabled="rating" variant="red" class="cute-wrong-button">
            {{ rating ? 'Processing...' : 'Wrong' }}
          </Button>
          <Button @click="rate(true)" :disabled="rating" variant="green" class="cute-correct-button">
            {{ rating ? 'Processing...' : 'Correct' }}
          </Button>
        </div>
      </div>
    </div>

    <div v-else-if="!loading" class="completion-screen cute-completion-screen">
      <div class="completion-character">
        <img src="/src/assets/white_wow.png" class="celebration-character" alt="Celebrating Character" />
      </div>
      <h3 class="cute-completion-title">STUDY SESSION COMPLETE!</h3>
      <p class="cute-completion-text">No more cards to review right now.</p>
      <BackButton :to="`/deck/${deckId}`" text="Back to Deck" />
    </div>

    <div v-if="loading" class="loading-screen cute-loading-screen">
      <div class="loading-content">
        <div class="loading-icon">⏳</div>
        <p class="cute-loading-text">LOADING NEXT CARD...</p>
        <div class="loading-character">
          <img src="/src/assets/orange_run.png" class="running-character" alt="Loading Character" />
        </div>
      </div>
    </div>
    

    <div v-if="error" class="pixel-message error">
      {{ error }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useAuth } from '../composables/useAuth'
import BackButton from '../components/BackButton.vue'
import Button from '../components/Button.vue'
import Header from '../components/Header.vue'

interface Card {
  id: number
  front: string
  back: string
  box_level: number
}

const route = useRoute()
const { router, getApiBase, getApiHeaders } = useAuth()
const deckId = route.params.id as string

const currentCard = ref<Card | null>(null)
const showAnswer = ref<boolean>(false)
const loading = ref<boolean>(false)
const rating = ref<boolean>(false)
const error = ref<string>('')
const deckTitle = ref<string>('')

async function loadNext(): Promise<void> {
  loading.value = true
  try {
    const res = await fetch(`${getApiBase()}/decks/${deckId}/study/next`, {
      headers: getApiHeaders()
    })
    
    if (res.ok) {
      const data = await res.json()
      currentCard.value = data.card
      if (data.deck_title) {
        deckTitle.value = data.deck_title
      }
      showAnswer.value = false
    } else {
      currentCard.value = null
    }
  } catch (e) {
    error.value = 'Network error'
  }
  loading.value = false
}

async function rate(correct: boolean): Promise<void> {
  if (rating.value) {
    return
  }
  rating.value = true
  
  try {
    if (currentCard.value) {
      await fetch(`${getApiBase()}/cards/${currentCard.value.id}/review`, {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          ...getApiHeaders()
        },
        body: JSON.stringify({ correct })
      })
      loadNext()
    }
  } catch (e) {
    error.value = 'Rating failed'
  } finally {
    rating.value = false
  }
}

function goBack(): void {
  router.push(`/deck/${deckId}`)
}

onMounted(loadNext)
</script>

<style scoped>
.cute-study-container {
  max-width: 900px;
  margin: 0 auto;
  padding: 10px;
  height: 100vh;
  box-sizing: border-box;
  overflow-y: auto;
}

.cute-card-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
}

.cute-card-side {
  background: linear-gradient(145deg, #fefefe, #fff8ff);
  border: 2px solid #dda0dd;
  border-radius: 15px;
  padding: 20px;
  max-width: 600px;
  width: 100%;
  min-height: 300px;
  display: flex;
  flex-direction: column;
  box-shadow: 
    0 0 0 2px rgba(221,160,221,0.3),
    0 6px 0 #dda0dd,
    0 10px 25px rgba(221,160,221,0.2);
  position: relative;
}

.cute-card-side::before {
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
  border-radius: 15px;
  opacity: 0.4;
}

@keyframes cardGlow {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}

.cute-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 3px solid #000;
}

.cute-question-title, .cute-answer-title {
  font-family: 'Fredoka One', Arial, sans-serif !important;
  color: #fda4ff !important;
  font-size: 14px !important;
  font-weight: 600 !important;
  text-shadow: 
    1px 1px 0 rgba(255,255,255,0.8),
    0 0 8px rgba(139,90,140,0.4);
  letter-spacing: 0.5px;
  margin: 0 !important;
  -webkit-text-stroke: 0.1px #000;
}

.cute-answer-title {
  color: #b8669b !important;
}

.cute-box-level {
  font-family: 'Fredoka One', Arial, sans-serif !important;
  background: linear-gradient(145deg, #fff8dc, #ffefd5);
  color: #b8860b !important;
  padding: 8px 16px;
  border: 2px solid #daa520;
  border-radius: 20px;
  font-weight: 600 !important;
  font-size: 12px;
  text-shadow: 1px 1px 0 rgba(255,255,255,0.6);
  box-shadow: 0 2px 0 #daa520, 0 4px 8px rgba(218,165,32,0.3);
}


.cute-card-content {
  font-family: 'Fredoka One', Arial, sans-serif !important;
  font-size: 18px !important;
  line-height: 1.6 !important;
  color: #664466 !important;
  text-align: center;
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px 0;
  font-weight: 600 !important;
  text-shadow: 1px 1px 0 rgba(255,255,255,0.5);
}

.cute-answer-content {
  color: #8b5a8c !important;
  border: 2px dashed #dda0dd;
  border-radius: 12px;
  padding: 15px !important;
  background: rgba(221,160,221,0.1);
}

.cute-question-reminder {
  font-family: 'Fredoka One', Arial, sans-serif !important;
  font-size: 12px !important;
  color: #9370db !important;
  background: rgba(147, 112, 219, 0.1);
  border: 2px solid #9370db;
  border-radius: 0;
  padding: 10px;
  margin-bottom: 15px;
  font-weight: 600 !important;
  text-align: left;
}

.cute-card-actions {
  display: flex;
  justify-content: center;
  gap: 15px;
  margin-top: 15px;
}

.cute-rating-actions {
  justify-content: space-between;
  gap: 20px;
}

.cute-show-button, .cute-wrong-button, .cute-correct-button {
  font-family: 'Fredoka One', Arial, sans-serif !important;
  font-weight: 600 !important;
  text-transform: uppercase;
  letter-spacing: 1px;
  font-size: 16px !important;
  padding: 15px 30px !important;
  min-width: 150px;
}


.cute-completion-screen {
  text-align: center;
  padding: 30px 20px;
  background: linear-gradient(135deg, #f8e6ff 0%, #e6f3ff 50%, #fff0e6 100%);
  border: 3px solid #dda0dd;
  border-radius: 20px;
  margin: 20px auto;
  max-width: 500px;
  box-shadow: 
    0 0 0 2px rgba(221,160,221,0.3),
    0 8px 16px rgba(0,0,0,0.1),
    inset 0 1px 0 rgba(255,255,255,0.9);
  position: relative;
}

.cute-completion-screen::before {
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

.completion-icon {
  font-size: 4rem;
  margin-bottom: 20px;
  animation: bounce 2s ease-in-out infinite;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-10px); }
}

.cute-completion-title {
  font-family: 'Fredoka One', sans-serif !important;
  color: #dd73f8 !important;
  font-size: 1.4rem !important;
  font-weight: 600 !important;
  text-shadow: 1px 1px 0 rgba(255,255,255,0.8);
  letter-spacing: 1px;
  margin: 0 0 20px 0 !important;
  -webkit-text-stroke: 0.1px #000;
}

.cute-completion-text {
  font-family: 'Fredoka One', sans-serif !important;
  color: #a259b4 !important;
  font-weight: 400 !important;
  font-size: 1rem;
  margin: 0 0 30px 0 !important;
  text-shadow: 1px 1px 0 rgba(255,255,255,0.8);
  opacity: 0.8;
}

.completion-character {
  margin: 20px 0;
}

.celebration-character {
  width: 64px;
  height: 64px;
  animation: celebrate 1.5s ease-in-out infinite;
}

@keyframes celebrate {
  0%, 100% { transform: scale(1) rotate(0deg); }
  50% { transform: scale(1.1) rotate(5deg); }
}

.cute-loading-screen {
  text-align: center;
  padding: 30px 20px;
  background: linear-gradient(135deg, #f8e6ff 0%, #e6f3ff 50%, #fff0e6 100%);
  border: 3px solid #dda0dd;
  border-radius: 20px;
  margin: 20px auto;
  max-width: 400px;
  box-shadow: 
    0 0 0 2px rgba(221,160,221,0.3),
    0 8px 16px rgba(0,0,0,0.1),
    inset 0 1px 0 rgba(255,255,255,0.9);
  position: relative;
}

.cute-loading-screen::before {
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

.loading-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

.loading-icon {
  font-size: 3rem;
  animation: spin 2s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.cute-loading-text {
  font-family: 'Fredoka One', sans-serif !important;
  color: #8b4a9c !important;
  font-weight: 600 !important;
  font-size: 1.2rem;
  text-shadow: 1px 1px 0 rgba(255,255,255,0.8);
  letter-spacing: 1px;
  margin: 0;
}

.loading-character {
  margin-top: 10px;
}

.running-character {
  width: 48px;
  height: 48px;
  animation: run 0.8s steps(2) infinite;
}

@keyframes run {
  0% { opacity: 1; }
  50% { opacity: 0.7; }
  100% { opacity: 1; }
}

.pixel-message.error {
  background: linear-gradient(145deg, #ffcccb, #ff6b6b);
  border: 3px solid #000;
  color: #8b0000;
  padding: 20px;
  margin: 20px 0;
  font-family: 'Fredoka One', Arial, sans-serif;
  font-weight: 600;
  text-align: center;
  box-shadow: 0 4px 0 #660000, 0 6px 8px rgba(0,0,0,0.2);
}


.pixel-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none !important;
  box-shadow: 0 2px 0 #333 !important;
}

/* Responsive */
@media (max-width: 768px) {
  .cute-study-container {
    padding: 10px;
  }
  
  .cute-study-header {
    flex-direction: column;
    gap: 15px;
    text-align: center;
    padding: 15px;
  }
  
  .cute-card-side {
    padding: 20px;
    min-height: 300px;
  }
  
  .cute-card-content {
    font-size: 16px !important;
    padding: 20px 0;
  }
  
  .cute-rating-actions {
    flex-direction: column;
    gap: 15px;
  }
  
  .cute-show-button, .cute-wrong-button, .cute-correct-button {
    font-size: 14px !important;
    padding: 12px 20px !important;
    min-width: 120px;
  }
  
  .cute-completion-screen {
    padding: 40px 20px;
    margin: 20px auto;
  }
  
  .cute-completion-title {
    font-size: 12px !important;
  }
}
</style>
