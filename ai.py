class WordChecker:
    def __init__(self):
        self.word_db = {}  # база слов с их частотами
        self.min_similarity = 0.6  # минимальное значение similarity для коррекции

    def check_word(self, word):
        # 1. Получаем слово
        word = word.lower()  # приводим к нижнему регистру

        # 2. Записываем слово в базу
        self.word_db[word] = self.word_db.get(word, 0) + 1

        # 3. Проверяем не совпадает ли оно с другим - более часто употребляемым словом
        similar_words = self.find_similar_words(word)
        if similar_words:
            most_frequent_similar_word = max(similar_words, key=lambda x: self.word_db.get(x, 0))
            similarity = self.calculate_similarity(word, most_frequent_similar_word)
            if similarity >= self.min_similarity:
                # 4. Возвращаем правильное слово если совпадает, но написано не верно
                return most_frequent_similar_word

        # если слово не совпадает с часто употребляемыми словами, возвращаем False
        return False

    def find_similar_words(self, word):
        similar_words = []
        for w in self.word_db:
            if w != word and len(w) == len(word):
                similar_words.append(w)
        return similar_words

    def calculate_similarity(self, word1, word2):
        # простой алгоритм сравнения строк (Levenshtein distance)
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