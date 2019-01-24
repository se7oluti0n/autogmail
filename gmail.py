from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart, MIMEBase
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio

from mimetypes import MimeTypes
import base64
from apiclient import errors
import os


SCOPES = [
            'https://www.googleapis.com/auth/gmail.readonly',
            'https://www.googleapis.com/auth/gmail.compose',
            'https://www.googleapis.com/auth/gmail.send'
]

TOKEN_FILE = 'token.json'
CREDENTIAL_FILE = 'secret.json'

def create_message(sender, to, subject, message_text):
    """Create a message for an email.

    Args:
        sender: Email address of the sender.
        to: Email address of the receiver.
        subject: The subject of the email message.
        message_text: The text of the email message.

    Returns:
        An object containing a base64url encoded email object.
    """
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    return {'raw': base64.b64encode(message.as_bytes()).decode('UTF-8')}

def create_message_with_attachment(
    sender, to, subject, message_text, files):
  """Create a message for an email.

  Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.
    file: The path to the file to be attached.

  Returns:
    An object containing a base64url encoded email object.
  """
  message = MIMEMultipart()
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject

  msg = MIMEText(message_text)
  message.attach(msg)

  mime = MimeTypes()

  for file in files:
    content_type, encoding = mime.guess_type(file)
    if content_type is None or encoding is not None:
      content_type = 'application/octet-stream'
    main_type, sub_type = content_type.split('/', 1)
    if main_type == 'text':
      fp = open(file, 'r')
      msg = MIMEText(fp.read(), _subtype=sub_type)
      fp.close()
    elif main_type == 'image':
      fp = open(file, 'rb')
      msg = MIMEImage(fp.read(), _subtype=sub_type)
      fp.close()
    elif main_type == 'audio':
      fp = open(file, 'rb')
      msg = MIMEAudio(fp.read(), _subtype=sub_type)
      fp.close()
    else:
      fp = open(file, 'rb')
      msg = MIMEBase(main_type, sub_type)
      msg.set_payload(fp.read())
      fp.close()
    filename = os.path.basename(file)
    msg.add_header('Content-Disposition', 'attachment', filename=filename)
    message.attach(msg)

  return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode('UTF-8')}

def create_draft(service, user_id, message_body):
  """Create and insert a draft email. Print the returned draft's message and id.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message_body: The body of the email message, including headers.

  Returns:
    Draft object, including draft id and message meta data.
  """
  try:
    message = {'message': message_body}
    draft = service.users().drafts().create(userId=user_id, body=message).execute()

    print ('Draft id: %s\nDraft message: %s' % (draft['id'], draft['message']))

    return draft
  except errors.HttpError as error:
    print ('An error occurred: %s' % error)
    return None


def send_draft(service, user_id, draft):
    try:
        message = (service.users().drafts().send(userId=user_id, body=draft)
                .execute())
        print ('Message Id: %s' % message['id'])
        return message
    except errors.HttpError as error:
        print ('An error occurred: %s' % error)

def send_message(service, user_id, message):
    """Send an email message.

    Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address. The special value "me"
        can be used to indicate the authenticated user.
        message: Message to be sent.

    Returns:
        Sent Message.
    """
    try:
        message = (service.users().messages().send(userId=user_id, body=message)
                .execute())
        print ('Message Id: %s' % message['id'])
        return message
    except errors.HttpError as error:
        print ('An error occurred: %s' % error)

def getService(scopes=SCOPES):
    store = file.Storage(TOKEN_FILE)
    creds = store.get()
    if not creds or creds.invalid:
        print ("Failed to get token, load from file")
        flow = client.flow_from_clientsecrets(CREDENTIAL_FILE, scopes)
        creds = tools.run_flow(flow, store)

    service = build('gmail', 'v1', http=creds.authorize(Http()))

    return service

def getLabels():
    """Show basic use of Gmail API
    Lists the user's Gmail labels
    """
    service = getService(SCOPES)

    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])

    if not labels:
        print ('No label found.')
    else:
        print ('Labels:')
        for label in labels:
            print(label['name'])

def sendEmail():
    service = getService(SCOPES)
    msg = create_message("manhtt@relipasoft.com", "manhattan.vn@gmail.com", "Test email", "Hello darkness, my old friend")
    send_message(service, 'me', msg)


if __name__ == "__main__":

    sendEmail()
    # main()