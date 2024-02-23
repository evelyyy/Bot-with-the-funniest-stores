from openai import OpenAI
import telebot
from telebot.types import KeyboardButton, Message
from telebot import types
from dotenv import load_dotenv
from os import getenv

load_dotenv()
token = getenv('token')
bot = telebot.TeleBot(token)


@bot.message_handler(commands=["start"])
def start(message: Message):
  keyboard = types.ReplyKeyboardMarkup(row_width=2)
  button1 = types.KeyboardButton("Generate")
  button2 = types.KeyboardButton('Continue')
  button3 = types.KeyboardButton("Stop")
  keyboard.add(button1, button2, button3)
  bot.send_message(message.chat.id,
                   'Hello, my dear user! Я бот, который может генерировать смешные истории на английском.\n'
                   'Нажми на кнопку ниже, чтобы начать генерацию.',
                   reply_markup=keyboard)


@bot.message_handler(func=lambda message: True)
def generate(message):
  if message.text == 'Generate':
    client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")

    completion = client.chat.completions.create(
      model="local-model",
      messages=[
        {"role": "system", "content": "Always answer in rhymes."},
        {"role": "user", "content": "Imagine that you are a good writer. Write a simple funny story."}
      ],
      temperature=7,
    )

    gpt_response = completion.choices[0].message.content

    bot.send_message(message.chat.id, text = gpt_response)
  elif message.text == 'Continue':
    client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")
    completion = client.chat.completions.create(
      model="local-model",
      messages=[
        {"role": "system", "content": "Always answer in rhymes."},
        {"role": "user", "content": "Continue this story a lot."}
      ],
      temperature=7,
    )
    gpt_response2 = completion.choices[0].message.content

    bot.send_message(message.chat.id, text=gpt_response2)
  elif message.text == 'Stop':
    bot.send_message(message.chat.id, 'Хорошо! Если понадобится новая история, пиши Generate.')
  else:
    bot.send_message(message.chat.id, 'Напиши: Generate, чтобы сгенерировать историю.\nНапиши: Continue, чтобы продолжить генерацию истории.\nНапиши: Stop, чтобы закончить генерацию')
bot.polling()
