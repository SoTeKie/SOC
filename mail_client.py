import smtplib
import ssl

# SSL port 
port = 465

password = input("Pass: ")

# Secure SSL context
context = ssl.create_default_context()

# Login and send email
with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    server.login("rpicamrk@gmail.com", password)


