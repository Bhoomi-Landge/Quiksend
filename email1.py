import smtplib
import csv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time

# Replace with your own email settings
SMTP_SERVER = 'email-smtp.ap-south-1.amazonaws.com'
SMTP_PORT = 587
SMTP_USERNAME = ''
SMTP_FROM = ''
SMTP_PASSWORD = ''


# Template for the email message
email_template = """
Hello,

We are from IT support at St. Paul's. Your email and password for the attendance portal are as follows:

Link to the portal :- attendance.stpaulsice.com
Email: {}
Password: {}

Best regards,
IT Support
"""


def send_email(subject, message, recipient_email):
    msg = MIMEMultipart()
    msg['From'] = SMTP_FROM
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(SMTP_FROM, recipient_email, msg.as_string())
        server.quit()
        print("Email sent successfully to", recipient_email)
    except Exception as e:
        print("Error sending email to", recipient_email, ":", e)


def main():
    # Read email data from CSV
    with open('/Users/bhoomilandge/Downloads/credentials - credentials.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            email = row['email']
            password = row['password']

            # Create and send email with the template
            message = email_template.format(email, password)
            send_email("St. Paul's Attendance Portal Credentials", message, email)
            time.sleep(1)  # Add a delay between sending emails to avoid rate limits

            print("Email Sent to:", email)

if __name__ == "__main__":
    main()


