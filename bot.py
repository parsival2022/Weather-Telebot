
import os
from models import User
from time import sleep
from telebot.async_telebot import AsyncTeleBot
from dotenv import load_dotenv
from keyboards import start_kb, w_details_kb, f_details_kb, specific_details_cb, menu_cb
from weather_util import get_weather, get_forecast
from helpers import Checker, get_user_and_id
from messages import *



# getting telegram bot token from .env
load_dotenv()
TOKEN = os.getenv('TOKEN') 

# initialising asynchronous bot
bot = AsyncTeleBot(TOKEN, parse_mode='HTML')

# initialising checkers from custom Checker class
cr_checker = Checker(['crossroad'])
m_checker = Checker(['get_forecast', 'get_weather'])
sp_checker = Checker(['get_specific_w', 'get_specific_f'])
spd_checker = Checker(specific_details_cb)

# handling /start command
# this command will always return user to main menu
@bot.message_handler(commands=['start'])
async def start_handler(msg):
    id, user = get_user_and_id(msg)

    if not user:
        user = User.create(user_id=id, stage='crossroad')
        user.save()
    else:
        user.stage = 'crossroad'  
        user.save()
    text = start_greeting(msg.from_user.username)
    await bot.send_message(id, text, reply_markup=start_kb)


# this handler checking callback recieved from inline main menu 
# and send according message with inline menu
@bot.callback_query_handler(lambda query: query.data in menu_cb)
async def get_chosen_option_handler(msg):
    id, user = get_user_and_id(msg)
    # saving user`s choice
    if user.stage == 'crossroad':
       user.stage = msg.data
       user.save()

       if user.stage in ['get_forecast', 'get_weather']:
           await bot.send_message(id, enter_city)  
       elif user.stage in ['get_specific_w']:
           await bot.send_message(id, chose_detail, reply_markup=w_details_kb)
       else:
           await bot.send_message(id, chose_detail, reply_markup=f_details_kb)
           

# this handler checks what specific option user chose, saving it and asking for the place
@bot.callback_query_handler(lambda query: query.data in specific_details_cb)
async def get_specific_place_handler(msg):
    id, user = get_user_and_id(msg)

    if user.stage == 'get_specific_w' or user.stage == 'get_specific_f':
        user.stage = msg.data
        user.save()
        await bot.send_message(id, enter_city) 


# this handler recieved place and processing it in accordance with chosen specific option which was saved before 
@bot.message_handler(func=spd_checker.check_stage)
async def send_specific_detail_answer(msg):
    id, user = get_user_and_id(msg)

    if user.stage in specific_details_cb:
        splitted = user.stage.split('_')
        mode = splitted[-1]
        answer = get_weather(msg.text, mode) if splitted[-2] == 'w' else get_forecast(msg.text, mode)
        await bot.reply_to(msg, answer)
        user.stage = 'crossroad'
        user.save()
        sleep(2)
        await bot.send_message(id, get_weather_again, reply_markup=start_kb)

        
# after recieving city from user, this handler checking user`s stage and processing recieved input accordingly
@bot.message_handler(func=m_checker.check_stage)
async def give_weather_handler(msg):
    id, user = get_user_and_id(msg)

    if user.stage == 'get_weather' or user.stage == 'get_forecast':
        answer = get_weather(msg.text) if user.stage == 'get_weather' else get_forecast(msg.text)
        await bot.reply_to(msg, answer)
        user.stage = 'crossroad'
        user.save()
        sleep(2)
        await bot.send_message(id, get_weather_again, reply_markup=start_kb)


# this handler processing random messages when there was no option chosen or no command recieved
@bot.message_handler(func=cr_checker.check_stage)
async def no_option_chosen(msg):
    await bot.reply_to(msg, choose_option, reply_markup=start_kb)




# bot polling, for developing usage only
if __name__ == '__main__':
    import asyncio
    asyncio.run(bot.polling())