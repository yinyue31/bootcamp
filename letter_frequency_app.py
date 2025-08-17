from flask import Flask, render_template, request, jsonify
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import io
import base64
import numpy as np
from collections import Counter
import re

app = Flask(__name__)

def letter_frequency(text):
    """Calculate letter frequency in text"""
    freq = {}
    for char in text.lower():
        if char.isalpha():  # Only count letters
            freq[char] = freq.get(char, 0) + 1
    return freq

def word_frequency(text):
    """Calculate word frequency in text"""
    words = re.findall(r'\b\w+\b', text.lower())
    return Counter(words)

def create_frequency_plot(freq, plot_type='letter'):
    """Create a matplotlib plot and return as base64 string"""
    plt.figure(figsize=(10, 6))
    
    if plot_type == 'letter':
        letters = sorted(freq.keys())
        counts = [freq[l] for l in letters]
        plt.bar(letters, counts, color='skyblue', alpha=0.7)
        plt.xlabel('Letter')
        plt.ylabel('Frequency')
        plt.title('Letter Frequency Distribution')
        
        # Add value labels on bars
        for i, v in enumerate(counts):
            plt.text(i, v + 0.1, str(v), ha='center', va='bottom')
            
    elif plot_type == 'word':
        # Get top 20 words
        top_words = dict(sorted(freq.items(), key=lambda x: x[1], reverse=True)[:20])
        words = list(top_words.keys())
        counts = list(top_words.values())
        
        plt.barh(words, counts, color='lightcoral', alpha=0.7)
        plt.xlabel('Frequency')
        plt.ylabel('Word')
        plt.title('Top 20 Word Frequencies')
        
        # Add value labels on bars
        for i, v in enumerate(counts):
            plt.text(v + 0.1, i, str(v), ha='left', va='center')
    
    plt.tight_layout()
    
    # Convert plot to base64 string
    img = io.BytesIO()
    plt.savefig(img, format='png', dpi=100, bbox_inches='tight')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    
    return plot_url

def calculate_statistics(freq):
    """Calculate statistical measures for frequency data"""
    if not freq:
        return {}
    
    counts = list(freq.values())
    total = sum(counts)
    
    stats = {
        'total_count': total,
        'unique_items': len(freq),
        'mean': np.mean(counts),
        'median': np.median(counts),
        'std_dev': np.std(counts),
        'min_freq': min(counts),
        'max_freq': max(counts),
        'most_common': max(freq.items(), key=lambda x: x[1])
    }
    
    return stats

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_text():
    data = request.json
    text = data.get('text', '')
    
    if not text.strip():
        return jsonify({'error': 'Please enter some text to analyze'})
    
    # Calculate frequencies
    letter_freq = letter_frequency(text)
    word_freq = word_frequency(text)
    
    # Create plots
    letter_plot = create_frequency_plot(letter_freq, 'letter')
    word_plot = create_frequency_plot(word_freq, 'word')
    
    # Calculate statistics
    letter_stats = calculate_statistics(letter_freq)
    word_stats = calculate_statistics(word_freq)
    
    # Prepare response
    response = {
        'letter_frequency': letter_freq,
        'word_frequency': dict(list(word_freq.items())[:50]),  # Top 50 words
        'letter_plot': letter_plot,
        'word_plot': word_plot,
        'letter_statistics': letter_stats,
        'word_statistics': word_stats,
        'text_length': len(text),
        'word_count': len(text.split()),
        'character_count': len([c for c in text if c.isalpha()])
    }
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
