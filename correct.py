import os


def calculate_similarity(word1, word2):
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cost = 0 if word1[i - 1] == word2[j - 1] else 1
            dp[i][j] = min(dp[i - 1][j] + 1, dp[i][j - 1] + 1, dp[i - 1][j - 1] + cost)
    return 1 - dp[m][n] / max(m, n)


def remove_punctuation(word):
    return ''.join(e for e in word if e.isalnum() or e.isspace())


class WordChecker:
    def __init__(self, db_file='word_db.txt'):
        self.db_file = db_file
        self.word_db = {}
        self.min_similarity = 0.6
        self.word_count = 0
        self.load_db()

    def check_text(self, text):
        words = [word.strip() for word in text.split()]  # split text into individual words
        corrected_words = []
        for word in words:
            corrected_word = self.check_word(word)
            if corrected_word:
                corrected_words.append(corrected_word)
            else:
                corrected_words.append(word)
        return ' '.join(corrected_words)  # join corrected words with spaces

    def check_word(self, word):
        # 1. Get word
        word = word.lower()  # lowercase
        word = remove_punctuation(word)

        # 2. Write word to base
        self.word_db[word] = self.word_db.get(word, 0) + 1
        self.word_count += 1

        # 3. Check word for similarity
        similar_words = self.find_similar_words(word)
        if similar_words:
            most_frequent_similar_word = max(similar_words, key=lambda x: self.word_db.get(x, 0))
            similarity = calculate_similarity(word, most_frequent_similar_word)
            if similarity >= self.min_similarity:
                # 4. Return corrected word
                return most_frequent_similar_word

        # else return False
        return False

    def find_similar_words(self, word):
        similar_words = []
        for w in self.word_db:
            if w != word and len(w) == len(word):
                similar_words.append(w)
        return similar_words

    def load_db(self):
        if os.path.exists(self.db_file):
            with open(self.db_file, 'r') as f:
                for line in f:
                    parts = line.strip().split('\t')
                    if len(parts) == 2:
                        phrase, freq = parts
                        words = phrase.split()
                        for word in words:
                            self.word_db[word] = self.word_db.get(word, 0) + int(freq)
                            self.word_count += 1

    def save_db(self):
        with open(self.db_file, 'w') as f:
            for word, freq in self.word_db.items():
                f.write(f"{word}\t{freq}\n")
        self.word_count = len(self.word_db)

    def can_correct(self):
        return self.word_count >= 500
