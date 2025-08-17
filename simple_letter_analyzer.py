import matplotlib.pyplot as plt
from collections import Counter

def count_letters(text):
    """Count how many times each letter appears in the text"""
    letter_count = {}
    
    # Go through each character in the text
    for char in text.lower():
        # Only count letters (a-z)
        if char.isalpha():
            if char in letter_count:
                letter_count[char] += 1
            else:
                letter_count[char] = 1
    
    return letter_count

def count_words(text):
    """Count how many times each word appears in the text"""
    # Split text into words and count them
    words = text.lower().split()
    word_count = Counter(words)
    return word_count

def make_letter_chart(letter_count):
    """Create a simple bar chart of letter frequencies"""
    # Sort letters alphabetically
    letters = sorted(letter_count.keys())
    counts = [letter_count[letter] for letter in letters]
    
    # Create the chart
    plt.figure(figsize=(10, 6))
    plt.bar(letters, counts, color='lightblue')
    plt.title('Letter Frequency in Text')
    plt.xlabel('Letters')
    plt.ylabel('Count')
    
    # Add numbers on top of each bar
    for i, count in enumerate(counts):
        plt.text(i, count + 0.1, str(count), ha='center')
    
    plt.show()

def make_word_chart(word_count, top_n=10):
    """Create a simple bar chart of top word frequencies"""
    # Get the most common words
    most_common = word_count.most_common(top_n)
    words = [item[0] for item in most_common]
    counts = [item[1] for item in most_common]
    
    # Create the chart
    plt.figure(figsize=(12, 6))
    plt.barh(words, counts, color='lightgreen')
    plt.title(f'Top {top_n} Most Common Words')
    plt.xlabel('Count')
    plt.ylabel('Words')
    
    # Add numbers on the right of each bar
    for i, count in enumerate(counts):
        plt.text(count + 0.1, i, str(count), va='center')
    
    plt.show()

def print_summary(text, letter_count, word_count):
    """Print a summary of the analysis"""
    print("\n" + "="*50)
    print("TEXT ANALYSIS SUMMARY")
    print("="*50)
    
    # Basic text info
    print(f"Total characters: {len(text)}")
    print(f"Total words: {len(text.split())}")
    print(f"Total letters: {sum(letter_count.values())}")
    print(f"Unique letters: {len(letter_count)}")
    
    # Most common letter
    if letter_count:
        most_common_letter = max(letter_count, key=letter_count.get)
        print(f"Most common letter: '{most_common_letter}' (appears {letter_count[most_common_letter]} times)")
    
    # Most common word
    if word_count:
        most_common_word = word_count.most_common(1)[0]
        print(f"Most common word: '{most_common_word[0]}' (appears {most_common_word[1]} times)")
    
    print("="*50)

def main():
    """Main function to run the program"""
    print("Welcome to Simple Letter Frequency Analyzer!")
    print("This program counts letters and words in your text.")
    
    # Get text from user
    print("\nEnter your text (or press Enter to use sample text):")
    user_text = input()
    
    # Use sample text if user didn't enter anything
    if not user_text.strip():
        user_text = "The quick brown fox jumps over the lazy dog. This is a sample text for demonstration."
        print(f"\nUsing sample text: {user_text}")
    
    # Analyze the text
    print("\nAnalyzing your text...")
    
    # Count letters and words
    letters = count_letters(user_text)
    words = count_words(user_text)
    
    # Show results
    print_summary(user_text, letters, words)
    
    # Show letter frequencies
    print("\nLetter frequencies:")
    for letter in sorted(letters.keys()):
        print(f"'{letter}': {letters[letter]}")
    
    # Show top word frequencies
    print("\nTop 10 word frequencies:")
    for word, count in words.most_common(10):
        print(f"'{word}': {count}")
    
    # Create charts
    print("\nCreating charts...")
    make_letter_chart(letters)
    make_word_chart(words)
    
    print("\nAnalysis complete! Check the charts above.")

if __name__ == "__main__":
    main()
