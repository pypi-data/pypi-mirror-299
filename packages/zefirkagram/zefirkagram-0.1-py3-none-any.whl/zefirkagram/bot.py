import requests

class ZefirkaGram:
    def __init__(self, token: str, channel_id: str):
        """
        Initialize the bot with a Telegram token and channel ID.
        :param token: Bot token provided by the BotFather.
        :param channel_id: Telegram channel ID where the messages/images will be sent.
        """
        self.token = token
        self.channel_id = channel_id
        self.api_url = f"https://api.telegram.org/bot{self.token}"

    def send(self, message: str):
        """
        Send a text message to the Telegram channel.
        :param message: The message text to send (supports markdown and newlines).
        """
        url = f"{self.api_url}/sendMessage"
        payload = {
            'chat_id': self.channel_id,
            'text': message,
            'parse_mode': 'Markdown',
            'disable_web_page_preview': True
        }

        response = requests.post(url, data=payload)
        if response.status_code != 200:
            raise Exception(f"Failed to send message: {response.text}")

        return response.json()

    def send_picture(self, image_source):
        """
        Send an image to the Telegram channel. The image can be a file path, URL, or image stream.
        :param image_source: Path to the image, image URL, or an image stream object.
        """
        url = f"{self.api_url}/sendPhoto"
        data = {'chat_id': self.channel_id}

        # If image_source is a URL
        if isinstance(image_source, str) and image_source.startswith("http"):
            data['photo'] = image_source
            response = requests.post(url, data=data)

        # If image_source is a file path
        elif isinstance(image_source, str):
            with open(image_source, 'rb') as image_file:
                files = {'photo': image_file}
                response = requests.post(url, data=data, files=files)

        # If image_source is a stream (file-like object)
        else:
            files = {'photo': image_source}
            response = requests.post(url, data=data, files=files)

        if response.status_code != 200:
            raise Exception(f"Failed to send picture: {response.text}")

        return response.json()
