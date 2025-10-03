<template>
  <button 
    :class="buttonClasses" 
    :style="{ '--btn-color': colors[props.variant] || colors.default }"
    :disabled="disabled || loading"
    @click="emit('click', $event)"
    :type="type"
  >
    <span v-if="loading" class="loading-spinner">⏳</span>
    <slot v-else />
  </button>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  variant?: 'green' | 'red' | 'yellow' | 'cyan' | 'purple' | 'default'
  size?: 'small' | 'medium' | 'large'
  disabled?: boolean
  loading?: boolean
  type?: 'button' | 'submit' | 'reset'
  fullWidth?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'default',
  size: 'medium',
  disabled: false,
  loading: false,
  type: 'button',
  fullWidth: false
})

const emit = defineEmits<{
  click: [event: MouseEvent]
}>()

const buttonClasses = computed(() => [
  'pixel-button',
  `pixel-button--${props.variant}`,
  `pixel-button--${props.size}`,
  {
    'pixel-button--disabled': props.disabled || props.loading,
    'pixel-button--loading': props.loading,
    'pixel-button--full-width': props.fullWidth
  }
])

const colors = {
  default: '#664466',
  green: '#32cd32', 
  red: '#ff6b6b',
  yellow: '#ffd700',
  cyan: '#00bfff',
  purple: '#9370db'
}
</script>

<style scoped>
.pixel-button {
  font-family: 'Fredoka One', Arial, sans-serif;
  font-weight: 400;
  text-transform: none;
  letter-spacing: 0.5px;
  border: 3px solid var(--btn-color, #664466);
  background: color-mix(in srgb, var(--btn-color, #664466) 20%, white);
  color: color-mix(in srgb, var(--btn-color, #664466) 80%, black);
  cursor: pointer;
  position: relative;
  border-radius: 0;
  transition: all 0.3s ease;
  box-shadow: 0 4px 0 color-mix(in srgb, var(--btn-color, #664466) 60%, black), 0 6px 8px rgba(0,0,0,0.1);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  text-decoration: none;
  border: none;
  outline: none;
}

.pixel-button:hover:not(.pixel-button--disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 0 color-mix(in srgb, var(--btn-color, #664466) 60%, black), 0 8px 12px rgba(0,0,0,0.15);
  background: color-mix(in srgb, var(--btn-color, #664466) 15%, white);
}

.pixel-button:active:not(.pixel-button--disabled) {
  transform: translateY(2px);
  box-shadow: 0 2px 0 color-mix(in srgb, var(--btn-color, #664466) 60%, black), 0 4px 6px rgba(0,0,0,0.1);
}

.pixel-button--small {
  font-size: 10px;
  padding: 8px 14px;
}

.pixel-button--medium {
  font-size: 12px;
  padding: 10px 18px;
}

.pixel-button--large {
  font-size: 14px;
  padding: 12px 24px;
}

/* State Variants */
.pixel-button--disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none !important;
}

.pixel-button--loading {
  cursor: wait;
}

.pixel-button--full-width {
  width: 100%;
}

.loading-spinner {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

@media (max-width: 768px) {
  .pixel-button--large {
    font-size: 12px;
    padding: 10px 20px;
  }
  
  .pixel-button--medium {
    font-size: 11px;
    padding: 9px 16px;
  }
  
  .pixel-button--small {
    font-size: 9px;
    padding: 7px 12px;
  }
}
</style>