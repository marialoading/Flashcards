<template>
  <div class="cute-header">
    <h1 class="cute-title">{{ pageTitle || 'FLASH DECK' }}</h1>
    <div class="header-actions">
      <LeitnerInfo />
      <slot name="page-actions"></slot>
      <Button v-if="showLogout" @click="logout" variant="cyan">
        LOGOUT
      </Button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useAuth } from '../composables/useAuth'
import Button from './Button.vue'
import LeitnerInfo from './LeitnerInfo.vue'

interface Props {
  pageTitle?: string
  showLogout?: boolean
}

defineProps<Props>()

const { router } = useAuth()

function logout() {
  localStorage.removeItem('token')
  router.push('/login')
}
</script>

<style scoped>
.cute-header {
  background: linear-gradient(145deg, #ff9dff, #dda0dd);
  padding: 30px 40px;
  text-align: center;
  border-radius: 15px;
  margin-bottom: 30px;
  position: relative;
  box-shadow: 
    0 0 0 3px rgba(255,255,255,0.8),
    0 0 0 6px #ff9dff,
    0 8px 20px rgba(255,157,255,0.3);
  display: flex;
  justify-content: space-between;
  align-items: center;
  min-height: 120px;
}

.cute-header::before {
  content: '';
  position: absolute;
  top: -6px;
  left: -6px;
  right: -6px;
  bottom: -6px;
  background: linear-gradient(45deg, #ff9dff, #b8f2ff, #ffc8dd, #fff2b8);
  background-size: 300% 300%;
  animation: headerGlow 6s ease infinite;
  z-index: -1;
  border-radius: 15px;
  opacity: 0.7;
}

@keyframes headerGlow {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}

.cute-title {
  font-family: 'Fredoka One', Arial, sans-serif;
  font-size: 2.5rem;
  color: #fff;
  text-shadow: 
    3px 3px 0 #000,
    -1px -1px 0 #000,
    1px -1px 0 #000,
    -1px 1px 0 #000,
    1px 1px 0 #000,
    0 0 15px rgba(255,255,255,0.5);
  letter-spacing: 3px;
  margin: 0;
  text-transform: uppercase;
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  pointer-events: none;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 20px;
  position: absolute;
  right: 20px;
  top: 50%;
  transform: translateY(-50%);
  z-index: 10;
}

/* Responsive Design */
@media (max-width: 768px) {
  .cute-header {
    flex-direction: column;
    gap: 20px;
    padding: 25px 20px;
    text-align: center;
  }
  
  .cute-title {
    font-size: 2rem;
    letter-spacing: 2px;
  }
  
  .header-actions {
    gap: 15px;
  }
}

@media (max-width: 480px) {
  .cute-header {
    padding: 20px 15px;
  }
  
  .cute-title {
    font-size: 1.8rem;
    letter-spacing: 1px;
  }
  
  .header-actions {
    gap: 12px;
  }
}
</style>