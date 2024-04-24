import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
GPT_API_URL = "https://api.openai.com/v1/chat/completions"
GPT_API_KEY = "YOUR_GPT_API_KEY"


def start(update, context):
    update.message.reply_text("Приветствую! Я нейросеть, которая может разговаривать на всех языках мира, отвечать на любой вопрос, делать конспекты и сочинения, писать программный код. Задайте ваш вопрос.")


def handle_message(update, context):
    text = update.message.text
    if text.startswith('/'):
        return
    update.message.reply_text("Обрабатываю запрос...")
    response = process_question(text)
    update.message.reply_text(response)


def process_question(question):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GPT_API_KEY}"
    }
    data = {
        "model": "text-davinci-003",
        "messages": [
            {
                "role": "user",
                "content": question
            }
        ]
    }
    response = requests.post(GPT_API_URL, json=data, headers=headers)
    response_data = response.json()
    if response.status_code == 200:
        return response_data["choices"][0]["message"]["content"]
    else:
        return "Извините, произошла ошибка при обработке запроса."

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
