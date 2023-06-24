from django.core.mail import EmailMessage

import threading


class EmailThread(threading.Thread):
    """
    Send emails on new thread.
    This can be done also using background tasks instead(i.e Celery)
    """

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data["email_subject"],
            body=data["email_body"],
            from_email="pulselabs@org.co.ug",  # this will need to change to correct organization email
            to=[data["to_email"]],
        )
        # email.send()
        EmailThread(email).start()
