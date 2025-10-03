<template>
  <div class="cute-auth">
    <div class="auth-container">
      <div class="auth-header">
        <h1 class="auth-title">Flashcards</h1>
        
        <!-- Characters sitting on the panel -->
        <div class="characters-on-panel">
          <img src="/src/assets/orange_stand.png" class="panel-character orange-char" alt="Orange Character" />
          <img src="/src/assets/white_wow.png" class="panel-character white-char" alt="White Character" />
        </div>
      </div>
      
      <div class="auth-panel">
        <form @submit.prevent="handleSubmit" class="auth-form">
          <div class="form-group">
            <label class="form-label">Username</label>
            <input 
              v-model="username" 
              placeholder="Enter your username..." 
              required 
              class="form-input"
              autocomplete="username"
            />
          </div>
          
          <div v-if="isRegister" class="form-group">
            <label class="form-label">Email</label>
            <input 
              v-model="email" 
              type="email"
              placeholder="Enter your email..." 
              required 
              class="form-input"
              autocomplete="email"
            />
          </div>
          
          <div class="form-group">
            <label class="form-label">Password</label>
            <input 
              v-model="password" 
              type="password" 
              placeholder="Enter your password..." 
              required 
              class="form-input"
              :autocomplete="isRegister ? 'new-password' : 'current-password'"
            />
          </div>
          
          <div class="form-actions">
            <Button 
              type="submit" 
              :disabled="loading"
              variant="cyan"
              fullWidth
              style="margin-bottom: 18px;"
            >
              {{ loading ? loadingText : buttonText }}
            </Button>
            
            <router-link :to="linkTo" class="switch-link">
              {{ linkText }}
            </router-link>
          </div>
        </form>
        
        <div v-if="error" class="error-message">
          {{ error }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useAuth } from '../composables/useAuth'
import Button from './Button.vue'

const route = useRoute()
const { router, getApiBase } = useAuth()

const isRegister = computed(() => route.path === '/register')
const buttonText = computed(() => isRegister.value ? 'CREATE ACCOUNT' : 'LOGIN')
const loadingText = computed(() => isRegister.value ? 'REGISTERING...' : 'CONNECTING...')
const linkTo = computed(() => isRegister.value ? '/login' : '/register')
const linkText = computed(() => isRegister.value ? '<<< BACK TO LOGIN' : '>>> CREATE NEW ACCOUNT')

const username = ref<string>('')
const email = ref<string>('')
const password = ref<string>('')
const error = ref<string>('')
const loading = ref<boolean>(false)

async function handleSubmit(): Promise<void> {
  error.value = ''
  loading.value = true
  
  const endpoint = isRegister.value ? '/register' : '/login'
  const payload = isRegister.value 
    ? { username: username.value, email: email.value, password: password.value }
    : { username: username.value, password: password.value }
  
  try {
    const res = await fetch(`${getApiBase()}${endpoint}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })
    
    const data = await res.json()
    if (!res.ok) {
      error.value = data.error || `${isRegister.value ? 'Registration' : 'Login'} failed`
      return
    }
    
    localStorage.setItem('token', data.token)
    router.push('/')
  } catch (e) {
    error.value = 'Network error'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.cute-auth {
  min-height: 100vh;
  background: linear-gradient(135deg, #f8e6ff 0%, #e6f3ff 50%, #fff0e6 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  font-family: 'Fredoka One', sans-serif;
}

.auth-container {
  max-width: 450px;
  width: 100%;
  position: relative;
}
/* Header */
.auth-header {
  text-align: center;
  margin-bottom: 30px;
}

.auth-title {
  font-family: 'Fredoka One', sans-serif;
  font-size: 2.5rem;
  color: #8b4a9c;
  text-shadow: 
    2px 2px 0 rgba(255,255,255,0.8),
    0 0 20px rgba(139, 74, 156, 0.3);
  margin: 0 0 20px 0;
  letter-spacing: 1px;
  font-weight: 600;
}

.characters-on-panel {
  display: flex;
  justify-content: center;
  align-items: flex-end;
  gap: 30px;
  margin-bottom: -15px;
  position: relative;
  z-index: 2;
}

.panel-character {
  width: 56px;
  height: 56px;
  image-rendering: pixelated;
  image-rendering: -moz-crisp-edges;
  image-rendering: crisp-edges;
  filter: drop-shadow(2px 2px 4px rgba(0,0,0,0.1));
}

.panel-character.orange-char {
  animation: characterFloat 4s ease-in-out infinite;
  animation-delay: 0s;
}

.panel-character.white-char {
  animation: characterFloat 4s ease-in-out infinite;
  animation-delay: 2s;
}

@keyframes characterFloat {
  0%, 100% {
    transform: translateY(0px) rotate(-2deg);
  }
  25% {
    transform: translateY(-8px) rotate(1deg);
  }
  50% {
    transform: translateY(-12px) rotate(2deg);
  }
  75% {
    transform: translateY(-8px) rotate(-1deg);
  }
}

.auth-panel {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 25px;
  border: 3px solid #dda0dd;
  padding: 40px;
  box-shadow: 
    0 0 0 2px rgba(221,160,221,0.3),
    0 15px 35px rgba(0,0,0,0.1),
    inset 0 1px 0 rgba(255,255,255,0.9);
  position: relative;
}

.auth-panel::before {
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
  opacity: 0.6;
  border-radius: 25px;
}

@keyframes panelGlow {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}

.auth-form {
  width: 100%;
  text-align: center;
}

.form-group {
  margin-bottom: 25px;
  text-align: center;
}

.form-label {
  font-family: 'Fredoka One', sans-serif;
  font-size: 1.1rem;
  font-weight: 600;
  color: #8b4a9c;
  display: block;
  margin-bottom: 10px;
  text-shadow: 1px 1px 0 rgba(255,255,255,0.8);
  text-align: center;
}

.form-input {
  width: 100%;
  max-width: 280px;
  padding: 15px 20px;
  font-family: 'Fredoka One', sans-serif;
  font-size: 1rem;
  font-weight: 500;
  background: rgba(255, 255, 255, 0.9);
  border: 3px solid #dda0dd;
  border-radius: 20px;
  color: #664466;
  text-align: center;
  transition: all 0.3s ease;
  box-shadow: 
    inset 0 2px 4px rgba(221,160,221,0.1),
    0 2px 8px rgba(0,0,0,0.05);
  margin: 0 auto;
  display: block;
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
  text-align: center;
}

.form-actions {
  margin-top: 35px;
  text-align: center;
}

.submit-button {
  width: 100%;
  max-width: 280px;
  padding: 18px 25px;
  font-family: 'Fredoka One', sans-serif;
  font-size: 1.1rem;
  font-weight: 600;
  background: linear-gradient(135deg, #ff9dff, #dda0dd);
  border: 3px solid #ff9dff;
  border-radius: 25px;
  color: #fff;
  text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
  cursor: pointer;
  transition: all 0.3s ease;
  margin-bottom: 20px;
  text-transform: uppercase;
  letter-spacing: 1px;
  box-shadow: 
    0 8px 0 #cc7acc,
    0 15px 25px rgba(221,160,221,0.3);
}

.submit-button:hover:not(:disabled) {
  transform: translateY(-3px);
  box-shadow: 
    0 12px 0 #cc7acc,
    0 20px 35px rgba(221,160,221,0.4);
  background: linear-gradient(135deg, #ffb3ff, #e6b3e6);
}

.submit-button:active:not(:disabled) {
  transform: translateY(2px);
  box-shadow: 
    0 4px 0 #cc7acc,
    0 8px 15px rgba(221,160,221,0.3);
}

.submit-button:disabled {
  background: linear-gradient(135deg, #ccc, #999);
  border-color: #ccc;
  cursor: not-allowed;
  transform: none;
  box-shadow: 
    0 4px 0 #999,
    0 8px 15px rgba(0,0,0,0.1);
}

.switch-link {
  display: inline-block;
  font-family: 'Fredoka One', sans-serif;
  font-size: 0.95rem;
  font-weight: 600;
  color: #8b4a9c;
  text-decoration: none;
  padding: 12px 25px;
  border: 2px solid #dda0dd;
  border-radius: 20px;
  background: rgba(221,160,221,0.1);
  transition: all 0.3s ease;
  text-shadow: 1px 1px 0 rgba(255,255,255,0.5);
}

.switch-link:hover {
  background: linear-gradient(135deg, #dda0dd, #ff9dff);
  color: #fff;
  text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(221,160,221,0.3);
}

.error-message {
  background: linear-gradient(135deg, #ffcccb, #ff9999);
  border: 3px solid #ff6b6b;
  border-radius: 15px;
  color: #8b0000;
  padding: 15px 20px;
  margin-top: 20px;
  font-family: 'Fredoka One', sans-serif;
  font-weight: 600;
  text-align: center;
  font-size: 0.95rem;
  box-shadow: 
    0 4px 0 #cc4444,
    0 8px 20px rgba(255,107,107,0.2);
  text-shadow: 1px 1px 0 rgba(255,255,255,0.3);
}

@media (max-width: 600px) {
  .cute-auth {
    padding: 15px;
  }
  
  .auth-container {
    max-width: 100%;
  }
  
  .auth-title {
    font-size: 2rem;
    letter-spacing: 0.5px;
  }
  
  .auth-panel {
    padding: 30px 25px;
    border-radius: 20px;
  }
  
  .characters-on-panel {
    gap: 20px;
    margin-bottom: -10px;
  }
  
  .panel-character {
    width: 48px;
    height: 48px;
  }
  
  .form-input,
  .submit-button {
    max-width: 100%;
    font-size: 0.95rem;
  }
  
  .submit-button {
    padding: 16px 20px;
  }
  
  .switch-link {
    font-size: 0.85rem;
    padding: 10px 20px;
  }
}

@media (max-width: 400px) {
  .auth-title {
    font-size: 1.8rem;
  }
  
  .auth-panel {
    padding: 25px 20px;
  }
  
  .panel-character {
    width: 40px;
    height: 40px;
  }
  
  .characters-on-panel {
    gap: 15px;
  }
  
  .form-input {
    padding: 12px 15px;
  }
  
  .submit-button {
    padding: 14px 15px;
  }
}

.auth-panel:hover::before {
  animation-duration: 6s;
}

.form-group:hover .form-input {
  border-color: #ffb3ff;
}

.form-group:hover .form-label {
  color: #ff6b9d;
  transform: scale(1.02);
  transition: all 0.3s ease;
}
</style>
