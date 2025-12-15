
 <h3 align="left">flashcard app with cats! </h3>
 <h4> Click on the newest release!  </h4>
 <dl align="left">
    <dt>
       <dt> Built for exam preperation, powered by cats, pastel gradients and the mighty leitner algorithm. </dt>
       <dt> I also drew this extremely complicated cat portraits which absolutely took more time than coding this.  </dt>
       <dt> You can register and start creating decks, includes study mode with spaced repetition (Leitner system, but cuter~) </dt>
       <dt> Feel free to add Decks for learning, it's currently empty. </dt>
    </dt>
</dl>

<h3 align="center"> used Tech-Stack:</h3> 
<dl align="left">
    <dt>
        <dt> Backend: Python + Flask + PostgreSQL</dt>
        <dt> Frontend: Vue 3 + TypeScript + CSS</dt>
        <dt> Desktop App: Tauri (Rust + Web)</dt>
        <dt> Deployment: Docker</dt>
        <dt> Development: Vite + HMR</dt>
    </dt>
</dl>

##  Quick Start

### Option 1: Download Pre-built App (Recommended) 
1. **Download the latest release** from [GitHub Releases](https://github.com/marialoading/Flashcards/releases)
2. **Choose your preferred option:**
   - **`app.exe`** - Portable standalone app (just download & run!)
   - **`flashcards_1.0.0_x64_en-US.msi`** - Windows Installer Package (adds to Programs)
   - **`flashcards_1.0.0_x64-setup.exe`** - Setup Wizard with uninstaller

**System Requirements:** Windows 10/11 (64-bit) • ~8.5 MB space

### Option 2: Build from Source
```bash
# Clone the repository
git clone https://github.com/marialoading/Flashcards
cd flashcards

# Start the backend services
docker-compose up -d

# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Development mode (with live reload)
npm run tauri:dev

# Or build for production
npm run tauri:build
```

##  After Building Locally

When you build the app yourself, you'll find your files here:

###  **Your Built App:**
```
frontend/src-tauri/target/release/app.exe
```

###  **Your Built Installers:**
```
frontend/src-tauri/target/release/bundle/msi/flashcards_0.1.0_x64_en-US.msi
frontend/src-tauri/target/release/bundle/nsis/flashcards_0.1.0_x64-setup.exe
```

**Note:** The `target/` folder is not included in the repository - you need to build these files yourself or download from releases.

### Frontend Development:
```bash
npm run dev          # Start Vite dev server only
npm run build        # Build frontend only
npm run tauri:dev    # Start Tauri app in development
npm run tauri:build  # Build production Tauri app
```

### Backend Development:
```bash
docker-compose up -d     # Start PostgreSQL database
docker-compose down      # Stop all services
```


##  Contributing

Feel free to contribute to make this app even more cat! 
-  Add more cute cats
- Improve animations  
-  Enhance the study algorithms
-  Add permanent decks
-  Add more pastel gradients

---

**Now available as native desktop app with v1.0.0! 🎮✨**
