<template>
  <div class="leitner-info">
    <button 
      @click="toggle" 
      class="info-trigger" 
      :class="{ active: isOpen }"
      title="Leitner Algorithm Info"
    >
      i
    </button>
    
    <Transition name="info-slide">
      <div v-if="isOpen" class="info-panel">
        <div class="info-header">
          <h3 class="info-title">Leitner Algorithm</h3>
        </div>
        
        <div class="info-content">
          <div class="algorithm-section">
            <h4>Box System</h4>
            <div class="box-grid">
              <div v-for="(info, index) in boxInfo" :key="index" class="box-item">
                <div class="box-number">Box {{ index + 1 }}</div>
                <div class="box-interval">{{ info.interval }}</div>
              </div>
            </div>
          </div>
          
          <div class="algorithm-section">
            <h4>How it works</h4>
            <div class="flow-steps">
              <div class="step">
                <strong>Correct:</strong> Card moves up one box
              </div>
              <div class="step">
                <strong>Wrong:</strong> Card returns to Box 1
              </div>
              <div class="step">
                <strong>Mastery:</strong> Cards in Box 5 are mastered
              </div>
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const isOpen = ref(false)

const boxInfo = [
  { interval: '1 day' },
  { interval: '3 days' },
  { interval: '7 days' },
  { interval: '14 days' },
  { interval: '30 days' }
]

function toggle() {
  isOpen.value = !isOpen.value
}
</script>

<style scoped>
.leitner-info {
  position: relative;
  display: inline-block;
}

.info-trigger {
  background: linear-gradient(145deg, #e6f3ff, #cce7ff);
  border: 2px solid #4a90e2;
  border-radius: 50%;
  width: 32px;
  height: 32px;
  font-size: 16px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  box-shadow: 0 2px 4px rgba(74, 144, 226, 0.2);
}

.info-trigger:hover {
  background: linear-gradient(145deg, #cce7ff, #b3daff);
  transform: scale(1.1);
  box-shadow: 0 4px 8px rgba(74, 144, 226, 0.3);
}

.info-trigger.active {
  background: linear-gradient(145deg, #4a90e2, #357abd);
  color: white;
  transform: scale(1.1);
}

.info-panel {
  position: absolute;
  top: 40px;
  right: 0;
  width: 320px;
  background: rgba(255, 255, 255, 0.98);
  border: 3px solid #4a90e2;
  border-radius: 15px;
  box-shadow: 
    0 0 0 2px rgba(74, 144, 226, 0.2),
    0 8px 25px rgba(0, 0, 0, 0.15);
  z-index: 1000;
  font-family: 'Fredoka One', sans-serif;
  backdrop-filter: blur(10px);
}

.info-header {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 15px 20px;
  background: linear-gradient(145deg, #4a90e2, #357abd);
  border-radius: 12px 12px 0 0;
  color: white;
}

.info-title {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 600;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2);
}

.info-content {
  padding: 20px;
  max-height: 400px;
  overflow-y: auto;
}

.algorithm-section {
  margin-bottom: 20px;
}

.algorithm-section h4 {
  color: #4a90e2;
  font-size: 1rem;
  margin: 0 0 12px 0;
  font-weight: 600;
  text-shadow: 1px 1px 0 rgba(255, 255, 255, 0.8);
}

.box-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(80px, 1fr));
  gap: 8px;
  margin-bottom: 15px;
}

.box-item {
  background: linear-gradient(145deg, #fff2e6, #ffe8cc);
  border: 2px solid #daa520;
  border-radius: 10px;
  padding: 8px;
  text-align: center;
  box-shadow: 0 2px 4px rgba(218, 165, 32, 0.2);
}

.box-number {
  font-weight: 600;
  color: #b8860b;
  font-size: 0.85rem;
  margin-bottom: 4px;
}

.box-interval {
  font-size: 0.75rem;
  color: #8b6914;
  font-weight: 600;
  margin-bottom: 4px;
}

.box-desc {
  font-size: 0.65rem;
  color: #6b5416;
  line-height: 1.2;
}

.flow-steps {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.step {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  background: rgba(74, 144, 226, 0.1);
  border-radius: 8px;
  font-size: 0.8rem;
  border-left: 3px solid #4a90e2;
}

.benefits-list {
  margin: 0;
  padding-left: 20px;
  font-size: 0.8rem;
  color: #555;
  line-height: 1.4;
}

.benefits-list li {
  margin-bottom: 6px;
}

.info-slide-enter-active,
.info-slide-leave-active {
  transition: all 0.3s ease;
}

.info-slide-enter-from {
  opacity: 0;
  transform: translateY(-10px) scale(0.95);
}

.info-slide-leave-to {
  opacity: 0;
  transform: translateY(-10px) scale(0.95);
}

/* Responsive */
@media (max-width: 480px) {
  .info-panel {
    width: 280px;
    right: -50px;
  }
  
  .box-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .info-content {
    padding: 15px;
  }
}
</style>