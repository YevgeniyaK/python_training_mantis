import poplib
import email
import time
import re

class MailHelper:
    def __init__(self, app):
        self.app = app

    def get_mail(self, username, password, subject):
        for i in range(5):
            pop = poplib.POP3(self.app.config['james']['host'])
            pop.user(username)
            pop.pass_(password)
            num = pop.stat()[0]
            if num > 0:
                for n in range(num):
                    msglines = pop.retr(n+1)[1]
                    msgtext = "\n".join(map(lambda x: x.decode('utf-8'), msglines))
                    # В письмах символ равенства "=" кодируется как "=3D", надо это заменить на "=" чтобы работали ссылки
                    msgtext = msgtext.replace("=3D", "=")
                    msg = email.message_from_string(re.sub(r"=\n[\s]*", "", msgtext))
                    if msg.get("Subject") == subject:
                        pop.dele(n+1)
                        pop.quit()
                        return msg.get_payload()
            pop.close()
            time.sleep(3)
        return None


