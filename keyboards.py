from telebot.util import quick_markup


specific_details_cb = ['get_sp_w_t', 'get_sp_w_h', 'get_sp_w_c', 'get_sp_w_r', 'get_sp_w_w',
                       'get_sp_f_t', 'get_sp_f_h', 'get_sp_f_c', 'get_sp_f_r', 'get_sp_f_w']

menu_cb = ['get_forecast', 'get_weather', 'get_specific_w', 'get_specific_f']


start_kb = quick_markup({'Get Weather': {'callback_data':'get_weather'},
                         'Get Weather Forecast': {'callback_data': 'get_forecast'},
                         'Get Specific Weather': {'callback_data': 'get_specific_w'},
                         'Get Specific Forecast': {'callback_data': 'get_specific_f'}
                        }, row_width=1)


w_details_kb = quick_markup({'Temperature': {'callback_data': 'get_sp_w_t'},
                           'Humidity': {'callback_data': 'get_sp_w_h'},
                           'Clouds': {'callback_data': 'get_sp_w_c'},
                           'Rain': {'callback_data': 'get_sp_w_r'},
                           'Wind': {'callback_data': 'get_sp_w_w'}
                          }, row_width=1, )

f_details_kb = quick_markup({'Temperature': {'callback_data': 'get_sp_f_t'},
                           'Humidity': {'callback_data': 'get_sp_f_h'},
                           'Clouds': {'callback_data': 'get_sp_f_c'},
                           'Rain': {'callback_data': 'get_sp_f_r'},
                           'Wind': {'callback_data': 'get_sp_f_w'}
                          }, row_width=1, )





