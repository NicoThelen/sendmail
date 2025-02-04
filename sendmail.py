################################################
## Author: Nico Thelen                        ##
## MIT License                                ##
## www.linkedin.com/in/nico-thelen-5bbb6a289  ##
################################################

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import ssl
import logging
import yaml

# Configure Logging
mail_logger = logging.getLogger('mail')
mail_logger.setLevel(logging.INFO)

# Get config to send mails
def get_mailconfig():
    configYML = os.path.join(os.path.dirname(os.path.realpath(__file__)),'mail_config.yml')    # Specify path to the yml file

    with open(configYML, 'r') as cnfg:
        mailconfig = yaml.safe_load(cnfg)                                           # Reading yml file content

    return mailconfig


# Function to create a connection to the mail server
def connect_server():
    mailconfig = get_mailconfig()
    server = mailconfig["mailserver_config"]["mailserver"]
    port = mailconfig["mailserver_config"]["port"]
    username = mailconfig["credentials"]["username"]
    password = mailconfig["credentials"]["password"]

    try:
        # Establish secure connection
        context = ssl.create_default_context()
        smtp_connection = smtplib.SMTP(server, port)
        smtp_connection.ehlo()
        smtp_connection.starttls(context=context)
        smtp_connection.ehlo()
        smtp_connection.login(username, password) 

        return smtp_connection
    
    except Exception as e:
        logging.error(f'Error creating server connection - {e}')
        return None
    

# Send mail with or without attachment via connected mail server
def send_email(smtp_connection, body, attachment=None):
    mailconfig = get_mailconfig()
    sender = mailconfig["mail_config"]["sender"]
    recipient = mailconfig["mail_config"]["recipient"]
    subject = mailconfig["mail_config"]["subject"]

    try:
        # Configure header
        mail = MIMEMultipart()
        mail['From'] = sender
        mail['To'] = recipient
        mail['Subject'] = subject

        # Configure body
        mail.attach(MIMEText(body, 'plain'))

        # Configure attachment if present
        if attachment:
            part = MIMEBase('application', "octet-stream")
            with open(attachment, 'rb') as file:
                part.set_payload(file.read())   # read report to be sent
            encoders.encode_base64(part)        # encode report/attachment base64
            part.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(attachment)}"')  # set attachment name
            mail.attach(part)                   # add attachment to mail

        # Send mail
        smtp_connection.sendmail(sender, recipient, mail.as_string())
        logging.info(f'Mail sent') 

    except Exception as e:
        logging.error(f'Mail could not be sent - {e}') 
    finally:                                
        smtp_connection.quit()                          # Quit smtp connection
