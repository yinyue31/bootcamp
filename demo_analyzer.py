import matplotlib.pyplot as plt
from collections import Counter

def count_letters(text):
    """Count how many times each letter appears in the text"""
    letter_count = {}
    
    for char in text.lower():
        if char.isalpha():
            if char in letter_count:
                letter_count[char] += 1
            else:
                letter_count[char] = 1
    
    return letter_count

def count_words(text):
    """Count how many times each word appears in the text"""
    words = text.lower().split()
    word_count = Counter(words)
    return word_count

def make_letter_chart(letter_count, text):
    """Create a simple bar chart of letter frequencies"""
    letters = sorted(letter_count.keys())
    counts = [letter_count[letter] for letter in letters]
    
    plt.figure(figsize=(10, 6))
    plt.bar(letters, counts, color='lightblue')
    plt.title(f'Letter Frequency in "{text}"')
    plt.xlabel('Letters')
    plt.ylabel('Count')
    
    # Add numbers on top of each bar
    for i, count in enumerate(counts):
        plt.text(i, count + 0.1, str(count), ha='center')
    
    plt.show()

def main():
    """Analyze text input from user"""
    print("="*60)
    print("LETTER FREQUENCY ANALYZER")
    print("="*60)
    
    # Get text from user
    print("Enter your text to analyze:")
    text = input("> ")
    
    # Check if user entered something
    if not text.strip():
        print("No text entered. Using sample text instead.")
        text = "hello world"
    
    print(f"\nAnalyzing text: '{text}'")
    print()
    
    # Count letters and words
    letters = count_letters(text)
    words = count_words(text)
    
    # Show results
    print("LETTER COUNT:")
    for letter in sorted(letters.keys()):
        print(f"  '{letter}': {letters[letter]}")
    
    print()
    print("WORD COUNT:")
    for word, count in words.items():
        print(f"  '{word}': {count}")
    
    print()
    print("SUMMARY:")
    print(f"  Total characters: {len(text)}")
    print(f"  Total words: {len(text.split())}")
    print(f"  Total letters: {sum(letters.values())}")
    print(f"  Unique letters: {len(letters)}")
    
    if letters:
        most_common_letter = max(letters, key=letters.get)
        print(f"  Most common letter: '{most_common_letter}' (appears {letters[most_common_letter]} times)")
    
    print()
    print("Creating chart...")
    make_letter_chart(letters, text)
    
    print("Analysis complete! Check the chart above.")

if __name__ == "__main__":
    main()
