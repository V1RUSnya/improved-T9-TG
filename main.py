import pyrogram
# import ai

app = pyrogram.Client("my_account")
your_user_id = 774159671  # ID телеграмм аккаунта

@app.on_message()
def type(client_object, message: pyrogram.types.Message):
    if message.from_user is not None and message.from_user.id == your_user_id:
        print(message.text)
        # message.edit("// " + message.text)  # Изменение сообщения

app.run()