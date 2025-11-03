# Hangman Web Frontend

Beautiful React application for playing Hangman with AI assistance.

## Features

### 🎮 Interactive Gameplay
- Virtual keyboard with color-coded feedback (green = correct, red = wrong)
- Real-time hangman ASCII art visualization
- Live pattern display with letter boxes
- Lives counter with heart icon

### 🤖 AI Assistance
- **Get Hint**: Shows top 5 AI predictions with probability percentages
- **AI Play**: Let AI make a single guess
- **Auto Play**: Watch AI play the entire game automatically

### 🎨 Modern UI
- Beautiful purple gradient background
- Smooth animations and transitions
- Responsive design (works on mobile)
- Clean, intuitive interface

## Tech Stack

- **React 18** - Modern UI framework
- **Axios** - HTTP client for API calls
- **Lucide React** - Beautiful icon library
- **CSS3** - Custom styling with gradients

## Installation

```bash
npm install
```

## Development

```bash
npm start
```

Runs on http://localhost:3000

## Build for Production

```bash
npm run build
```

Creates optimized build in `build/` directory.

## Project Structure

```
src/
├── App.js          # Main game component
├── App.css         # Styles
├── index.js        # React entry point
└── index.css       # Global styles

public/
└── index.html      # HTML template
```

## API Integration

The app connects to Flask backend on http://localhost:5001

### Endpoints Used:
- `POST /api/init` - Initialize game
- `POST /api/new-game` - Start new game
- `POST /api/guess` - Make a guess
- `GET /api/ai-hint` - Get AI suggestions
- `POST /api/ai-play` - AI makes a move

## Game Flow

1. **Initialization**: Loads corpus and initializes ML oracle
2. **New Game**: Fetches random word from test set
3. **Gameplay**: 
   - User clicks letters on keyboard
   - Backend validates guess
   - Frontend updates pattern and lives
4. **AI Hints**: Fetches probability distribution from oracle
5. **Game Over**: Shows win/loss message with target word

## Components

### Main App Component
- Manages game state
- Handles user interactions
- Communicates with backend API
- Renders UI elements

### Key State Variables
- `gameState` - Current game status (pattern, lives, guessed letters)
- `aiSuggestions` - AI hint data
- `showHint` - Toggle hint display
- `autoPlay` - Auto-play mode flag
- `message` - Feedback messages

## Styling

Uses custom CSS with:
- CSS Grid for layout
- Flexbox for components
- Linear gradients
- Smooth transitions
- Responsive breakpoints

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## License

MIT
