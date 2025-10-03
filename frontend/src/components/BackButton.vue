<template>
  <Button @click="handleBack" variant="cyan" class="cute-back-button">
    {{ text || 'BACK' }}
  </Button>
</template>

<script setup lang="ts">
import { useAuth } from '../composables/useAuth'
import Button from './Button.vue'

interface Props {
  to?: string
  text?: string
}

const props = defineProps<Props>()
const { router } = useAuth()

function handleBack(): void {
  if (props.to) {
    router.push(props.to)
  } else {
    router.back()
  }
}
</script>

<style scoped>
.cute-back-button {
  font-family: 'Fredoka One', Arial, sans-serif !important;
  font-weight: 600 !important;
  text-transform: uppercase;
  letter-spacing: 1px;
  text-shadow: 1px 1px 0 rgba(0,0,0,0.3);
}
</style>
