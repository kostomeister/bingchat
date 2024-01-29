import time

from bingchat import BingChat

chat = BingChat()

chat.set_tone_creative()

chat.set_prompt("Describe this image.")
chat.upload_image("example.jpg")
time.sleep(1)
response = chat.submit()
print(response)
