
import os
from models import User
from time import sleep
from telebot.async_telebot import AsyncTeleBot
from dotenv import load_dotenv
from keyboards import start_kb
from weather_util import get_weather, get_forecast
from helpers import check_stage

# getting bot token from .env
load_dotenv()
TOKEN = os.getenv('TOKEN')

# initialising asynchronous bot
bot = AsyncTeleBot(TOKEN, parse_mode='HTML')

# handling /start command
# bot returning message with inline menu thet offers two options:
# get current weather or forecast weather for tomorrow
@bot.message_handler(commands=['start'])
async def start_handler(msg):
    id = msg.from_user.id
    user = User.select().where(User.user_id == id)

    if not user:
        user = User.create(user_id=id, stage='crossroad')
        user.save()
        
    text = f'Hello, {msg.from_user.username}! If you tell me the city or country I`ll find out it`s weather!'
    await bot.send_message(id, text, reply_markup=start_kb)

# handling callback: changing the stage to process the input according to chosen previosly menu option
# (which is getting current weather in this case)
# and then asking user to insert the city 
@bot.callback_query_handler(lambda query: query.data == 'get_weather')
async def get_weather_handler(msg):
    id= msg.from_user.id
    user = User.select().where(User.user_id == id).get()

    if user.stage == 'crossroad':
       user.stage = 'get_weather'
       user.save()

    enter_city = 'Please enter the city: '
    await bot.send_message(id, enter_city)

# this handler doing the same as previous, but changing the user stage according to forecast option
@bot.callback_query_handler(lambda query: query.data == 'get_forecast')
async def get_forecast_handler(msg):
    id = msg.from_user.id
    user = User.select().where(User.user_id == id).get()

    if user.stage == 'crossroad':
       user.stage = 'get_forecast'
       user.save()

    enter_city = 'Please enter the city: '
    await bot.send_message(id, enter_city)

# after recieving city from user, we checking user`s stage and processing his or her input accordingly
@bot.message_handler(func=check_stage)
async def give_weather_handler(msg):
    id = msg.from_user.id
    user = User.select().where(User.user_id == id).get()

    if user.stage == 'get_weather' or user.stage == 'get_forecast':
        answer = get_weather(msg.text) if user.stage == 'get_weather' else get_forecast(msg.text)
        await bot.reply_to(msg, answer)
        user.stage = 'crossroad'
        user.save()
        sleep(2)
        get_weather_again = 'Get you some other place`s weather?'
        await bot.send_message(id, get_weather_again, reply_markup=start_kb)



# bot polling, for developing usage only
if __name__ == '__main__':
    import asyncio
    asyncio.run(bot.polling())