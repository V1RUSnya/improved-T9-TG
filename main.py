import pyrogram

import config  # api_id and api_hash from https://my.telegram.org/
import correct

checker = correct.WordChecker()
app = pyrogram.Client("my_account", api_id=config.api_id, api_hash=config.api_hash)
user_id = None


@app.on_message()
def typing(client_object, message: pyrogram.types.Message):
    global user_id

    if message.from_user is None:
        return

    if message.text == "/start":
        user_id = message.from_user.id
        message.edit("Ready ☑")
    elif user_id is not None:
        if message.from_user.id == user_id:
            words = message.text.split()
            corrected_words = []
            for word in words:
                result = checker.check_word(word)
                if result:
                    corrected_words.append(result)
                else:
                    corrected_words.append(word)
            corrected_text = ' '.join(corrected_words)
            if message.text != corrected_text and checker.can_correct():
                print(f"{message.text} -->> {corrected_text}")
                message.edit(corrected_text)
    checker.save_db()


app.run()
