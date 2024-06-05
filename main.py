import pyrogram
import correct

checker = correct.WordChecker()
app = pyrogram.Client("my_account")
your_user_id = 774159671  # ID телеграмм аккаунта

@app.on_message()
def type(client_object, message: pyrogram.types.Message):
    if message.from_user is not None and message.from_user.id == your_user_id:
        print(message.text)
        words = message.text.split()
        corrected_words = []
        for word in words:
            result = checker.check_word(word)
            if result != False:
                corrected_words.append(result)
            else:
                corrected_words.append(word)
        corrected_text = ' '.join(corrected_words)
        print(f"{message.text} -->> {corrected_text}")
        if message.text != corrected_text: message.edit(corrected_text)  # Изменение сообщения
    checker.save_db()

app.run()