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
                                    ''",
                                    settings.EMAIL_HOST_USER, #Remitente
                                    [user.email]) #Destinatario

    message.attach_alternative(content, 'text/html')
    message.send()