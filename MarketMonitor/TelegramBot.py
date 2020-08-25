import requests
import telegram
from telegram import Bot
from jinja2 import Template

TEMPLATE = 'message_template.html'


class Messenger:
    def __init__(self, token, chat_id):
        self.bot_token = token
        self.chat_id = chat_id
        self.bot = Bot(self.bot_token)

        template_str = open(TEMPLATE, 'r').read()
        self.template = Template(template_str)

    def send_simple_text(self, bot_message):
        send_text = 'https://api.telegram.org/bot' + self.bot_token + '/sendMessage?chat_id=' + self.chat_id + '&parse_mode=Markdown&text=' + bot_message

        response = requests.get(send_text)

        return response.json()

    def send_html(self, info_json):
        # format the text using a jinja
        text = self.template.render(info_json, information=info_json)

        self.bot.send_message(chat_id=self.chat_id,
                              text=text,
                              parse_mode=telegram.ParseMode.HTML)
