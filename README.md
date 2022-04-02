Please connect with us on social media for annoucements and infosharing! \
[https://butterweich.agency](https://butterweich.agency) \
[![Twitter URL](https://img.shields.io/twitter/url/https/twitter.com/BWA_Lead.svg?style=social&label=Follow%20%40BWA_Lead)](https://twitter.com/BWA_Lead)\
[Join our Discord to exchange tips and tricks](https://discord.gg/vv5JdRs62Z)

# Внимание: НЕ ИСПОЛЬЗУЙТЕ ЭТУ УТИЛИТУ, если вы находитесь в России, на территории контролируемой Россией или имеете причины опасаться российского наблюдения. Эта утилита вашу задницу не скрывает!

# AnonMailBlaster - General Info 
A open-source free-to-use python-based tool to send unique emails to close Russian friends fully automatically. Consists of a memory-friendly mailloader module, a textgenerator than can generate text based on grammar and finally mailer.py, which uses these modules to send your mails. 

### Disclaimer
This tool is for educational purposes only. Do not use this tool to send uncontrolled and mass emails to unknown people. This is illegal in almost all countries and can be prosecuted by law enforcement agencies. Educational purposes only! Educate your personal Russian friends (with their consent, of course)!
We do not 

### Your help needed!
Please support each other getting this running everywhere. I would really appreciate if someone can do a YouTube Video on how to set it up. Send it to me. If its good, I link it here. 

### Read before using #OpSec
This tool is using a standard secure socket layer connection to report every 1000th mail you wrote. So we know how many people we have helped with this tool. It only sends a "ping" - nothing else (especially nothing sensitive) is transmitted. I dont see an issue with your internet connection using a web-based-counter. You could have used that counter in any application - does therefore not prove anything.
BUT if you don't want me to enjoy the success of my tool, set the "statistics" option to 0. This will disable all non-SMTP connections. Of course I understand if you very much depend on your privacy. Especially if you live in a censored country. Btw this tool should be compatible with any system-VPN you got.

Also make sure to not use any private sensitive email account with this tool. Storing passwords as plain text is NOT safe. We recommend either creating one/some free ones (gmail.com, mail.com, outlook.com, ...) or if u are into tech you can setup your own SMTP-server. \
\
We (BWA) will never ask you for Admin-Permission. We never ask you to download and install and executable. Every file we ever give you is in plain-text format (like python scripts) and open-source for your own security. The plain-text format ensures that you can actually see what the script is doing when executed. The "open-source" ensures that coders can verify the source-code and proof that it is not dangerous. Do not just download and run python-scripts (.py) from anywhere, just because they say "AnonMailBlaster better version". [More Info about how we safe your ass](https://butterweich.agency/#whatwestandfor)

### Maillists and Grammar
This tool uses datasets which you need to find yourself: Maillists, which are ".txt" files that contain a email-address every line. 

### How to install? 
(We wont explain how to install Python3 on every OS. Just google it and use official sources only! Its for your safety and our laziness) \
\
Step 1: On the top right click Code > "Download Zip" \
Step 2: Unpack the folder to somewhere \
Step 3: Download and Install Python 3.10 (Windows users, you can find it in Microsoft Store) \
Step 4: If you want "green-font-on-black-background"-terminal run "pip install colorama" in your command line to install the colorama module. \
Step 5: Go to your AnonMailBlaster Folder and rename settings.ini.temp in settings.ini \
Step 6: Right click settings.ini and open with any text editor. Please review title "settings.ini" for more info \
Step 7: At [MAIL_1] enter your first mail, password and smtp settings. DO NOT USE A PRIVATE MAIL! Default smtp-settings is google. \
Step 8 Optionally add as many accs as you want by copy-pasting the "MAIL_" section. Dont forget to give it different numbers "MAIL_1", "MAIL_2",... \
Step 9: Download mail-dataset, subject-dataset and grammar. Put txt-maildataset in "maillist" folder and grammar-tsv in "grammars"-folder. Subject-tsv ofc in subject folder. \
--> Done. Now just call the mailer.py and let it do its job.

### settings.ini
The settings.ini file is your personal configuration file. If the program crashes for any reasons, your first try should be to download a fresh settings.ini.temp file, configure it again and test again. Some settings are boolean settings like "statistics", "green_on_black_style", "disable_disclaimer" or "review_before_sending". If you set their value to 1, they will be activated. 0 is deactivates. Anything else is unexpected behaviour. \
\
I recommend you to now change any folder settings. Do never change home_server!! This updates itself if needed. \

You can copy and paste multiple MAIL_ sections in one file. The tool will test all of them and use the functional ones. We do not recommend to change rec_per_mail_ settings if you dont know what you do. 

# Mail Accounts Discussion

### GMAIL.COM
For gmail, make sure you activated SMTP by activating what Google calls insecure apps. You can do this here: https://myaccount.google.com/lesssecureapps
Google is right, SMTP can be hacked easier. Another reason to not use your personal sensitive gmail account

### Protonmail
Protonmail needs a client to get SMTP working. Noone of us tried yet. Tell us if it worked. 

### Self-hosted vs Provider
Generally you got 2 options: Either register a mail-accoount at a provider (like gmail.com) with SMTP support, or create your own SMTP server with some tutorials. \
\
Your own SMTP server will not limit you. You can send as many mails as you want. BUT its not super easy to set it up the right way. Maybe someone could write some instructions for that? \
Please be aware that a Hosting-Webspace is normally limited in the amount of mails you can send. Try the limit urself, your hoster will tell you if you reached it. \
\
A email account at a bigger provider like gmail.com is created in a few minutes and allows you sending up to 100 mails with up to 30 recipients per day (2100 receiver per week - not sure how many friends u got but...). We however recommend putting it to 50 mails with 30 receivers per day, so gmail does not mistakenly assumes you would be a spammer.

### How to find SMTP settings? 
We will add a list of common services-SMTPs soon, but basically you just need to search the internet for "smtp settings <provider>". For example 
you could search for "smtp settings outlook.com" and you will find a SMTP Server and a SMTP Port. The tool will tell you on startup if logging in worked
or not. Gmail.com for sure works. Some providers like protonmail want to install you a extra application for it. We dont recommend to do it. \
\
If you are not broke and got a basic understanding of tech, you could consider setting up your own SMTP servers. Send me some instructions if you find some good one. 

# I am a Developer/Designer/RU-Translator and want to help
Join our Discord and explain your skillset. If available, feel free to add ideas on how you would like to help us. We would really like to take this on the next level! Especially every skilled coder is welcome - independent of languages. 