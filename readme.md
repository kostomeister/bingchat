# BingChat

BingChat provides a Python interface to interact with the Bing chatbot AI. It allows you to easily send text and image prompts and receive responses.

## Installation 

Since BingChat is currently only available on GitHub, you'll need to install it directly from the repo:

```bash
git clone https://github.com/user/bingchat.git
cd bingchat
pip install . 
```

This will automatically install the requirements in requirements.txt, including Selenium, Edge WebDriver, and other dependencies.

## Usage

```python
from bingchat import BingChat

chat = BingChat()

chat.set_prompt("Describe this image.")

chat.upload_image("example.jpg") 

response = chat.submit()

print(response)
```

The main methods are: 

- `set_prompt` - Sets a text prompt

- `upload_image` - Uploads an image prompt

- `submit` - Submits the prompt and returns the AI response

- `clear_prompts` - Clears any existing prompts

- `prompts_left` - Gets the number of remaining prompts allowed 

The chatbot has a limited number of prompts per session. Use `prompts_left` to check remaining prompts and `clear_prompts` to reset.

## Contributing

Contributions are welcome! Please open an issue or PR on Github.

## Credits

BingChat uses Selenium to programmatically interact with the Bing chatbot. Credit to Microsoft for providing the AI chatbot.

## License 

MIT
