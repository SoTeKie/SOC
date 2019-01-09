import smtplib
import ssl
import getpass
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

# SSL port 
port = 465

# Credentials and message
sender = "rpicamrk@gmail.com"
receiver = "rpicamrk@gmail.com"
password = getpass.getpass()
filename = "image.jpg"

# Set up email subject etc
message = MIMEMultipart("alternative")
message["Subject"] = "Movement detected!"
message["From"] = sender 
message["To"] = receiver

plainMsg = """\
Html must be enabled to view image."""

with open('html_msg.html', 'r') as f:
    htmlMsg = f.read()

img = open(filename, 'rb').read()
msgImg = MIMEImage(img, 'jpg')
msgImg.add_header('Content-ID', '<image1>')
msgImg.add_header('Content-Disposition', 'inline', filename=filename)


# Turn them into MIMEText objects
part1 = MIMEText(plainMsg, "plain")
part2 = MIMEText(htmlMsg, "html")


# Add them to the message, the last one will be rendered first
message.attach(part1)
message.attach(part2)
message.attach(msgImg)

# Create secure context
context = ssl.create_default_context()

# Login and send email
with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    server.login(sender, password)
    server.sendmail(sender, receiver, message.as_string())
