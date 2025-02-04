# Sendmail

## Description
This script is intended to function as a library. It only works as an import into another tool and can take over the task of sending E-Mails. \
This library is used in the following tool and sends alerts by E-Mail: https://github.com/NicoThelen/Phishing-Monitor

## Notes and Preparations
The data required for sending E-Mails must be provided to the script as a config file `"mail_config.yml"`. \
The script reads these as required. The following information must be included:
* Mailserver
* Port
* Sender
* Recipient
* Subject 
* Username
* Password

As this information is read in again each time, it is possible to dynamically adapt the E-Mail configuration during the runtime of the “main program”

## Functionality
Use `"import sendmail"` in your script and call up the functions as follows: 

* Establishing the connection to the server: `"sendmail.connect_server()"`
  * returns an object that is required for the second function and enables an error check
* Sending the e-mail with attachment: `"sendmail.send_email(server, msg, file)"` 
  * server = returned server object from the connect_server() function
  * msg = Message that represents the e-mail content as string
  * file = Path to the file to be sent
* Sending the e-mail without attachment: `"sendmail.send_email(server, msg)"` 
  * server = returned server object from the connect_server() function
  * msg = Message that represents the e-mail content as string

**Example**
```python
server = sendmail.connect_server()  # Establish mail server connection
if server:
  sendmail.send_email(server, msg)  # Send mail
```
