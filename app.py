#!/usr/bin/env python3
"""
Flask Backend for Hangman Game
Serves the ML oracle through REST API
"""
from flask import Flask, jsonify, request
from flask_cors import CORS
import sys
import random

sys.path.insert(0, 'src')
from hangman_oracle import HangmanOracle

app = Flask(__name__)
CORS(app)

# Global state
oracle = None
test_words = []
game_state = {}


def load_words(filepath):
    """Load words from file"""
    with open(filepath, 'r') as f:
        return [line.strip().lower() for line in f if line.strip()]


@app.route('/api/init', methods=['POST'])
def initialize():
    """Initialize the oracle with corpus"""
    global oracle, test_words
    
    try:
        corpus_words = load_words('Data/corpus.txt')
        test_words = load_words('Data/test.txt')
        oracle = HangmanOracle(corpus_words)
        
        return jsonify({
            'success': True,
            'corpus_size': len(corpus_words),
            'test_size': len(test_words)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/new-game', methods=['POST'])
def new_game():
    """Start a new game"""
    global game_state, test_words
    
    if not oracle:
        return jsonify({'error': 'Oracle not initialized'}), 400
    
    data = request.json
    mode = data.get('mode', 'random')  # 'random' or 'custom'
    
    if mode == 'custom':
        word = data.get('word', '').lower()
        if not word or not word.isalpha():
            return jsonify({'error': 'Invalid word'}), 400
    else:
        word = random.choice(test_words)
    
    game_state = {
        'target_word': word,
        'guessed': set(),
        'pattern': ['_'] * len(word),
        'lives': 6,
        'wrong_guesses': 0,
        'game_over': False,
        'won': False,
        'history': []
    }
    
    return jsonify({
        'success': True,
        'word_length': len(word),
        'pattern': ''.join(game_state['pattern']),
        'lives': game_state['lives']
    })


@app.route('/api/guess', methods=['POST'])
def make_guess():
    """Make a guess (player or AI)"""
    global game_state
    
    if not game_state:
        return jsonify({'error': 'No active game'}), 400
    
    if game_state['game_over']:
        return jsonify({'error': 'Game is over'}), 400
    
    data = request.json
    letter = data.get('letter', '').lower()
    
    if not letter or len(letter) != 1 or not letter.isalpha():
        return jsonify({'error': 'Invalid letter'}), 400
    
    if letter in game_state['guessed']:
        return jsonify({'error': 'Letter already guessed'}), 400
    
    game_state['guessed'].add(letter)
    target = game_state['target_word']
    is_correct = letter in target
    
    if is_correct:
        # Reveal all occurrences
        for i, ch in enumerate(target):
            if ch == letter:
                game_state['pattern'][i] = letter
    else:
        game_state['wrong_guesses'] += 1
        game_state['lives'] -= 1
    
    # Add to history
    game_state['history'].append({
        'letter': letter,
        'correct': is_correct
    })
    
    # Check win/loss
    if '_' not in game_state['pattern']:
        game_state['game_over'] = True
        game_state['won'] = True
    elif game_state['lives'] <= 0:
        game_state['game_over'] = True
        game_state['won'] = False
    
    return jsonify({
        'success': True,
        'letter': letter,
        'correct': is_correct,
        'pattern': ''.join(game_state['pattern']),
        'lives': game_state['lives'],
        'guessed': list(game_state['guessed']),
        'game_over': game_state['game_over'],
        'won': game_state['won'],
        'target_word': target if game_state['game_over'] else None
    })


@app.route('/api/ai-hint', methods=['GET'])
def ai_hint():
    """Get AI suggestion for next letter"""
    global game_state
    
    if not game_state or not oracle:
        return jsonify({'error': 'No active game or oracle not initialized'}), 400
    
    if game_state['game_over']:
        return jsonify({'error': 'Game is over'}), 400
    
    pattern = ''.join(game_state['pattern'])
    guessed = game_state['guessed']
    
    # Get probabilities from oracle
    probs = oracle.get_letter_probabilities(pattern, guessed)
    
    # Get top 5 suggestions
    top_indices = probs.argsort()[-5:][::-1]
    suggestions = []
    for idx in top_indices:
        letter = chr(97 + idx)
        prob = float(probs[idx])
        if prob > 0:
            suggestions.append({
                'letter': letter,
                'probability': prob
            })
    
    return jsonify({
        'success': True,
        'suggestions': suggestions,
        'best_guess': suggestions[0]['letter'] if suggestions else None
    })


@app.route('/api/ai-play', methods=['POST'])
def ai_play():
    """Let AI make the next move"""
    global game_state
    
    if not game_state or not oracle:
        return jsonify({'error': 'No active game or oracle not initialized'}), 400
    
    if game_state['game_over']:
        return jsonify({'error': 'Game is over'}), 400
    
    pattern = ''.join(game_state['pattern'])
    guessed = game_state['guessed']
    
    # Get AI's guess
    letter = oracle.guess_letter(pattern, guessed)
    
    # Make the guess
    return make_guess_internal(letter)


def make_guess_internal(letter):
    """Internal function to make a guess"""
    global game_state
    
    if letter in game_state['guessed']:
        # AI shouldn't guess repeated letters, but handle it
        return jsonify({'error': 'Letter already guessed'}), 400
    
    game_state['guessed'].add(letter)
    target = game_state['target_word']
    is_correct = letter in target
    
    if is_correct:
        for i, ch in enumerate(target):
            if ch == letter:
                game_state['pattern'][i] = letter
    else:
        game_state['wrong_guesses'] += 1
        game_state['lives'] -= 1
    
    game_state['history'].append({
        'letter': letter,
        'correct': is_correct
    })
    
    if '_' not in game_state['pattern']:
        game_state['game_over'] = True
        game_state['won'] = True
    elif game_state['lives'] <= 0:
        game_state['game_over'] = True
        game_state['won'] = False
    
    return jsonify({
        'success': True,
        'letter': letter,
        'correct': is_correct,
        'pattern': ''.join(game_state['pattern']),
        'lives': game_state['lives'],
        'guessed': list(game_state['guessed']),
        'game_over': game_state['game_over'],
        'won': game_state['won'],
        'target_word': target if game_state['game_over'] else None
    })


@app.route('/api/game-state', methods=['GET'])
def get_game_state():
    """Get current game state"""
    if not game_state:
        return jsonify({'error': 'No active game'}), 400
    
    return jsonify({
        'pattern': ''.join(game_state['pattern']),
        'lives': game_state['lives'],
        'guessed': list(game_state['guessed']),
        'game_over': game_state['game_over'],
        'won': game_state['won'],
        'target_word': game_state['target_word'] if game_state['game_over'] else None,
        'history': game_state['history']
    })


if __name__ == '__main__':
    print("Initializing Hangman Oracle...")
    try:
        corpus_words = load_words('Data/corpus.txt')
        test_words = load_words('Data/test.txt')
        oracle = HangmanOracle(corpus_words)
        print(f"✓ Oracle initialized with {len(corpus_words)} corpus words")
        print(f"✓ Loaded {len(test_words)} test words")
    except Exception as e:
        print(f"✗ Failed to initialize: {e}")
    
    print("\nStarting Flask server on http://localhost:5001")
    app.run(debug=True, port=5001)
