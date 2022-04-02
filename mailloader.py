#!/usr/bin/env python
import sys, os, random, re, time
# This is a very memory friendly mailloader. 
# It got a fastmode: This mode is not "real random" as it just picks a random file, opens it, and picks the line after any random byte
#                    -> This is not real random as this prefers "longer addresses" compared to shorter ones. 
#                    -> And ofc the mode completly ignores the fact that maillists might be unequal big. 
# The fastmode=False would be really random, but if you got a huge list, indexing and selecting out of it takes some time. Maybe someone can write a C-Lib?
# Even if not real random, I recommend fastmode=True.

# python3 mailloader.py <amount-of-mails>
regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

class MailLoader:
    def __init__(self, path, fastmode=True):
        self.path = path
        self.files = {} #Key: path, value: amount
        self.fastmode = fastmode
        self._IndxFiles()

    def listdir_nohidden(self, path):
        lst = []
        for f in os.listdir(path):
            if not f.startswith('.'):
                lst.append(f)
        return lst

    def _IndxFiles(self):
        files = self.listdir_nohidden(self.path)
        if(len(files) == 0):
            print("[CRITICAL ERROR] Your maillist folder is empty. Please add a maillist and read the manual. ")
            exit(1)
            
        for file in files:
            fname = os.path.join(self.path, file)
            print("Load maillist:", fname, "...")
            self.files[file] = None
            print("> Loaded", fname)
        return

    def _LoadKindaRandomMailFromDB(self):
        filename = os.path.join(self.path, random.choice(list(self.files.keys())))
        with open(filename, "r") as fp:
            total_bytes = os.stat(filename).st_size 
            random_point = random.randint(0, total_bytes)
            fp.seek(random_point) #Go to a random byte in the file
            fp.readline() #Read until next \n

            # Read another 50 lines and pick a real random one from the list
            # We do that so its a bit more "real random" and more independent from mail addr length
            reallist = []
            line = ""
            for i in range(50):
                line = fp.readline()
                if(line != None):
                    reallist.append(line)
            
            return random.choice(reallist).strip()
        print("Loading Mail failed. ")
        return ""

    def GetMail(self):
        isgood = False
        mail = ""
        while(not isgood):
            mail = self._LoadKindaRandomMailFromDB()
            if(not re.fullmatch(regex, mail)):
                print("Mail did not match regex:", mail)
                continue
            # Add more filters here

            break
        return mail

if __name__ == "__main__":
    mails = 30
    if(len(sys.argv)==2):
        try:
            mails = int(sys.argv[1])
        except:
            print("Expected number of mails")
    ml = MailLoader("maillist/")
    maillist = [ml.GetMail() for i in range(mails)]
    print(maillist)