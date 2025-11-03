# Hangman Web App - Setup Instructions

## ✅ Complete Setup

### 1. Install Python Dependencies
```bash
pip3 install flask flask-cors numpy
```

### 2. Install React Dependencies
```bash
cd hangman-web
npm install
cd ..
```

## 🚀 Running the Application

### Option 1: Quick Start (Recommended)
```bash
./start.sh
```

### Option 2: Manual Start

**Terminal 1 - Backend (Port 5001):**
```bash
python3 app.py
```

**Terminal 2 - Frontend (Port 3000):**
```bash
cd hangman-web
npm start
```

## 🎮 How to Use

### Access the Game
Open your browser to: **http://localhost:3000**

### Game Modes

#### 1. Random Word Mode
- Click **"Random Word"** button
- Game selects a word from the test set (2000 words)
- Try to guess the word!

#### 2. Custom Word Mode ⭐ NEW
- Click **"Custom Word"** button
- Enter any word (letters only, no spaces)
- Click **"Start Game"** or press Enter
- Play with your own word!

### AI Features
- **Get Hint**: See AI's top 5 letter suggestions with probabilities
- **AI Play**: Let AI make one guess
- **Auto Play**: Watch AI play automatically (1 guess per second)

## 🔧 Port Configuration

**Important**: Port 5000 is used by Apple iTunes/AirPlay on macOS.

This app uses:
- **Backend**: Port 5001 (Flask API)
- **Frontend**: Port 3000 (React Dev Server)

## 📝 Features

✅ Interactive virtual keyboard  
✅ Real-time hangman visualization  
✅ Random word selection from test set  
✅ **Custom word input** (NEW)  
✅ AI hints with probability scores  
✅ AI auto-play mode  
✅ Beautiful gradient UI  
✅ Win/loss tracking  

## 🐛 Troubleshooting

### Flask Server Won't Start
```bash
# Install Flask
pip3 install flask flask-cors

# Check if port 5001 is free
lsof -i :5001
```

### React Won't Start
```bash
# Install dependencies
cd hangman-web
npm install

# If port 3000 is in use
lsof -ti:3000 | xargs kill -9
```

### Cannot Connect to Backend
- Ensure Flask is running on port 5001
- Check browser console for errors
- Verify CORS is enabled in app.py

## 📊 API Endpoints

All endpoints are on `http://localhost:5001/api/`

- `POST /init` - Initialize oracle
- `POST /new-game` - Start game (supports `mode: 'random'` or `mode: 'custom'` with `word`)
- `POST /guess` - Make a letter guess
- `GET /ai-hint` - Get AI suggestions
- `POST /ai-play` - AI makes a move
- `GET /game-state` - Get current state

## 🎯 Example: Custom Word via API

```bash
curl -X POST http://localhost:5001/api/new-game \
  -H "Content-Type: application/json" \
  -d '{"mode": "custom", "word": "python"}'
```

Response:
```json
{
  "success": true,
  "word_length": 6,
  "pattern": "______",
  "lives": 6
}
```

## 🎨 UI Updates

### New Components
- **Custom Word Input Modal**: Beautiful input form with validation
- **Two Game Mode Buttons**: "Random Word" and "Custom Word"
- **Input Validation**: Only accepts letters, shows error messages

### Styling
- Gradient background for input modal
- Focus effects on input field
- Responsive button layout
- Error message display

## 💡 Tips

1. **For Testing**: Use custom words to test specific scenarios
2. **For Demo**: Show both random and custom modes
3. **For AI Testing**: Use custom words to see how AI performs on specific patterns
4. **For Fun**: Challenge friends with difficult words!

## 📚 Documentation

- `WEB_APP_README.md` - Complete documentation
- `QUICK_START_WEB.md` - Quick start guide
- `DELIVERABLES.md` - Project deliverables

---

**Enjoy playing Hangman! 🎮**
