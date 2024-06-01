import pyrogram

app = pyrogram.Client("my_account")

@app.on_message(pyrogram.filters.command(""))
def type(client_object, message: pyrogram.types.Message):
   print(message.text)

app.run()