from __future__ import print_function
import gmail
from apscheduler.schedulers.blocking import BlockingScheduler
import json
from datetime import datetime

class EmailInfo:
    def __init__(self,sender, to, title, content, time, attach=None):
        self.sender = sender
        self.to = to
        self.title = title
        self.content = content
        self.time = time
        self.time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
        self.attach = attach
        self.createEmailMessage()

    def createEmailMessage(self):
        if self.attach:
            self.msg = gmail.create_message_with_attachment(self.sender, self.to, self.title, self.content, self.attach)
        else:
            self.msg = gmail.create_message(self.sender, self.to, self.title, self.content)

    def createDraft(self, service, user_id):
        print ("Creating draft")
        self.draft = gmail.create_draft(service, user_id, self.msg)



    def __repr__(self):
        return "EmailInfo: " +  self.sender + " " + self.to + " " + self.title +\
            " " + self.content + " " + self.time.strftime("%Y-%m-%d %H:%M:%S")

def readSetting(file_name):
    with open(file_name, "r") as read_file:
        data = json.load(read_file)

    emails = []
    for reg in data['registerList']:
        print (reg)
        senderList = reg['senders']
        recipient = reg['to']
        content = reg['content']
        title = reg['title']


        for idx, sender in  enumerate(senderList):
            emails += [EmailInfo(sender['from'], recipient, title, content, sender['time'], ["setting.json", 'emailContent.txt'])]
    
    return emails



def send(service, email):
    print ("Send at:", datetime.now())
    gmail.send_draft(service, 'me', email.draft)


if __name__ == "__main__":
    emails = readSetting('setting.json')
    service = gmail.getService()

    for email in emails:
        email.createDraft(service, 'me')
    print (emails[0])
    send(service, emails[0])

    # test add scheduler
    # scheduler = BlockingScheduler()
    # time = emails[0].time
    # scheduler.add_job(send,'cron',args=(service, emails[0]), year=time.year, month=time.month, day=time.day,
    #     hour=time.hour, minute=time.minute, second=time.second)
    # scheduler.start()