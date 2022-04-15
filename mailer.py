#!/usr/bin/python3
import smtplib, string
from email.mime.text import MIMEText
import datetime, os, configparser, time, random, sys
from mailloader import MailLoader
from textgen import TextGenerator, SubjectGenerator
import requests, base64, json
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.primitives.asymmetric import padding
from colorama import Fore, Back, Style

VERSION = 1.0
EXT_JSON = None
CACHEFILE = ".cachesentc"

class EmailAccount:
    def __init__(self, settings, sectionname):
        self.tempfolder = settings.get("general", 'tempfolder')
        if(not os.path.exists(self.tempfolder)):
            os.mkdir(self.tempfolder)
        self.mail = settings.get(sectionname, 'mail')
        self.password = settings.get(sectionname, 'password')
        self.security = settings.get(sectionname, 'security')
        self.smtp_server = settings.get(sectionname, 'smtp_server')
        self.smtp_port = int(settings.get(sectionname, 'smtp_port'))
        self.mail_limit = int(settings.get(sectionname, 'mail_limit_day'))
        self.sent_today = self.LoadSentToday()

    def GetBrainname(self):
        date_time = datetime.datetime.now()
        return self.tempfolder+self.mail.replace("@", "").replace(".", "")+date_time.strftime("-%Y-%b-%d")+".txt"

    def LoadSentToday(self):
        fname = self.GetBrainname()
        #Create file if not exist
        if(not os.path.exists(fname)):
            f = open(fname, "w+")
            f.write("0")
            f.close()

        # Try open and read
        f = open(fname, "r")
        try:
            return int(f.read())
        except:
            print("Failed parsing:", fname) # We dont care. Will be auto fixed next day.
            return 99999999999999999 #Inf -> Defn over the limit
    
    def LogMailSent(self):
        self.sent_today += 1
        fname = self.GetBrainname()
        f = open(fname, "w+")
        f.write(self.sent_today)
        f.close()
        return

    def FreeMail(self):
        if(self.mail_limit > self.LoadSentToday()):
            return True
        else:
            return False

def SendMail(sender_acc, receiverlist, message, subject):
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = sender_acc.mail
    msg['To'] = ", ".join(receiverlist)
    with smtplib.SMTP(sender_acc.smtp_server, sender_acc.smtp_port) as server:
        if(sender_acc.security.lower() == "tls"):
            server.ehlo()
            server.starttls()
            server.ehlo()
        server.login(sender_acc.mail, sender_acc.password)
        server.sendmail(sender_acc.mail, receiverlist, msg.as_string())
        print("    >> Successfully sent email to", len(receiverlist), "recipients")
    return

# Load Mail-Accs from settings file
def GetMailAccs(settings):
    accs = []
    for mail in [s for s in settings.sections() if "MAIL_" in s]:
        ea = EmailAccount(settings, mail)
        accs.append(ea)

    if(len(accs) == 0):
        print("[CRITICAL] You dont have email accs in your configuration. Please check our instructions on how to setup settings.ini!")
        exit(1)
    return accs

# Test Mails on Startup
def TestMails(mail_accs):
    for sender_acc in mail_accs:
        print("Test access:", sender_acc.mail)
        try:
            with smtplib.SMTP(sender_acc.smtp_server, sender_acc.smtp_port) as server:
                if(sender_acc.security.lower() == "tls"):
                    server.ehlo(); server.starttls(); server.ehlo()
                server.login(sender_acc.mail, sender_acc.password)
                print("      > Successfully logged into", sender_acc.mail)
        except:
            print("      > Failed logging into", sender_acc.mail)
            print("      > Ignore. But please fix. ")

# Verifies if the signation of the JSON is correct
def VerifyContentJSON(jso):
    with open("public.pem", 'rb') as pem_in:
        pemlines = pem_in.read()
    public_key = load_pem_public_key(pemlines)
    content = bytes(str(jso["data"]), "utf-8")
    signature = base64.urlsafe_b64decode(jso["signature"])
    try:
        public_key.verify(
            signature,
            content,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except:
        print("Verify signation of content failed! ")
    return False


# Loading a external .json from all the homeservers specified.
def PullLatestInfo(settings):
    global EXT_JSON
    # check if ppl want to stay fully offline mode
    if(int(settings.get("general", 'statistics')) != 0):
        infolinks_local = settings.get("general", 'home_server').split(";")[1:]
        answers = {}
        #Iterate over all links, check their signation and add them to "answers"
        for link in infolinks_local:
            try:
                resp = requests.get(link, timeout=3)
                sjs = resp.json()
            except:
                print("Failed fetching current_info: ", link)
                continue

            try:
                vnow = sjs["data"]["sourcelist"].split(";")[0]
                if(VerifyContentJSON(sjs)):
                    answers[int(vnow)] = sjs
            except Exception as e:
                print("Failed verify current_info: ", e, link)
        
        if(len(answers) == 0):
            print("Could not receive any current_info! Seems like all our servers are offline or cant be trusted anymore. Use your search engine to look out whats going on. Or deactivate the statistics-mode, to simply ignore it. ")
            exit(1)
            
        EXT_JSON = answers[max(answers.keys())] #Load json with highest version number
        settings.set("general", 'home_server', EXT_JSON["data"]["sourcelist"]) # Update to new homeservers in case of loss
        with open("settings.ini", 'w') as configfile:
            settings.write(configfile)
    else:
        print("[INFO] You run in offline mode")
    return

def LoadSent():
    global CACHEFILE
    c = 0
    if(os.path.exists(CACHEFILE)):
        f = open(CACHEFILE, "r")
        c = int(f.read())
        f.close()
    else: #Set to default
        f = open(CACHEFILE, "w+")
        f.write("0")
        f.close()
    return c

# Record amount of receivers and report to server
# Please do not modify statistics algorithm for obv reason. 
# Obfuscate on purpose
def ReportSent(settings, amount):
    global EXT_JSON
    global CACHEFILE
    c = LoadSent()
    temp = c % 1000
    c = c + amount
    temp2 = c % 1000
    # Report -> (temp2 < temp) -> overflow == "reached 1000 marking"
    if(temp2 < temp and int(settings.get("general", 'statistics')) != 0):
        try:
            # Use not-hardcoded link in case we need to change provider. Not processing request -> Not bad for User Sec. 
            resp = requests.get(str(base64.b64decode(EXT_JSON["data"]["report_1000_link"]+"=="), 'utf-8')+str("#")+str(random.randint(0,99999999999999)))
        except Exception as e:
            print(e)
            print("  > Error reporting 1000")
            time.sleep(10) # #Give user time to read
    
    # Store new result
    f = open(CACHEFILE, "w+")
    f.write(str(c))
    f.close()
    return

def ShowInfoBox():
    # Pulled Info
    print("> Find more info about this tool on https://butterweich.agency")
    global EXT_JSON
    if(EXT_JSON != None):
        key = "show_on_startup"
        try:
            print(EXT_JSON["data"][key])
        except:
            print("Parsing error in", key)
        
        key = "newest_version"
        try:
            print("You run Version:", VERSION)
            v = float(EXT_JSON["data"][key])
            if(v < VERSION): print("[INFO] Your client is outdated. Newest Version is", v, ". Please visit https://butterweich.agency/amb for instructions.")
        except:
            print("Parsing error in", key)
    else:
        print("> Activate 'statistics' to see more info on startup")
    print("Mails already sent:", LoadSent())
    return

def Disclaimer():
    print("This tool is for educational purposes only. Do not use this tool to send uncontrolled and mass emails to unknown people. This is illegal in almost all countries and can be prosecuted by law enforcement agencies.")
    time.sleep(2)
    res = input("\nPress y and confirm with enter if you understand: ")
    if(res.lower() != "y"):
        print("Educating Russians should not be a crime.")
        exit(1)
    return

if __name__ == "__main__":
    ### Init
    settings = configparser.ConfigParser()
    settings._interpolation = configparser.ExtendedInterpolation()
    if(os.path.exists("settings.ini")):
        settings.read('settings.ini')
    else:
        print("[CRITICAL ERROR] You do not have a settings.ini configured. Please configure first and read the manual!")
        exit(1)

    if(int(settings.get("general", 'disable_disclaimer')) != 1):
        Disclaimer()

    #Activate green-on-black
    if(int(settings.get("general", 'green_on_black_style'))): #Give the kids green terminals on black bg <3
        print(Fore.GREEN + Back.BLACK)

    PullLatestInfo(settings)
    print("   Started Anonymous Mail Blaster 2022")
    ShowInfoBox()
    time.sleep(3) #Time to INQ

    #### Actually starting up everything
    print("> Loading Mail Addresses")
    mail_accs = GetMailAccs(settings)
    TestMails(mail_accs)
    print("> Indexing mail-database...")
    ml = MailLoader(settings.get("general", 'mailfolder'))
    print("> Loading Grammar...")
    tg = TextGenerator(settings.get("general", 'grammarsfolder'), int(settings.get("general", 'max_words_mail')))
    sg = SubjectGenerator(settings.get("general", 'subjectsfolder'))
    print("> Loaded Grammar!")

    print("> Now start sending!")
    try:
        while True:
            time.sleep(1)
            daily_limit_reached = True
            for account in mail_accs:
                print("> Logging into account: ", account.mail)
                if(account.FreeMail()):
                    daily_limit_reached = False
                    print("  > Generating new Text")
                    mail, translation = tg.GenerateText("ru")
                    subject = sg.GenerateSubject()
                    min_recv = int(settings.get("general", 'rec_per_mail_min'))
                    max_recv = int(settings.get("general", 'rec_per_mail_max'))
                    print("  > Selecting random receivers from DB")
                    receiver = [ml.GetMail() for i in range(random.randint(min_recv,max_recv))]

                    # Allows user to review mail if wanted
                    if(int(settings.get("general", 'review_before_sending'))==1):
                            print("-------------------------- Please review this text --------------------------------- ")
                            print(mail)
                            print("               --------------- English Translation ----------------- ")
                            print(translation)
                            print("\n Receivers:", "; ".join(receiver))
                            print("------------------------------- END OF MAIL ---------------------------------------- ")
                            if(input("Do you like to send this mail? ('Y'=Yes, 'N'=No)").lower() != "y"):
                                print("Does not send mail... Load next!")
                                continue 

                    print("  > Sending...")
                    try:
                        SendMail(account, receiver, mail, subject)
                        ReportSent(settings, len(receiver))
                    except: 
                        print("    > Sending mail failed")
                        receiver = []
            
            if(daily_limit_reached): #Just sleep 6 to 16 hours randomly
                print("> Reached limit for today. Wait until tomorrow :) ")
                time.sleep(random.randint(60*60*6, 60*60*16))
            print("> Iteration Done. Mails sent:", LoadSent())

            if(int(settings.get("general", 'review_before_sending'))!=1):
                print("> Sleeping 60-120 seconds...")
                time.sleep(random.randint(60,120))

    except KeyboardInterrupt:
        print(Style.RESET_ALL)
        exit(0)