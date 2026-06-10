# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart

# def send_email_alert(sender_email, sender_password, receiver_email, subject, message):
#     """Sends an email alert."""

#     msg = MIMEMultipart()
#     msg['From'] = sender_email
#     msg['To'] = receiver_email
#     msg['Subject'] = subject

#     msg.attach(MIMEText(message, 'plain')) # Plain text email

#     try:
#         with smtplib.SMTP('smtp.gmail.com', 587) as server: # For Gmail - adjust for other providers
#             server.starttls() # Secure the connection
#             server.login(sender_email, sender_password)
#             server.sendmail(sender_email, receiver_email, msg.as_string())
#         print("Email alert sent successfully!")
#     except Exception as e:
#         print(f"Error sending email: {e}")


import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage  # Import MIMEImage for images
import cv2  # Import cv2 to encode image if needed (or if not already imported in this file)

def send_email_alert(sender_email, sender_password, receiver_email, subject, message, image_path=None, image_data=None):
    """Sends an email alert, optionally with an image attachment."""

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain')) # Plain text email body

    if image_data: # Check if image data is provided
        # Create MIMEImage object using image data
        image = MIMEImage(image_data, name=os.path.basename(image_path) if image_path else 'unknown_face.jpg') # Guess filename if path is given, else generic name
        msg.attach(image) # Attach the image to the email

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server: # For Gmail
            server.starttls() # Secure the connection
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Email alert sent successfully (with image attachment)!")
    except Exception as e:
        print(f"Error sending email with image: {e}")




        #             sender_email = "nkjsr186582@gmail.com"        # <---- REPLACE THIS WITH YOUR GMAIL ADDRESS
        #             sender_password = "urdk ivfz tvdo amrp"  # <---- REPLACE THIS WITH YOUR APP PASSWORD
        #             receiver_email = "naveenkumar186582@gmail.com" # <---- REPLACE THIS WITH YOUR RECIPIENT EMAIL ADDRESS