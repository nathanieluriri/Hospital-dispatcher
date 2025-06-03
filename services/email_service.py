from email_templates.changing_of_password_template import generate_changing_password_email_from_template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr # To properly format sender name and email
import logging
import smtplib

EMAIL_PASSWORD = "1[#|M[N7nNzS"
EMAIL_USERNAME = "test@observer.affiliatemarketing.com.ng"
EMAIL_HOST = "smtp.hostinger.com"

def send_html_email_optimized(
    sender_email: str,
    sender_display_name: str, # Added for display name
    receiver_email: str,
    subject: str,
    html_content: str,
    plain_text_content: str, # Added for plain text alternative
    smtp_server: str,
    smtp_port: int,
    smtp_login: str,
    smtp_password: str
):
    """
    Sends an HTML email with a plain text alternative and a display name.

    Args:
        sender_email: The actual email address of the sender.
        sender_display_name: The name to be displayed as the sender.
        receiver_email: The email address of the recipient.
        subject: The subject of the email.
        html_content: The HTML content of the email body.
        plain_text_content: The plain text equivalent of the email body.
        smtp_server: The SMTP server hostname (e.g., 'smtp.hostinger.com').
        smtp_port: The SMTP server port (e.g., 465 for implicit SSL, 587 for explicit TLS).
        smtp_login: The username for SMTP authentication.
        smtp_password: The password for SMTP authentication (consider using app passwords).
    """

    # 1. Format the sender's "From" header with display name
    # This ensures correct display like "Your Company <your_email@example.com>"
    formatted_from_address = formataddr((sender_display_name, sender_email))

    # 2. Create the email message (MIMEMultipart for HTML + Plain Text)
    msg = MIMEMultipart("alternative")
    msg["From"] = formatted_from_address # Use the formatted address here
    msg["To"] = receiver_email
    msg["Subject"] = subject

    # 3. Attach the plain text part first (important for email clients to prioritize)
    # This also helps with spam filters and accessibility
    plain_part = MIMEText(plain_text_content, "plain")
    msg.attach(plain_part)

    # 4. Attach the HTML part
    html_part = MIMEText(html_content, "html")
    msg.attach(html_part)

    # 5. Connect and send email
    server = None # Initialize server to None
    try:
        if smtp_port == 465:
            # Use SSL directly for port 465 (implicit SSL/TLS)
            server = smtplib.SMTP_SSL(smtp_server, smtp_port)
            print(f"Connecting to SMTP server {smtp_server}:{smtp_port} using SSL.")
        elif smtp_port == 587 or smtp_port == 25:
            # Use regular SMTP and then upgrade to TLS for ports like 587 or 25
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.ehlo() # Identify yourself to the ESMTP server
            server.starttls() # Upgrade connection to secure
            server.ehlo() # Re-identify after starting TLS
            print(f"Connecting to SMTP server {smtp_server}:{smtp_port} using STARTTLS.")
        else:
            print(f"Unsupported SMTP port: {smtp_port}. Please use 465 or 587.")
            raise ValueError("Unsupported SMTP port.")

        server.login(smtp_login, smtp_password)
        print(f"Successfully logged in to {smtp_login}.")
        
        server.sendmail(sender_email, receiver_email, msg.as_string())
        print(f"Email sent successfully to {receiver_email} from {sender_email} (Display: {sender_display_name}).")
  
    except smtplib.SMTPAuthenticationError as e:
        print(f"Authentication failed. Check username and password: {e}")
        raise # Re-raise for caller to handle
    except smtplib.SMTPConnectError as e:
        print(f"SMTP connection failed: {e}")
        raise
    except smtplib.SMTPException as e:
        print(f"An SMTP error occurred: {e}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise
    finally:
        if server:
            server.quit() # Always ensure the connection is closed
            print("SMTP connection closed.")



def send_change_of_password_otp_email(receiver_email:str,otp:str):
    email_body_content = generate_changing_password_email_from_template(otp_code=otp,user_email=receiver_email,avatar_image_link="https://banner2.cleanpng.com/20180330/cue/avicnrp87.webp")
    sender_email = EMAIL_USERNAME
    sender_display_name = "NAT FROM HOSPITAL" # The display name for the sender
    subject = "Reset Password?"
    smtp_server = EMAIL_HOST
    smtp_port = 465 
    smtp_login = EMAIL_USERNAME
    smtp_password = EMAIL_PASSWORD # Use your actual app password/email password here

    try:
      
        email_body_content = email_body_content.replace('<br>','')
        send_html_email_optimized(
        sender_email=sender_email,
        sender_display_name=sender_display_name,
        receiver_email=receiver_email,
        subject=subject,
        html_content=email_body_content,
        plain_text_content=f"Enter this {otp} to log in",
        smtp_server=smtp_server,
        smtp_port=smtp_port,
        smtp_login=smtp_login,
        smtp_password=smtp_password
    )


    except Exception as e:
        print(f"Error sending email: {e}")
        return 1
   