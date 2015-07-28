import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.conf import settings


def send_mail(subject, text_msg, to_email_list):

    server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
    server.starttls()
    server.ehlo()
    server.esmtp_features['auth'] = 'LOGIN PLAIN'
    server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

    from_email = settings.EMAIL_FROM_USER

    mail = MIMEMultipart("alternative")
    mail['Subject'] = subject
    mail['From'] = from_email
    mail.attach(MIMEText(text_msg, 'plain'))

    for to_email in to_email_list:
        del mail['To']
        mail['To'] = to_email
        server.sendmail(from_email, to_email, mail.as_string())