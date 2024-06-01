import pyrogram

app = pyrogram.Client("my_account")

@app.on_message()
def type(client_object, message: pyrogram.types.Message):
    print(message.text)

app.run()