#!/usr/bin/env python3
# Simple Letter Frequency Analyzer - No external libraries needed

def count_letters(text):
    """Count frequency of each letter in text"""
    freq = {}
    for char in text.lower():
        if char.isalpha():  # Only count letters a-z
            freq[char] = freq.get(char, 0) + 1
    return freq

def count_words(text):
    """Count frequency of each word in text"""
    words = text.lower().split()
    freq = {}
    for word in words:
        freq[word] = freq.get(word, 0) + 1
    return freq

def create_ascii_chart(data, title, max_width=50):
    """Create simple ASCII bar chart"""
    if not data:
        return "No data to chart"
    
    print(f"\n{title}")
    print("-" * len(title))
    
    # Find maximum value for scaling
    max_val = max(data.values())
    
    for item in sorted(data.keys()):
        count = data[item]
        # Create bar using # characters, scaled to max_width
        bar_length = int((count / max_val) * max_width) if max_val > 0 else 0
        bar = "#" * bar_length
        print(f"{item:2} | {bar} {count}")

def print_results(text, letters, words):
    """Display analysis results"""
    print("=" * 50)
    print("LETTER FREQUENCY ANALYSIS")
    print("=" * 50)
    print(f"Text: '{text}'")
    print(f"Total characters: {len(text)}")
    print(f"Total words: {len(text.split())}")
    print(f"Total letters: {sum(letters.values())}")
    print(f"Unique letters: {len(letters)}")
    
    # Show letter counts
    print("\nLetter frequencies:")
    for letter in sorted(letters.keys()):
        print(f"  '{letter}': {letters[letter]}")
    
    # Show word counts
    print("\nWord frequencies:")
    for word in sorted(words.keys()):
        print(f"  '{word}': {words[word]}")
    
    # Find most common letter
    if letters:
        most_common = max(letters, key=letters.get)
        print(f"\nMost common letter: '{most_common}' ({letters[most_common]} times)")
    
    # Create ASCII charts
    create_ascii_chart(letters, "LETTER FREQUENCY CHART")
    create_ascii_chart(words, "WORD FREQUENCY CHART")

def main():
    """Main program - get input and analyze"""
    print("Enter text to analyze (or press Enter for sample):")
    text = input("> ").strip()
    
    if not text:  # Use sample text if nothing entered
        text = "hello world"
        print(f"Using sample: '{text}'")
    
    # Analyze the text
    letters = count_letters(text)
    words = count_words(text)
    
    # Show results
    print_results(text, letters, words)

if __name__ == "__main__":
    main()
