import numpy as np
import string
import tensorflow as tf
from tensorflow import keras
from keras import Sequential
from keras import Dense, Dropout, Flatten
from keras import to_categorical
from sklearn.model_selection import train_test_split

# Этот словарь сопоставляет каждый символ в неправильной раскладке правильному символу
layout_mapping = {
    'q': 'й', 'w': 'ц', 'e': 'у', 'r': 'к', 't': 'е', 'y': 'н', 'u': 'г', 'i': 'ш', 'o': 'щ', 'p': 'з',
    'a': 'х', 's': 'ъ', 'd': 'ф', 'f': 'ы', 'g': 'в', 'h': 'а', 'j': 'п', 'k': 'р', 'l': 'о',
    'z': 'л', 'x': 'д', 'c': 'ж', 'v': 'э', 'b': 'я', 'n': 'ч', 'm': 'с', 'Q': 'Й', 'W': 'Ц',
    'E': 'У', 'R': 'К', 'T': 'Е', 'Y': 'Н', 'U': 'Г', 'I': 'Ш', 'O': 'Щ', 'P': 'З', 'A': 'Х',
    'S': 'Ъ', 'D': 'Ф', 'F': 'Ы', 'G': 'В', 'H': 'А', 'J': 'П', 'K': 'Р', 'L': 'О', 'Z': 'Л',
    'X': 'Д', 'C': 'Ж', 'V': 'Э', 'B': 'Я', 'N': 'Ч', 'M': 'С'
}

# Этот словарь хранит правильную версию слов, набранных в неправильной раскладке
memory = {}

def process_word(word):
    # Переводим слово из неправильной раскладки в правильную
    translated_word = ''.join(layout_mapping.get(c, c) for c in word)

    # Если слово новое, добавляем его в память
    if translated_word not in memory:
        memory[translated_word] = word

    # Возвращаем правильную версию слова
    return translated_word

def create_dataset(words):
    # Создаем сопоставление символов целым числам
    char_to_int = dict((c, i) for i, c in enumerate(string.printable))

    X = np.zeros((len(words), len(string.printable), len(max(words, key=len)))))), dtype=np.bool)
    y = np.zeros((len(words), len(max(words, key=len))))))

    for i, word in enumerate(words):
        translated_word = process_word(word)
        for j, char in enumerate(string.printable):
            X[i, j, :len(word)] = (char_to_int[char] == char_to_int[c] for c in word)
        y[i, :len(translated_word)] = [char_to_int[c] for c in translated_word]

    return X, to_categorical(y)

def create_neural_network(max_word_length):
    model = Sequential()
    model.add(Dense(512, input_shape=(len(string.printable), max_word_length), activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(512, activation='relu'))
    model.add(Dropout(0.2))
    model.add(Flatten())
    model.add(Dense(len(string.printable) * max_word_length, activation='softmax'))

    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    return model

def train_neural_network(words):
    # Определяем длину самого длинного слова
    max_word_length = len(max(words, key=len))

    # Создаем набор данных
    X, y = create_dataset(words)

    # Разделяем набор данных на обучающую и тестовую выборки
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Создаем нейронную сеть
    model = create_neural_network(max_word_length)

    # Обучаем нейронную сеть
    model.fit(X_train, y_train, batch_size=32, epochs=10, verbose=1, validation_data=(X_test, y_test))

    # Сохраняем нейронную сеть в файл
    model.save('neural_network.h5')

def predict_word(word):
    # Загружаем нейронную сеть из файла
    model = tf.keras.models.load_model('neural_network.h5')

    # Определяем длину самого длинного слова
    max_word_length = len(max(memory, key=len))

    # Создаем сопоставление символов целым числам
    char_to_int = dict((c, i) for i, c in enumerate(string.printable))

    # Подготавливаем входные данные для нейронной сети
    X = np.zeros((1, len(string.printable), max_word_length)), dtype=np.bool)
    for j, char in enumerate(string.printable):
        X[0, j, :len(word)] = (char_to_int[char] == char_to_int[c] for c in word)

    # Выполняем предсказание с помощью нейронной сети
    y_pred = model.predict(X)

    # Конвертируем предсказание в строку
    predicted_word = ''
    for i in range(max_word_length):
        char_int = np.argmax(y_pred[0, i * len(string.printable): (i + 1) * len(string.printable)])
        char = chr(char_int) if char_int >= 32 and char_int <= 126 else ' '
        predicted_word += char

    # Проверяем, есть ли предсказанное слово в памяти
    if predicted_word in memory:
        # Если предсказанное слово есть в памяти, возвращаем оригинальное слово
        return memory[predicted_word]
    else:
        # Если предсказанное слово нет в памяти, возвращаем 0
        return 0

if __name__ == '__main__':
    # Собираем список слов, набранных в неправильной раскладке
    words = []
    while True:
        # Получаем слово от пользователя
        word = input('Введите слово (или напишите "exit" для выхода): ').lower().strip()

        if word == 'exit':
            break

        # Добавляем слово в список
        words.append(word)

    # Обучаем нейронную сеть
    train_neural_network(words)

    # Тестируем нейронную сеть
    while True:
        # Получаем слово от пользователя
        word = input('Введите слово для предсказания (или напишите "exit" для выхода): ').lower().strip()

        if word == 'exit':
            break

        # Выполняем предсказание слова с помощью нейронной сети
        result = predict_word(word)
        print(f'Результат: {result}')
