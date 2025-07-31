from collections import Counter
import re

class TextAnalyzer:
    def __init__(self, text):
        """
        Initialize with text to analyze
        """
        self.original_text = text
        self.text = text.lower()  # For case-insensitive analysis

    def get_character_frequency(self, include_spaces=False):
        """
        Get frequency of each character.
        """
        chars = self.text if include_spaces else self.text.replace(" ", "")
        return Counter(chars)

    def get_word_frequency(self, min_length=1):
        """
        Get frequency of each word, filtering by min_length.
        """
        words = re.findall(r'\b\w+\b', self.text)
        filtered = [w for w in words if len(w) >= min_length]
        return Counter(filtered)

    def get_sentence_length_distribution(self):
        """
        Analyze sentence lengths (in words).
        """
        sentences = re.split(r'[.!?]+', self.text)
        lengths = [len(re.findall(r'\b\w+\b', s)) for s in sentences if s.strip()]
        counter = Counter(lengths)
        return {
            "lengths": counter,
            "average": round(sum(lengths) / len(lengths), 2) if lengths else 0,
            "longest": max(lengths) if lengths else 0,
            "shortest": min(lengths) if lengths else 0
        }

    def find_common_words(self, n=10, exclude_common=True):
        """
        Find most common words, optionally excluding stop words.
        """
        common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by',
                        'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'did', 'will',
                        'would', 'could', 'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those', 'it', 'you',
                        'he', 'she', 'we', 'they', 'i', 'me', 'him', 'her', 'us', 'them'}
        word_freq = self.get_word_frequency(1)
        if exclude_common:
            for w in list(word_freq.keys()):
                if w in common_words:
                    del word_freq[w]
        return word_freq.most_common(n)

    def get_reading_statistics(self):
        """
        Get reading statistics including word count, sentence count, etc.
        """
        words = re.findall(r'\b\w+\b', self.text)
        sentences = re.split(r'[.!?]+', self.text)
        char_count = len(self.text)
        avg_word_len = round(sum(len(w) for w in words) / len(words), 2) if words else 0
        reading_time = round(len(words) / 200, 2)  # 200 WPM assumption
        return {
            "character_count": char_count,
            "word_count": len(words),
            "sentence_count": len([s for s in sentences if s.strip()]),
            "average_word_length": avg_word_len,
            "reading_time_minutes": reading_time
        }

    def compare_with_text(self, other_text):
        """
        Compare this text with another.
        """
        words1 = set(re.findall(r'\b\w+\b', self.text))
        words2 = set(re.findall(r'\b\w+\b', other_text.lower()))
        common = words1 & words2
        similarity = round(len(common) / len(words1 | words2) * 100, 2) if (words1 | words2) else 0
        return {
            "common_words": list(common),
            "similarity_score": similarity,
            "unique_to_first": list(words1 - words2),
            "unique_to_second": list(words2 - words1)
        }


# ✅ Test the implementation
sample_text = """
Python is a high-level, interpreted programming language with dynamic semantics.
Its high-level built-in data structures, combined with dynamic typing and dynamic binding,
make it very attractive for Rapid Application Development. Python is easy to learn and
python supports modules and packages, which encourages program modularity and code reuse.
The Python interpreter and the extensive standard library are available in source or binary
form without charge for all major platforms, and can be freely distributed.
"""

analyzer = TextAnalyzer(sample_text)

print("Character frequency (top 5):", analyzer.get_character_frequency().most_common(5))
print("Word frequency (top 5):", analyzer.get_word_frequency().most_common(5))
print("Common words:", analyzer.find_common_words(5))
print("Sentence length distribution:", analyzer.get_sentence_length_distribution())
print("Reading statistics:", analyzer.get_reading_statistics())

# Compare with another text
other_text = "Java is a programming language. Java is object-oriented and platform independent."
comparison = analyzer.compare_with_text(other_text)
print("Comparison results:", comparison)
