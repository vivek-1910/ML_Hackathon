# 🎮 Quick Start Guide - Hangman Web App

## Prerequisites
- Python 3.7+ installed
- Node.js 14+ and npm installed
- Terminal/Command Line access

## Setup (First Time Only)

### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
```

This installs Flask, Flask-CORS, NumPy, and other dependencies.

### 2. Install React Dependencies
```bash
cd hangman-web
npm install
cd ..
```

This installs React, Axios, Lucide-React, and other frontend dependencies.

## Running the App

### Easy Way: Use the Start Script
```bash
./start.sh
```

This automatically starts both servers!

### Manual Way: Two Terminals

**Terminal 1 - Backend:**
```bash
python app.py
```
Wait for: `✓ Oracle initialized with 50000 corpus words`
Server runs on: http://localhost:5001

**Terminal 2 - Frontend:**
```bash
cd hangman-web
npm start
```

## Access the Game

Open your browser to: **http://localhost:3000**

**Note**: Backend runs on port 5001, frontend on port 3000

## How to Play

1. **New Game** - Click to start a new random word
2. **Click Letters** - Click on the keyboard to guess letters
3. **Get Hint** - See AI's top 5 suggestions with probabilities
4. **AI Play** - Let AI make one guess
5. **Auto Play** - Watch AI play the entire game

## Features

- ✅ Interactive virtual keyboard
- ✅ Real-time hangman visualization
- ✅ AI hints with probability scores
- ✅ Auto-play mode
- ✅ Beautiful gradient UI
- ✅ Win/loss tracking

## Troubleshooting

### "Cannot connect to backend"
- Make sure Flask is running on port 5001
- Check Terminal 1 for errors

### "Port 3000 already in use"
```bash
# Kill existing process
lsof -ti:3000 | xargs kill -9
# Then restart
npm start
```

### "Module not found"
```bash
# Python modules
pip install -r requirements.txt

# Node modules
cd hangman-web
npm install
```

## API Endpoints

The Flask backend provides these endpoints:

- `POST /api/init` - Initialize oracle
- `POST /api/new-game` - Start new game
- `POST /api/guess` - Make a guess
- `GET /api/ai-hint` - Get AI suggestions
- `POST /api/ai-play` - AI makes a move
- `GET /api/game-state` - Get current state

## Tech Stack

**Backend:**
- Flask (Python web framework)
- ML Oracle (42% win rate, 4-gram weighted)
- NumPy (numerical computations)

**Frontend:**
- React 18 (UI framework)
- Axios (HTTP client)
- Lucide React (icons)
- Custom CSS with gradients

## Performance

The AI oracle achieves:
- **42% win rate** on test set
- **0% corpus overlap** (generalizes well)
- **4-gram weighted** probabilistic model
- **Real-time predictions** (<100ms per guess)

## Need Help?

See `WEB_APP_README.md` for detailed documentation.

---

**Enjoy playing Hangman with AI! 🎮🤖**
