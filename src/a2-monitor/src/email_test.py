# Install Courier SDK: pip install trycourier
from trycourier import Courier
from my_log import myLog
client = Courier(auth_token="<random_token>")

em_ml = myLog("Emailer")

email_address="example@uni.ac.uk"

def sendErrorEmail(subject, msg):
   try:
      resp = client.send_message(
         message={
            "to": {
               "email": email_address
            },
            "content": {
               "title": subject,
               "body": msg
            }
         }
      )
      return True
   except Exception:
      return False


# Create e-mail message, and send notification.
email_msg = {}
def reset_email_msg():
    email_msg = {}

def send_error():
    subject = ""
    message = ""
    if len(email_msg) == 1:
        for service,stats in email_msg.items():
            subject = f"Service ({service}) is down"
            message = f"{service} is down. Send help!\nHere are the current stats: {stats}"
        em_ml.log_info("Sending email for single service")
    elif len(email_msg) > 1:
        for k,v in email_msg.items():
            subject = "Multiple Services are down"
            message = message + f"\n\n{k} is down. Send help!\nHere are the current stats: {v}"
        em_ml.log_info("Sending email for multi-service")
    else:
        em_ml.log_info("There have been no change in stats so no email is sent.")
        return
    reset_email_msg()
    em_ml.log_warn("Sending Email to " + email_address)
    email_res = sendErrorEmail(subject, message) # Send the email
    if email_res:
        em_ml.log_info("Successfully sent email to " + email_address)
    else:
        em_ml.log_error("An error was encountered when sending email to " + email_address)

def make_email(service, stats):
    em_ml.log_info("Adding " + service + " to email")
    email_msg[service] = stats
