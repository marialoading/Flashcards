<template>
<router-view />
</template>

<style>
@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=Fredoka+One:wght@400&display=swap');

* {
  box-sizing: border-box;
}

body {
  margin: 0;
  padding: 10px;
  background: linear-gradient(45deg, #fefcf8 25%, #fffef0 25%, #fffef0 50%, #fefcf8 50%, #fefcf8 75%, #fffef0 75%, #fffef0);
  background-size: 30px 30px;
  font-family: 'Fredoka One', Arial, sans-serif;
  color: #5a4a4a;
  height: 100vh;
  overflow: hidden;
  animation: gentleFloat 15s ease-in-out infinite;
}

@keyframes gentleFloat {
  0%, 100% { background-position: 0 0; }
  50% { background-position: 15px 15px; }
}


.pixel-input {
  font-family: 'Fredoka One', Arial, sans-serif;
  font-size: 12px;
  padding: 10px 14px;
  border: 3px solid #664466;
  background: #fefcf8;
  color: #664466;
  outline: none;
  border-radius: 0;
  transition: all 0.3s ease;
  box-shadow: 0 2px 0 #443344, inset 0 2px 4px rgba(0,0,0,0.1);
}

.pixel-input:focus {
  border-color: #8b3a5c;
  background: #fff;
  box-shadow: 0 2px 0 #5c2a3d, inset 0 2px 4px rgba(139, 58, 92, 0.1), 0 0 8px rgba(139, 58, 92, 0.3);
}

.pixel-panel {
  background: linear-gradient(145deg, #fefcf8, #fff);
  border: 3px solid #664466;
  border-radius: 0;
  padding: 20px;
  margin: 15px 0;
  box-shadow: 0 4px 0 #443344, 0 6px 12px rgba(0,0,0,0.1);
  position: relative;
}


.pixel-header {
  font-family: 'Fredoka One', Arial, sans-serif;
  font-weight: 700;
  margin: 0 0 20px 0;
  text-shadow: 2px 2px 0 rgba(0,0,0,0.1);
}

.pixel-header.h1 {
  font-size: 28px;
  color: #8b3a5c;
  text-shadow: 3px 3px 0 rgba(0,0,0,0.2);
}

.pixel-header.h2 {
  font-size: 22px;
  color: #6a4c93;
  text-shadow: 2px 2px 0 rgba(0,0,0,0.15);
}

.pixel-header.h3 {
  font-size: 16px;
  color: #2d5f3f;
  text-shadow: 1px 1px 0 rgba(0,0,0,0.1);
}

.pixel-pulse {
  animation: sweetPulse 2s infinite ease-in-out;
}

@keyframes sweetPulse {
  0%, 100% { 
    opacity: 1; 
    transform: scale(1);
  }
  50% { 
    opacity: 0.8; 
    transform: scale(1.02);
  }
}
</style>