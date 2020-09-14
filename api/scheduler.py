
from datetime import datetime, date
from api.models import Colonia, Destinatario
from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
import requests
import logging

logger = logging.getLogger(__name__)

URL = 'http://fflood-env.eba-72qxynva.us-west-1.elasticbeanstalk.com/api/ml/prediccion'

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_user_mail, 'cron', hour=3, minute=15, second=0)
    scheduler.start()

def send_user_mail():
    hoy = date.today()
    hoy_s = hoy.strftime('%Y-%m-%d')
    p = ''
    try:
        colonias = Colonia.objects.all()
        for c in colonias:
            result = requests.get(URL+'?colonia='+str(c.id_colonia)+"&fecha="+hoy_s)
            print(result.json())
            result = result.json()
            p += createMessage(c, result['value'])
            logger.info(p)
        users = Destinatario.objects.all()
        for u in users:
            b = createBody(u.nombre, hoy_s, p)
            s = createSubject(hoy_s)
            message = EmailMultiAlternatives(s, #Titulo
                                    b,
                                    settings.EMAIL_HOST_USER, #Remitente
                                    [u.email]) #Destinatario
            message.send()
            logger.info('Alert succesfully sent to: ' + u.nombre)
    except Exception as e:
        logger.error(str(e))

def createMessage(colonia, prediccion):
    msg = 'Para la colonia ' + str(colonia.nombre)
    if prediccion < 0.5:
        msg += 'no hay probabilidad de inundación.\n'
    else:
        msg += ' existe una probabilidad '
        if prediccion <= 0.6:
            msg += 'baja, '
        elif prediccion <= 0.8:
            msg += 'media, '
        elif prediccion <= 1:
            msg += 'alta, '
        msg += 'de inundación. Valor: ' + str(round(prediccion*100)) + '%.\n'
    return msg

def createBody(nombre, fecha, pronostico):
    msg = 'Hola ' + nombre + ','
    msg += ' el pronóstico para el día de hoy ' + fecha + ' es:\n'
    msg += pronostico + '\n'
    msg += 'Gracias por hacer uso del sistema de alertas de fflood.'
    return msg

def createSubject(fecha):
    msg = 'Pronóstico ' + fecha
    return msg
