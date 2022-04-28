from pyowm.utils.config import get_default_config
from pyowm.owm import OWM
from pyowm.commons.exceptions import NotFoundError
from datetime import datetime

from config import OW_API, _

def Weater_message(arguments, message):
###Weather reaction###
        config_dict = get_default_config()
        config_dict['language'] = str(message.from_user.locale)
        owm = OWM(OW_API, config_dict)
        try:
            mgr = owm.weather_manager()
            observation = mgr.weather_at_place(arguments)
            w = observation.weather
            temp = w.temperature('celsius')['temp']
            today = datetime.today()
        #answers-weather
            answer = _('Weater_message_1').format(today=today.strftime("%d/%m/%Y"), arguments=arguments, detailed_status=w.detailed_status, temp=str(temp))
            if temp < 5:
                answer += _('Weater_message_2').format(arguments=arguments)+('!')
            elif temp < 17:
                answer += _('Weater_message_3').format(arguments=arguments)+('!')
            else:
                answer += _('Weater_message_4').format(arguments=arguments)+('?')
            return answer
        except NotFoundError:
            return _('Weater_message_5')+'?'