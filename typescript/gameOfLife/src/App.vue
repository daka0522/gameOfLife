<template>
    <h1>Conway's Game of Life</h1>
    <div>
        <span>Step: {{ step }}</span>
        <button @click="start">Start</button>
        <button @click="stop">Stop</button>
        <button @click="reset">Reset</button>
    </div>
    <canvas ref="canvasRef" width="800" height="800"></canvas>
</template>

<script setup lang="ts">
import { Game } from './gameOfLife';
import { onMounted, ref, onUnmounted } from 'vue';

const canvasRef = ref<HTMLCanvasElement | null>(null)

let game: Game
let animationId: number | null
let step = ref(0)

function animate() {
    game.drawGrid();
    game.nextGeneration();
    animationId = requestAnimationFrame(animate);
    step.value++
}

function start() {
    if (!animationId) {
        animate()
    }
}

function stop() {
    if (animationId) {
        cancelAnimationFrame(animationId)
        animationId = null
    }
}

function reset() {
    stop()
    if (canvasRef.value) {
        game = new Game(canvasRef.value)
        step.value = 0
    }
    start()
}

onMounted(() => {
    if (canvasRef.value) {
        game = new Game(canvasRef.value)
    }
    start()
})

onUnmounted(() => {
    stop()
})
</script>

<style scoped>
canvas {
    max-width: 85vmin;
    max-height: 85vmin;
}

span {
  margin: 1rem;
}
</style>