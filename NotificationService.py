from abc import ABC, abstractmethod
import smtplib

# alllows a notification to be sent
class NotificationService(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def notify(text):
        pass

class ConsoleNotificationService(NotificationService):
    def __init__(self):
        pass

    def notify(self, text):
        print("ConsoleNotificationService: {0}".format(text))

class EmailNotificationService(NotificationService):
    def __init__(self):
        self.consoleNotificationService = ConsoleNotificationService()
        self.username = "josephagrane@gmail.com"
        self.password = "zzihnzkhekefesch"
        self.recipient = "flisslipscomb@gmail.com"

    def notify(self, text):
        print("EmailNotificationService: Sending email notification...")
        self.consoleNotificationService.notify(text)
        message = "From: {0}\nTo: {1}\nSubject: {2}\n\n{3}\n".format(self.username, self.recipient, "New Flat Listings", text)
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.ehlo()
        server.login(self.username, self.password)
        server.sendmail(self.username, self.recipient, message)
        server.close()
