from telebot.util import quick_markup

start_kb = quick_markup({'Get Weather': {'callback_data':'get_weather'},
                         'Get Weather Forecast': {'callback_data': 'get_forecast'}
                        }, row_width=1)

