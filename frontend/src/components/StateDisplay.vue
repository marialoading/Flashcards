<template>
  <div class="state-container">
    <div v-if="loading" class="loading-state pixel-pulse cute-loading">
      {{ loadingText || 'LOADING...' }}
    </div>
    
    <div v-else-if="isEmpty" class="empty-state pixel-panel cute-empty-panel">
      <div class="empty-content">
        <h3 class="pixel-header h3 cute-empty-title">{{ title || 'NO ITEMS FOUND' }}</h3>
        <p class="cute-empty-text">{{ message || 'Add your first item to get started!' }}</p>
      </div>
    </div>
    
    <slot v-else></slot>
  </div>
</template>

<script setup lang="ts">
interface Props {
  loading?: boolean
  isEmpty?: boolean
  loadingText?: string
  icon?: string
  title?: string
  message?: string
}

defineProps<Props>()
</script>

<style scoped>
.state-container {
  width: 100%;
}

.loading-state {
  text-align: center;
  padding: 40px;
  font-size: 18px;
  font-weight: 600;
}

.empty-state {
  text-align: center;
  padding: 40px;
}

.empty-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 15px;
}

.empty-icon {
  font-size: 48px;
  margin-bottom: 10px;
}


.cute-loading {
  font-family: 'Fredoka One', sans-serif !important;
  color: #8b4a9c !important;
  text-shadow: 1px 1px 0 rgba(255,255,255,0.8);
  font-weight: 600 !important;
  text-transform: uppercase;
  letter-spacing: 2px;
  font-size: 1.2rem;
}

.cute-empty-panel {
  background: linear-gradient(135deg, #f8e6ff 0%, #e6f3ff 50%, #fff0e6 100%) !important;
  border: 3px solid #dda0dd !important;
  border-radius: 20px !important;
  box-shadow: 
    0 0 0 2px rgba(221,160,221,0.3),
    0 8px 16px rgba(0,0,0,0.1),
    inset 0 1px 0 rgba(255,255,255,0.9) !important;
  position: relative;
  padding: 40px 30px !important;
}

.cute-empty-panel::before {
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

.cute-empty-icon {
  color: #ff9dff !important;
  font-weight: bold !important;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
  animation: iconFloat 3s ease-in-out infinite;
  font-size: 4rem !important;
}

@keyframes iconFloat {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-10px);
  }
}

.cute-empty-title {
  font-family: 'Fredoka One', sans-serif !important;
  color: #8b4a9c !important;
  font-size: 1.4rem !important;
  font-weight: 600 !important;
  text-shadow: 1px 1px 0 rgba(255,255,255,0.8);
  letter-spacing: 1px;
  margin: 0 !important;
}

.cute-empty-text {
  font-family: 'Fredoka One', sans-serif !important;
  color: #8b4a9c !important;
  font-weight: 400 !important;
  text-shadow: 1px 1px 0 rgba(255,255,255,0.8);
  margin: 0 !important;
  font-size: 1rem;
  opacity: 0.8;
}

@media (max-width: 600px) {
  .loading-state, .empty-state {
    padding: 20px;
  }
  
  .empty-icon {
    font-size: 36px;
  }
  
  .cute-empty-title {
    font-size: 12px !important;
  }
  
  .cute-loading {
    font-size: 16px;
    letter-spacing: 1px;
  }
}
</style>
