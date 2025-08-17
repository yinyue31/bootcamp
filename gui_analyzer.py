#!/usr/bin/env python3
# Interactive GUI for Letter Frequency Analyzer with Real Charts
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from simple_analyzer import count_letters, count_words

class AnalyzerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Letter Frequency Analyzer - Interactive Charts")
        self.root.geometry("1000x700")
        
        # Create main frame
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="Letter Frequency Analyzer", font=("Arial", 18, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Left panel for input and controls
        left_panel = ttk.Frame(main_frame)
        left_panel.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Input section
        input_label = ttk.Label(left_panel, text="Enter your text:", font=("Arial", 12, "bold"))
        input_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        self.text_input = tk.Text(left_panel, height=6, width=40)
        self.text_input.grid(row=1, column=0, pady=(0, 10))
        
        # Buttons
        button_frame = ttk.Frame(left_panel)
        button_frame.grid(row=2, column=0, pady=(0, 20))
        
        generate_btn = ttk.Button(button_frame, text="Analyze & Plot", command=self.analyze_and_plot, style="Accent.TButton")
        generate_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        clear_btn = ttk.Button(button_frame, text="Clear All", command=self.clear_all)
        clear_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        exit_btn = ttk.Button(button_frame, text="Exit", command=root.quit)
        exit_btn.pack(side=tk.LEFT)
        
        # Statistics panel
        stats_label = ttk.Label(left_panel, text="Text Statistics:", font=("Arial", 12, "bold"))
        stats_label.grid(row=3, column=0, sticky=tk.W, pady=(0, 5))
        
        self.stats_text = tk.Text(left_panel, height=8, width=40, font=("Courier", 10))
        self.stats_text.grid(row=4, column=0, pady=(0, 10))
        
        # Right panel for charts
        right_panel = ttk.Frame(main_frame)
        right_panel.grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create matplotlib figure with subplots
        self.fig = Figure(figsize=(12, 8))
        self.ax1 = self.fig.add_subplot(2, 1, 1)  # Letter chart
        self.ax2 = self.fig.add_subplot(2, 1, 2)  # Word chart
        
        # Create canvas
        self.canvas = FigureCanvasTkAgg(self.fig, right_panel)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Configure grid weights
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        left_panel.columnconfigure(0, weight=1)
        right_panel.columnconfigure(0, weight=1)
        
        # Initial message
        self.show_welcome_message()
        
    def show_welcome_message(self):
        """Show welcome message in charts"""
        self.ax1.clear()
        self.ax1.text(0.5, 0.5, 'Enter text and click "Analyze & Plot"\nto see interactive charts!', 
                      ha='center', va='center', transform=self.ax1.transAxes, fontsize=14)
        self.ax1.set_title('Letter Frequency Chart', fontsize=14, fontweight='bold')
        self.ax1.axis('off')
        
        self.ax2.clear()
        self.ax2.text(0.5, 0.5, 'Word frequency chart will appear here', 
                      ha='center', va='center', transform=self.ax2.transAxes, fontsize=14)
        self.ax2.set_title('Word Frequency Chart', fontsize=14, fontweight='bold')
        self.ax2.axis('off')
        
        self.canvas.draw()
    
    def analyze_and_plot(self):
        """Analyze text and create interactive charts"""
        text = self.text_input.get("1.0", tk.END).strip()
        
        if not text:
            self.stats_text.delete("1.0", tk.END)
            self.stats_text.insert("1.0", "Please enter some text to analyze.")
            return
        
        # Analyze text using functions from simple_analyzer.py
        letters = count_letters(text)
        words = count_words(text)
        
        # Update statistics
        self.update_statistics(text, letters, words)
        
        # Create interactive charts
        self.create_letter_chart(letters)
        self.create_word_chart(words)
        
        # Refresh canvas
        self.canvas.draw()
    
    def update_statistics(self, text, letters, words):
        """Update statistics display"""
        stats = f"""TEXT ANALYSIS SUMMARY
{'='*40}
Text: '{text[:50]}{'...' if len(text) > 50 else ''}'
Total characters: {len(text)}
Total words: {len(text.split())}
Total letters: {sum(letters.values())}
Unique letters: {len(letters)}

MOST COMMON LETTERS:
"""
        
        # Show top 5 letters
        sorted_letters = sorted(letters.items(), key=lambda x: x[1], reverse=True)
        for i, (letter, count) in enumerate(sorted_letters[:5]):
            stats += f"{i+1}. '{letter}': {count} times\n"
        
        stats += f"\nMOST COMMON WORDS:\n"
        # Show top 5 words
        sorted_words = sorted(words.items(), key=lambda x: x[1], reverse=True)
        for i, (word, count) in enumerate(sorted_words[:5]):
            stats += f"{i+1}. '{word}': {count} times\n"
        
        self.stats_text.delete("1.0", tk.END)
        self.stats_text.insert("1.0", stats)
    
    def create_letter_chart(self, letters):
        """Create interactive letter frequency chart"""
        if not letters:
            return
        
        self.ax1.clear()
        
        # Sort letters by frequency
        sorted_letters = sorted(letters.items(), key=lambda x: x[1], reverse=True)
        letters_list = [item[0] for item in sorted_letters]
        counts_list = [item[1] for item in sorted_letters]
        
        # Create bar chart
        bars = self.ax1.bar(letters_list, counts_list, color='skyblue', alpha=0.7, edgecolor='navy')
        
        # Add value labels on bars
        for bar, count in zip(bars, counts_list):
            height = bar.get_height()
            self.ax1.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                          str(count), ha='center', va='bottom', fontweight='bold')
        
        self.ax1.set_title('Letter Frequency Distribution', fontsize=14, fontweight='bold')
        self.ax1.set_xlabel('Letters', fontsize=12)
        self.ax1.set_ylabel('Frequency', fontsize=12)
        self.ax1.grid(axis='y', alpha=0.3)
        
        # Rotate x-axis labels for better readability
        self.ax1.tick_params(axis='x', rotation=45)
    
    def create_word_chart(self, words):
        """Create interactive word frequency chart"""
        if not words:
            return
        
        self.ax2.clear()
        
        # Get top 10 words
        sorted_words = sorted(words.items(), key=lambda x: x[1], reverse=True)[:10]
        words_list = [item[0] for item in sorted_words]
        counts_list = [item[1] for item in sorted_words]
        
        # Create horizontal bar chart for words
        bars = self.ax2.barh(words_list, counts_list, color='lightcoral', alpha=0.7, edgecolor='darkred')
        
        # Add value labels on bars
        for bar, count in zip(bars, counts_list):
            width = bar.get_width()
            self.ax2.text(width + 0.1, bar.get_y() + bar.get_height()/2.,
                          str(count), ha='left', va='center', fontweight='bold')
        
        self.ax2.set_title('Top 10 Word Frequencies', fontsize=14, fontweight='bold')
        self.ax2.set_xlabel('Frequency', fontsize=12)
        self.ax2.set_ylabel('Words', fontsize=12)
        self.ax2.grid(axis='x', alpha=0.3)
    
    def clear_all(self):
        """Clear input, statistics, and charts"""
        self.text_input.delete("1.0", tk.END)
        self.stats_text.delete("1.0", tk.END)
        self.show_welcome_message()

def main():
    root = tk.Tk()
    app = AnalyzerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
