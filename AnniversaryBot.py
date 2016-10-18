import os,time, csv
import urlparse, urllib
from slackclient import SlackClient
from TEKServiceAnniversary import TEKServiceAnniversary

BOT_NAME = 'anniversarybot'
SLACK_BOT_TOKEN = 'xoxb-88193568502-M1qqQYkCSnx6p0omz0Js2aON'
slack_client = SlackClient(SLACK_BOT_TOKEN)
BOT_ID = 'U2L5PGQES'

# constants
AT_BOT = "<@" + BOT_ID + ">:"
EXAMPLE_COMMAND = "do"
CH_ID = 'C1Y7S3YD6'
#User Id Dictionary
User_ref=dict()

def get_user_list():
    User = slack_client.api_call('users.list').get('members')
    for u in User:
        User_det = u.get('profile')
        User_id = u.get('id')
        print User_det['first_name']+" "+User_det['real_name']+" "+User_id
        User_ref[User_id]=User_det['real_name']
def handle_command(command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    response = "Not sure what you mean. Use the *" + EXAMPLE_COMMAND + \
               "* command with numbers, delimited by spaces."
    if command.startswith(EXAMPLE_COMMAND):
        response = "Sure...write some more code then I can do that!"
    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)
def retrieve_history():
    msg = slack_client.api_call('channels.history',channel=CH_ID)
    message = msg.get('messages')
    for m in message:
        print User_ref[m.get('user')]+" "+m.get('text')
    

def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']
    return None, None

num = {1:'one',2:'two',3:'three',4:'four',5:'five',6:'six',7:'seven',8:'eight',9:'nine',10:'ten',11:'eleven',12:'twelve',13:'thirteen',14:'fourteen',15:'fifteen'}
#img = {1:"http://imgur.com/Gnbne3e.jpg",2:"http://imgur.com/zjXOMkq.jpg",3:"http://imgur.com/fKEgwUt.jpg",4:"http://imgur.com/HQRxGNL.jpg",5:"http://imgur.com/t2zLPbQ.jpg",6:"http://imgur.com/e9tgWf1.jpg",7:"http://imgur.com/BXuP3TJ.jpg",8:"http://imgur.com/4hOlJ0C.jpg",9:"http://imgur.com/oLhPTfm.jpg",10:"http://imgur.com/AgtQDTR.jpg"}

def getImgs():
    origpath = os.path.dirname(os.path.realpath(__file__))
    mypath = origpath+'/Images/'
    dirfiles = [f for f in os.listdir(origpath) if os.path.isfile(os.path.join(origpath, f))]
    imgfiles = [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]
    #Bring in Excel Format
    csv.register_dialect(
    'mydialect',
    delimiter = ',',
    quotechar = '"',
    doublequote = True,
    skipinitialspace = True,
    lineterminator = '\r\n',
    quoting = csv.QUOTE_MINIMAL)
    if('track.csv' not in dirfiles):
        flg=True
        with open('track.csv', 'wb') as trackfile:
            thedatawriter = csv.writer(trackfile, dialect='mydialect')
            thedatawriter.writerow(['FILE NAME', 'STATUS'])
            for row in imgfiles:
                if(flg):
                    thedatawriter.writerow([row,'Used'])
                    imgFile=mypath+row
                    flg=False
                else:
                    thedatawriter.writerow([row,'Not Used'])
    else:
        newdata = list()
        done=True
        status=list()
        imgFile=''
        with open('track.csv', 'rb') as trackfile:
            dictofdata = csv.DictReader(trackfile, dialect='mydialect')
            for row in dictofdata:
                status.append(row['STATUS'])
                if(row['STATUS']=='Not Used' and done):
                    newdata.append([row['FILE NAME'],'Used'])
                    imgFile=mypath+row['FILE NAME']
                    done=False
                else:
                    newdata.append([row['FILE NAME'],row['STATUS']])
            if(all(x=='Used' for x in status)):
                newdata = list()
                flg=True
                with open('track.csv', 'rb') as trackfile:
                    dictofdata = csv.DictReader(trackfile, dialect='mydialect')
                    for row in dictofdata:
                        if(flg):
                            newdata.append([row['FILE NAME'],'Used'])
                            imgFile=mypath+row['FILE NAME']
                            flg=False
                        else:
                            newdata.append([row['FILE NAME'],'Not Used'])
        with open('track.csv', 'wb') as trackfile:
            thedatawriter = csv.writer(trackfile, dialect='mydialect')
            thedatawriter.writerow(['FILE NAME', 'STATUS'])
            for row in newdata:
                thedatawriter.writerow(row)
    return imgFile

def path2url(path):
    return urlparse.urljoin(
      'file:', urllib.pathname2url(path))

#from PIL import Image


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    #ch = slack_client.api_call("channels.list")
    #get_user_list()
    #retrieve_history()
    obj=TEKServiceAnniversary()
    if slack_client.rtm_connect():
        print("anniversarybot connected and running!")
        img = getImgs()
        """img1 = Image.open(img)
        img1.show()"""
        print path2url(img)
        details = obj.getServiceAnniversary()
        if(details!=None):
            #print slack_client.api_call('channels.history',channel = CH_ID)
            nick = details[1].split('@')[0]
            years=details[3]
            attach = '[{"fields": [{"title": ""}],"image_url": "'+path2url(img)+'"}]'
            message = "Cheers @"+nick+" for completion of "+num[years]+" "+["years","year"][years==1]+" with TEKsystems. Congratulations and keep up the good work !! :+1:"
            print slack_client.api_call("chat.postMessage", channel=CH_ID,
                              text=message, as_user=True, attachments=attach)
        """while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)"""
    
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
