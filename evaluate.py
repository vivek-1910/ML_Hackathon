#!/usr/bin/env python3
"""
Hangman Evaluation Script
Best Model: 42.5% Win Rate on Test Set
"""
import sys
from typing import List, Set

# Add src to path
sys.path.insert(0, 'src')

from hangman_oracle import HangmanOracle


def load_words(filepath: str) -> List[str]:
    """Load words from file"""
    with open(filepath, 'r') as f:
        return [line.strip().lower() for line in f if line.strip()]


def play_game(oracle: HangmanOracle, target_word: str, max_lives: int = 6) -> dict:
    """
    Play a single game of Hangman.
    
    Returns:
        dict with keys: won, wrong_guesses, repeated_guesses
    """
    target = target_word.lower()
    lives = max_lives
    guessed = set()
    mask = ['_'] * len(target)
    wrong_guesses = 0
    repeated_guesses = 0
    
    while lives > 0 and '_' in mask:
        pattern = ''.join(mask)
        guess = oracle.guess_letter(pattern, guessed)
        
        if guess in guessed:
            repeated_guesses += 1
            continue
        
        guessed.add(guess)
        
        if guess in target:
            # Reveal all occurrences
            for i, ch in enumerate(target):
                if ch == guess:
                    mask[i] = guess
        else:
            wrong_guesses += 1
            lives -= 1
    
    won = '_' not in mask
    return {
        'won': won,
        'wrong_guesses': wrong_guesses,
        'repeated_guesses': repeated_guesses
    }


def evaluate(corpus_file: str, test_file: str, n_games: int = 2000):
    """
    Evaluate the oracle on test set.
    
    Scoring formula:
    Final Score = (Success Rate * n_games) - (Total Wrong * 5) - (Total Repeated * 2)
    """
    print("Loading corpus...")
    corpus_words = load_words(corpus_file)
    print(f"Loaded {len(corpus_words)} words from corpus")
    
    print("\nBuilding oracle (this may take a minute)...")
    oracle = HangmanOracle(corpus_words)
    print("Oracle ready!")
    
    print(f"\nLoading test set...")
    test_words = load_words(test_file)
    print(f"Loaded {len(test_words)} test words")
    
    print(f"\nPlaying {n_games} games...")
    wins = 0
    total_wrong = 0
    total_repeated = 0
    
    for i in range(n_games):
        target = test_words[i % len(test_words)]
        result = play_game(oracle, target)
        
        if result['won']:
            wins += 1
        total_wrong += result['wrong_guesses']
        total_repeated += result['repeated_guesses']
        
        if (i + 1) % 100 == 0:
            print(f"  Progress: {i+1}/{n_games} games ({wins}/{i+1} wins, {wins/(i+1)*100:.1f}%)")
    
    # Calculate metrics
    success_rate = wins / n_games
    final_score = (success_rate * n_games) - (total_wrong * 5) - (total_repeated * 2)
    
    # Print results
    print("\n" + "="*60)
    print("EVALUATION RESULTS")
    print("="*60)
    print(f"Games Played: {n_games}")
    print(f"Wins: {wins} ({success_rate*100:.2f}%)")
    print(f"Losses: {n_games - wins}")
    print(f"Total Wrong Guesses: {total_wrong}")
    print(f"Total Repeated Guesses: {total_repeated}")
    print(f"Average Wrong per Game: {total_wrong/n_games:.2f}")
    print(f"\nFINAL SCORE: {final_score:.2f}")
    print("="*60)
    
    return {
        'wins': wins,
        'success_rate': success_rate,
        'total_wrong': total_wrong,
        'total_repeated': total_repeated,
        'final_score': final_score
    }


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Evaluate Hangman Oracle')
    parser.add_argument('--corpus', default='Data/corpus.txt', help='Path to corpus file')
    parser.add_argument('--test', default='Data/test.txt', help='Path to test file')
    parser.add_argument('--n_games', type=int, default=2000, help='Number of games to play')
    
    args = parser.parse_args()
    
    evaluate(args.corpus, args.test, args.n_games)
