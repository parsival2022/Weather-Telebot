# Weather-Telebot
A simple Telegram bot for checking weather using Python Telegram Bot API

Used libraries:

python-telegram-bot-API as core
docs: https://docs.python-telegram-bot.org/en/stable/

pewee for working with database
docs: https://docs.peewee-orm.com/en/latest/index.html

OWM as free weather manager
docs: https://openweathermap.org/api
(you have to recieve key to use this service)

----------------------------------------------------

This bot is quite simple yet it constructed in a way that allows to add further functionality
without rewriting the whole code. So we have menu with four options. First two are 'Get weather' 
and 'Get Forecast' They are practically identical in behavior and differ only by result. When user 
choose option, bot asking them for a place, processing it by calling according function and return 
list of weather or forecast at the place which included temperature, humidity, rain, wind and clouds (more
to be added). Currently forecast could be recieved only for tomorrow(more options to be added). If user wish 
to get some specific data, bot got two other options: 'Get specific weather' and 'Get specific forecast'. 
These are similar too. After user chose some of them, bot sends inline menu with available weather 
parameters for user to choose, then asking for a place. After processing recieved data bot
returns asked parameter at the place. 
    /n- Bot automatically register every user
    /n- Bot remembering events from the user and processing data accordingly.
    This prevents random messages and abrupt mind changing. Once you got
    into cycle you should go to the end or jump to main menu using /start.
    /n- All messages and markup keyboards grouped in separate self-contained
    modules. In case message or keyboard editing that makes that much easier. 
    /n- Although in this version bot is run by polling for simplicity, there 
    should be used webhook instead if bot to be deployed. 
