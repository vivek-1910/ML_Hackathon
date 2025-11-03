import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { 
  Heart, 
  Lightbulb, 
  Bot, 
  RefreshCw, 
  Trophy,
  XCircle,
  Sparkles,
  Brain,
  Edit3
} from 'lucide-react';
import './App.css';

const HANGMAN_STAGES = [
  // Stage 0 - Full lives
  `
   ___
  |   |
  |
  |
  |
  |___
  `,
  // Stage 1
  `
   ___
  |   |
  |   O
  |
  |
  |___
  `,
  // Stage 2
  `
   ___
  |   |
  |   O
  |   |
  |
  |___
  `,
  // Stage 3
  `
   ___
  |   |
  |   O
  |  /|
  |
  |___
  `,
  // Stage 4
  `
   ___
  |   |
  |   O
  |  /|\\
  |
  |___
  `,
  // Stage 5
  `
   ___
  |   |
  |   O
  |  /|\\
  |  /
  |___
  `,
  // Stage 6 - Game Over
  `
   ___
  |   |
  |   O
  |  /|\\
  |  / \\
  |___
  `
];

function App() {
  const [gameState, setGameState] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [aiSuggestions, setAiSuggestions] = useState([]);
  const [showHint, setShowHint] = useState(false);
  const [message, setMessage] = useState('');
  const [autoPlay, setAutoPlay] = useState(false);
  const [showCustomWordInput, setShowCustomWordInput] = useState(false);
  const [customWord, setCustomWord] = useState('');

  useEffect(() => {
    initializeGame();
  }, []);

  useEffect(() => {
    if (autoPlay && gameState && !gameState.game_over) {
      const timer = setTimeout(() => {
        handleAIPlay();
      }, 1000);
      return () => clearTimeout(timer);
    }
  }, [autoPlay, gameState]);

  const initializeGame = async () => {
    try {
      setLoading(true);
      await axios.post('/api/init');
      await startNewGame();
      setLoading(false);
    } catch (err) {
      setError('Failed to initialize game. Make sure the Flask server is running.');
      setLoading(false);
    }
  };

  const startNewGame = async (mode = 'random', word = '') => {
    try {
      const payload = mode === 'custom' ? { mode: 'custom', word } : { mode: 'random' };
      const response = await axios.post('/api/new-game', payload);
      setGameState({
        pattern: response.data.pattern,
        lives: response.data.lives,
        guessed: [],
        game_over: false,
        won: false,
        target_word: null
      });
      setMessage('');
      setShowHint(false);
      setAiSuggestions([]);
      setAutoPlay(false);
      setShowCustomWordInput(false);
      setCustomWord('');
    } catch (err) {
      setMessage(err.response?.data?.error || 'Failed to start new game');
    }
  };

  const handleCustomWordSubmit = () => {
    if (!customWord || !customWord.trim()) {
      setMessage('Please enter a word');
      return;
    }
    if (!/^[a-zA-Z]+$/.test(customWord)) {
      setMessage('Word must contain only letters');
      return;
    }
    startNewGame('custom', customWord.toLowerCase());
  };

  const handleGuess = async (letter) => {
    if (!gameState || gameState.game_over || gameState.guessed.includes(letter)) {
      return;
    }

    try {
      const response = await axios.post('/api/guess', { letter });
      setGameState({
        pattern: response.data.pattern,
        lives: response.data.lives,
        guessed: response.data.guessed,
        game_over: response.data.game_over,
        won: response.data.won,
        target_word: response.data.target_word
      });

      if (response.data.correct) {
        setMessage(`✓ Great! "${letter.toUpperCase()}" is in the word!`);
      } else {
        setMessage(`✗ Sorry, "${letter.toUpperCase()}" is not in the word.`);
      }

      setShowHint(false);
      setAiSuggestions([]);
    } catch (err) {
      setMessage(err.response?.data?.error || 'Failed to make guess');
    }
  };

  const handleAIHint = async () => {
    try {
      const response = await axios.get('/api/ai-hint');
      setAiSuggestions(response.data.suggestions);
      setShowHint(true);
    } catch (err) {
      setMessage('Failed to get AI hint');
    }
  };

  const handleAIPlay = async () => {
    if (!gameState || gameState.game_over) return;

    try {
      const response = await axios.post('/api/ai-play');
      setGameState({
        pattern: response.data.pattern,
        lives: response.data.lives,
        guessed: response.data.guessed,
        game_over: response.data.game_over,
        won: response.data.won,
        target_word: response.data.target_word
      });

      if (response.data.correct) {
        setMessage(`🤖 AI guessed "${response.data.letter.toUpperCase()}" - Correct!`);
      } else {
        setMessage(`🤖 AI guessed "${response.data.letter.toUpperCase()}" - Wrong!`);
      }

      setShowHint(false);
      setAiSuggestions([]);
    } catch (err) {
      setMessage('Failed to let AI play');
      setAutoPlay(false);
    }
  };

  const renderKeyboard = () => {
    const rows = [
      'qwertyuiop'.split(''),
      'asdfghjkl'.split(''),
      'zxcvbnm'.split('')
    ];

    return (
      <div className="keyboard">
        {rows.map((row, rowIndex) => (
          <div key={rowIndex} className="keyboard-row">
            {row.map(letter => {
              const isGuessed = gameState?.guessed.includes(letter);
              const isCorrect = gameState?.pattern.includes(letter);
              const isWrong = isGuessed && !isCorrect;
              
              return (
                <button
                  key={letter}
                  className={`key ${isGuessed ? (isCorrect ? 'correct' : 'wrong') : ''}`}
                  onClick={() => handleGuess(letter)}
                  disabled={!gameState || gameState.game_over || isGuessed}
                >
                  {letter.toUpperCase()}
                </button>
              );
            })}
          </div>
        ))}
      </div>
    );
  };

  if (loading) {
    return (
      <div className="app">
        <div className="loading">
          <Brain className="loading-icon" size={48} />
          <p>Loading AI Oracle...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="app">
        <div className="error">
          <XCircle size={48} />
          <p>{error}</p>
          <button onClick={initializeGame} className="btn-primary">
            Retry
          </button>
        </div>
      </div>
    );
  }

  const wrongGuesses = 6 - (gameState?.lives || 6);

  return (
    <div className="app">
      <div className="container">
        <header className="header">
          <div className="title">
            <Sparkles className="icon" />
            <h1>Hangman ML</h1>
          </div>
          <p className="subtitle">Powered by 42% Win Rate AI Oracle</p>
        </header>

        <div className="game-content">
          <div className="left-panel">
            <div className="hangman-display">
              <pre>{HANGMAN_STAGES[wrongGuesses]}</pre>
            </div>

            <div className="stats">
              <div className="stat">
                <Heart className="stat-icon" />
                <span>{gameState?.lives || 6} Lives</span>
              </div>
              <div className="stat">
                <span>Guessed: {gameState?.guessed.length || 0}</span>
              </div>
            </div>
          </div>

          <div className="right-panel">
            <div className="word-display">
              {gameState?.pattern.split('').map((char, idx) => (
                <div key={idx} className="letter-box">
                  {char === '_' ? '' : char.toUpperCase()}
                </div>
              ))}
            </div>

            {message && (
              <div className={`message ${message.includes('✓') || message.includes('Correct') ? 'success' : 'error'}`}>
                {message}
              </div>
            )}

            {gameState?.game_over && (
              <div className={`game-over ${gameState.won ? 'won' : 'lost'}`}>
                {gameState.won ? (
                  <>
                    <Trophy size={48} />
                    <h2>You Won!</h2>
                    <p>The word was: <strong>{gameState.target_word?.toUpperCase()}</strong></p>
                  </>
                ) : (
                  <>
                    <XCircle size={48} />
                    <h2>Game Over</h2>
                    <p>The word was: <strong>{gameState.target_word?.toUpperCase()}</strong></p>
                  </>
                )}
              </div>
            )}

            {!gameState?.game_over && renderKeyboard()}

            {showHint && aiSuggestions.length > 0 && (
              <div className="ai-hints">
                <h3>AI Suggestions:</h3>
                <div className="suggestions">
                  {aiSuggestions.map((suggestion, idx) => (
                    <div key={idx} className="suggestion">
                      <span className="letter">{suggestion.letter.toUpperCase()}</span>
                      <span className="probability">{(suggestion.probability * 100).toFixed(1)}%</span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {showCustomWordInput && (
              <div className="custom-word-input">
                <h3>Enter Your Word</h3>
                <div className="input-group">
                  <input
                    type="text"
                    value={customWord}
                    onChange={(e) => setCustomWord(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && handleCustomWordSubmit()}
                    placeholder="Type a word (letters only)"
                    autoFocus
                  />
                  <button className="btn-primary" onClick={handleCustomWordSubmit}>
                    Start Game
                  </button>
                  <button className="btn-secondary" onClick={() => {
                    setShowCustomWordInput(false);
                    setCustomWord('');
                  }}>
                    Cancel
                  </button>
                </div>
              </div>
            )}

            <div className="controls">
              <button 
                className="btn-secondary"
                onClick={handleAIHint}
                disabled={!gameState || gameState.game_over}
              >
                <Lightbulb size={20} />
                Get Hint
              </button>

              <button 
                className="btn-secondary"
                onClick={handleAIPlay}
                disabled={!gameState || gameState.game_over}
              >
                <Bot size={20} />
                AI Play
              </button>

              <button 
                className={`btn-secondary ${autoPlay ? 'active' : ''}`}
                onClick={() => setAutoPlay(!autoPlay)}
                disabled={!gameState || gameState.game_over}
              >
                <Bot size={20} />
                {autoPlay ? 'Stop Auto' : 'Auto Play'}
              </button>

              <button 
                className="btn-primary"
                onClick={() => startNewGame()}
              >
                <RefreshCw size={20} />
                Random Word
              </button>

              <button 
                className="btn-primary"
                onClick={() => setShowCustomWordInput(true)}
              >
                <Edit3 size={20} />
                Custom Word
              </button>
            </div>
          </div>
        </div>

        <footer className="footer">
          <p>Built with React + Flask + ML Oracle (4-gram weighted, 42% win rate)</p>
        </footer>
      </div>
    </div>
  );
}

export default App;
