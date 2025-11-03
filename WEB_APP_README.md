# Hangman Web Application

A beautiful, modern web interface for playing Hangman powered by a 42% win-rate ML oracle.

## Features

- 🎮 **Interactive Gameplay** - Click letters on the virtual keyboard to guess
- 🤖 **AI Assistance** - Get hints from the ML oracle showing top letter predictions with probabilities
- 🎯 **AI Auto-Play** - Watch the AI play the game automatically
- 🎨 **Modern UI** - Beautiful gradient design with smooth animations
- 📊 **Real-time Stats** - Track lives, guessed letters, and game progress
- 🏆 **Win/Loss Tracking** - Clear visual feedback on game outcomes

## Architecture

### Backend (Flask)
- **File**: `app.py`
- **Port**: 5001
- **Endpoints**:
  - `POST /api/init` - Initialize the ML oracle
  - `POST /api/new-game` - Start a new game
  - `POST /api/guess` - Make a letter guess
  - `GET /api/ai-hint` - Get AI suggestions
  - `POST /api/ai-play` - Let AI make the next move
  - `GET /api/game-state` - Get current game state

### Frontend (React)
- **Directory**: `hangman-web/`
- **Port**: 3000 (development)
- **Features**:
  - Virtual keyboard with color-coded feedback
  - Hangman ASCII art visualization
  - AI hint system with probability display
  - Auto-play mode
  - Responsive design

## Installation

### Prerequisites
- Python 3.7+
- Node.js 14+ and npm
- pip

### Step 1: Install Python Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- numpy
- flask
- flask-cors
- (and other ML dependencies)

### Step 2: Install React Dependencies

```bash
cd hangman-web
npm install
```

This installs:
- react
- react-dom
- axios
- lucide-react (for icons)

## Running the Application

You need to run both the backend and frontend servers.

### Terminal 1: Start Flask Backend

```bash
# From the ML_hack directory
python app.py
```

The backend will:
1. Load the corpus (50k words)
2. Initialize the ML oracle
3. Start the Flask server on http://localhost:5001

You should see:
```
✓ Oracle initialized with 50000 corpus words
✓ Loaded 2000 test words
Starting Flask server on http://localhost:5001
```

### Terminal 2: Start React Frontend

```bash
# From the ML_hack/hangman-web directory
cd hangman-web
npm start
```

The frontend will:
1. Start the React development server
2. Automatically open http://localhost:3000 in your browser

## How to Play

### Manual Mode
1. Click **New Game** to start
2. Click letters on the keyboard to make guesses
3. Green = correct letter, Red = wrong letter
4. Try to guess the word before running out of lives (6 wrong guesses)

### AI Assistance Mode
1. Click **Get Hint** to see AI's top 5 letter suggestions with probabilities
2. Click **AI Play** to let the AI make one guess
3. Click **Auto Play** to watch the AI play the entire game automatically

## Game Rules

- **Lives**: 6 (standard Hangman rules)
- **Scoring**: 
  - Win: Guess the word before lives run out
  - Loss: Run out of lives
- **Letters**: 26 letters (a-z)
- **Words**: Random selection from 2000 test words

## API Usage Examples

### Start a New Game
```bash
curl -X POST http://localhost:5001/api/new-game \
  -H "Content-Type: application/json" \
  -d '{"mode": "random"}'
```

Response:
```json
{
  "success": true,
  "word_length": 7,
  "pattern": "_______",
  "lives": 6
}
```

### Make a Guess
```bash
curl -X POST http://localhost:5001/api/guess \
  -H "Content-Type: application/json" \
  -d '{"letter": "e"}'
```

Response:
```json
{
  "success": true,
  "letter": "e",
  "correct": true,
  "pattern": "_e___e_",
  "lives": 6,
  "guessed": ["e"],
  "game_over": false,
  "won": false
}
```

### Get AI Hint
```bash
curl http://localhost:5001/api/ai-hint
```

Response:
```json
{
  "success": true,
  "suggestions": [
    {"letter": "e", "probability": 0.234},
    {"letter": "a", "probability": 0.189},
    {"letter": "t", "probability": 0.156},
    {"letter": "o", "probability": 0.123},
    {"letter": "i", "probability": 0.098}
  ],
  "best_guess": "e"
}
```

## Project Structure

```
ML_hack/
├── app.py                      # Flask backend server
├── src/
│   └── hangman_oracle.py       # ML oracle (42% win rate)
├── Data/
│   ├── corpus.txt              # Training corpus (50k words)
│   └── test.txt                # Test words (2k words)
├── hangman-web/                # React frontend
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── App.js              # Main React component
│   │   ├── App.css             # Styles
│   │   ├── index.js            # React entry point
│   │   └── index.css           # Global styles
│   ├── package.json            # npm dependencies
│   └── .gitignore
├── requirements.txt            # Python dependencies
└── WEB_APP_README.md          # This file
```

## Technologies Used

### Backend
- **Flask** - Lightweight Python web framework
- **Flask-CORS** - Cross-Origin Resource Sharing support
- **NumPy** - Numerical computations for ML oracle
- **Custom ML Oracle** - 4-gram weighted probabilistic model

### Frontend
- **React 18** - Modern UI framework
- **Axios** - HTTP client for API calls
- **Lucide React** - Beautiful icon library
- **CSS3** - Custom styling with gradients and animations

## ML Oracle Details

The AI uses an advanced multi-signal strategy:
- **4-gram context** (weight=30) - Highest priority
- **Trigram context** (weight=16)
- **Positional patterns** (weight=10)
- **Length-specific frequencies** (weight=5)
- **Bigram context** (weight=6)
- **Strategic vowel/early-game boosting**

**Performance**: 42% win rate on test set with 0% corpus overlap

## Troubleshooting

### Backend Issues

**Problem**: `ModuleNotFoundError: No module named 'flask'`
```bash
pip install flask flask-cors
```

**Problem**: `FileNotFoundError: Data/corpus.txt`
```bash
# Make sure you're running app.py from the ML_hack directory
cd /path/to/ML_hack
python app.py
```

### Frontend Issues

**Problem**: `Cannot connect to backend`
- Make sure Flask server is running on port 5001
- Check that CORS is enabled in app.py

**Problem**: `npm: command not found`
- Install Node.js from https://nodejs.org/

**Problem**: Port 3000 already in use
```bash
# Kill the process using port 3000
lsof -ti:3000 | xargs kill -9
# Or use a different port
PORT=3001 npm start
```

## Development

### Hot Reload
Both servers support hot reload:
- **Flask**: Runs in debug mode, auto-reloads on Python file changes
- **React**: Auto-reloads on JS/CSS file changes

### Building for Production

```bash
cd hangman-web
npm run build
```

This creates an optimized production build in `hangman-web/build/`

To serve the production build with Flask, update `app.py`:
```python
from flask import send_from_directory

@app.route('/')
def serve_frontend():
    return send_from_directory('hangman-web/build', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('hangman-web/build', path)
```

## Future Enhancements

- [ ] Multiplayer mode
- [ ] Difficulty levels (word length selection)
- [ ] Custom word input
- [ ] Statistics dashboard (win rate, average guesses)
- [ ] Leaderboard
- [ ] Sound effects
- [ ] Dark mode
- [ ] Mobile app version

## License

MIT License - Feel free to use and modify.

## Credits

Created for UE23CS352A Machine Learning Hackathon  
ML Oracle: 42% win rate, 4-gram weighted model  
UI Design: Modern gradient with smooth animations
