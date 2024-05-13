import smtplib
from random import choices
import string
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class MailSendler:
    """Класс создает объект, который отправляет email"""
    def __init__(self, bot_email, bot_email_password):
        self._bot_email = bot_email
        self._bot_email_password = bot_email_password
        self._smtp_server = smtplib.SMTP("smtp.yandex.ru", 587)
        self._smtp_server.starttls()

    async def start_sendler(self):
        """Логинимся на почте"""
        self._smtp_server.login(user=self._bot_email, password=self._bot_email_password)

    async def send_verification_code(self, user_email):
        """Отправляем код подтверждения пользователю на почту"""
        # Создание объекта сообщения
        msg = MIMEMultipart()

        # Настройка параметров сообщения
        msg["From"] = self._bot_email
        msg["To"] = user_email
        msg["Subject"] = "Код подтверждения"

        # Добавление текста в сообщение
        verification_code = ''.join(choices(string.digits + string.ascii_letters, k=8))
        msg_text = f'Ваш код подтверждения для регистрации {verification_code}'

        msg.attach(MIMEText(msg_text, "plain"))
        self._smtp_server.sendmail(from_addr=self._bot_email, to_addrs=user_email, msg=msg.as_string())
        # Так же вернем код, что бы можно было свериться с тем, что введет пользователь
        return verification_code


