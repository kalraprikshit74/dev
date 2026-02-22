import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email():
    try:
        # Set up the SMTP server (using Gmail's SMTP server)
        smtp_server = "smtp.gmail.com"
        smtp_port = 587

        # Create the MIMEMultipart message object
        message = MIMEMultipart()
        message['From'] = "kalraprikshit74@gmail.com"
        message['To'] = "manoj.hec@gmail.com"
        message['Subject'] ="writing_an_code_for_sending"

        # Attach the email body (text)
        message.attach(MIMEText("test email", 'plain'))

        # Connect to the SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Use TLS (Transport Layer Security) to encrypt the connection

        # Log in to the SMTP server using the sender's credentials
        server.login("kalraprikshit74@gmail.com", "pfcyfrsvnmomqmoz")

        # Send the email
        text = message.as_string()
        server.sendmail("kalraprikshit74@gmail.com", "manoj.hec@gmail.com", text)

        # Close the server connection
        server.quit()

        print("Email sent successfully!")

    except Exception as e:
        print(f"Failed to send email: {e}")


send_email()
