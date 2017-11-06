import smtplib
from email.message import EmailMessage
from yaml_reader import get_config

#This script requires a yaml config file with the following dict:
_email_settings_name = "email_settings"

def send_email(subject, message_body, config_file_path):
    '''
    Create an email message using pythons smtplib and EmailMessage.
    It returns a dictionary, with one entry for each recipient that was
    refused. Each entry contains a tuple of the SMTP error code and the
    accompanying error message sent by the server.

    Args:
    subject: a string for the subject line
    message_body: a string for the email message body
    config_file_path: a path to a yaml settings file
        the email_settings is a dictionary with the following keys:
        host: the host that is sending the emails
        port: the port required to send emails through
        from_email: who the email is coming from
        to_emails: either a string or list of email address being sent to
    '''
    configs = get_config(config_file_path, _email_settings_name)
    msg = __create_message(subject, message_body, configs)
    return __send(msg, configs)

def __connect_to_smtp(configs):
    '''
    Using Django settings and smtplib, create an smtplib SMTP instance
    https://docs.python.org/3/library/smtplib.html#smtplib.SMTP
    '''
    try:
        connection = smtplib.SMTP(host=configs['host'],
                                  port=configs['port'],)
    except smtplib.SMTPConnectError as err:
        print(err)
        connection = None
    return connection

def __send(message, configs):
    connection = __connect_to_smtp(configs)
    failures = {}
    try:
        failures = connection.send_message(message)
    except smtplib.SMTPRecipientsRefused as err:
        #If no emails are sent
        failures = err.recipients
    connection.quit()
    return failures

def __create_message(subject, message_body, configs):
    '''
    Take the subject, message body, from email, and to emails list and create
    a message object to send off.
    '''
    msg = EmailMessage()
    msg.set_content(message_body)
    msg['Subject'] = subject
    msg['From'] = configs['from_email']
    msg['To'] = __get_list(configs['to_emails'])
    return msg

def __get_list(string_or_list):
    '''
    Take a string and return a list
    '''
    if isinstance(string_or_list, list):
        return string_or_list
    try:
        return string_or_list.split()
    except AttributeError:
        return []
