from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework import status
from django.conf import settings
from django.core.mail import EmailMultiAlternatives


def send_user_mail(user):
    subject = 'Titulo del correo'
    template = "hola!!!!"
    #template = get_template('templates/mi_template_correo.html')

    #content = template.render({
     #   'user': user,
    #})

    message = EmailMultiAlternatives(subject, #Titulo
                                    '',
                                    settings.EMAIL_HOST_USER, #Remitente
                                    [user["email"]]) #Destinatario

    #message.attach_alternative(content, 'text/html')
    message.send()


class EmailView(APIView):
    def get(self, request, format=None):
        user = dict()
        user["email"] = 'jcampos.jc38@gmail.com'
        send_user_mail(user)
        return Response("ok")