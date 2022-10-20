# -*- coding: utf-8 -*- 
#####################################################
#    Project:     RFID with online Source           #
#    Programmer:  Sina Shiry                        #
#    Date:        2016 Nov 19                       #
#    For:         Fanavard Contest                  #
#####################################################

#####___Import Modules___#####     
import RPi.GPIO as GPIO		
from Tkinter import *
import tkFont
import PIL
from PIL import Image
import time
import os
import os.path
import urllib
import serial
import jdatetime
import string
from datetime import datetime

print "Wait for Network"
time.sleep(3)


#_Check_THE_FIRST_EXECUTE_OF_PROGRAM_#
first = os.path.isfile('First_Execute')
if first ==False:
	open('First_Execute','w')
	print "FIRST EXECUTE"

#_INSTALL_NEEDED_LIBRARIES_#
if first==False:
	print "Installing Libaries:"
	print "####################################"
	os.system("sudo aptitude install python-imaging")
	os.system("sudo apt-get install python-serial")
	os.system("sudo apt-get install python-ntplib")
	os.system("sudo pip install jdatetime")
	print "####################################"
	print "Libraries...OK"
	print "Copy Fonts"
	os.system("sudo cp -r /home/pi/FanAvard/Font/BTitrBd.ttf /usr/local/share/fonts")
	os.system("sudo cp -r /home/pi/FanAvard/Font/BTraffic.ttf /usr/local/share/fonts")
	print "Fonts...ok"

#__Setup_TimeZone__#
os.environ['TZ'] = ':Iran'; time.tzset()
#_Setup_GPIOs_Communication__#
print "Installing GPIOs"
LED_RD = 27
LED_GN = 22
IN_REL = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_RD,GPIO.OUT)
GPIO.setup(LED_GN,GPIO.OUT)
GPIO.setup(IN_REL, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.output(LED_RD,False)
GPIO.output(LED_GN,False)
print "GPIOs...OK"

#_Setup_Serial_Communication_#
print "Installing Serial Port"
serial_number = serial.Serial('/dev/ttyAMA0', 9600, timeout = 10)
serial_number.close()
print "Serial Port...OK"
#__Data_From_Server_and_..._#
#_Get_File_Name_#
#_Get_DATE
FILE_NAME = datetime.strftime(datetime.now(), '%Y-%m-%d')
#_Get_HOUR
HOUR = int(datetime.strftime(datetime.now(),'%H'))
if HOUR<14 and HOUR>11:
	FILE_NAME = FILE_NAME + "_1.txt"
elif (HOUR<21 and HOUR>18):
	FILE_NAME = FILE_NAME + "_2.txt"
else:
	FILE_NAME = FILE_NAME + "_1.txt"
	#print "For Time Limitation,We Can't Execute Program"
	#while True:
	#	time.sleep(2)
#_Create_LINK_and_File_Location
#print FILE_NAME
LINK_NAME = "http://www.pro.uploadpa.com/?file=1479802235245885_" + FILE_NAME
#print LINK_NAME
FILE_Location = "/home/reserves/" + FILE_NAME
#_Get_Data_From_Server_#
print "Get Data From Server"
testfile=urllib.URLopener()
testfile.retrieve(LINK_NAME,FILE_Location)
print "Data Recieved...OK"
#_Get_Saved_file_#
opened_file = open(FILE_Location)
person_names = opened_file.read()
opened_file.close()
print "File Saved...OK"
#_Count_Resereved_Persons_#
NUM_OF_RESERVED = len(person_names.split('\n'))

#________Variables_________#
Gived_person = ""
NUM_OF_NOW = 0
delete_flag = 0

#####_____Functions_____#####

##__DATE_IN_PERSIAN__##
months_FA = {'Far':'فروردین',
		'Ord':'اردیبهشت',
		'Kho':'خرداد',
		'Tir':'تیر',
		'Mor':'مرداد',
		'Sha':'شهریور',
		'Meh':'مهر',
		'Aba':'آبان',
		'Aza':'آذر',
		'Dey':'دی',
		'Bah':'بهمن',
		'Esf':'اسفند'}
def DATE_MONTH_FA(months):
	months = months_FA[months]
	return months		
days_FA = {'Sat':'شنبه',
		'Sun':'یشنبه',
		'Mon':'دوشنبه',
		'Tue':'سه شنبه',
		'Wed':'هارشنبه',
		'Thu':'نجشنبه',
		'Fri':'جمعه'}
def DATE_DAY_FA(day):
	days = days_FA[days]
	return days
#___Convert_Numbers___#
numbers = {'0':'۰','1':'۱','2':'۲','3':'۳','4':'۴','5':'۵','6':'۶','7':'۷','8':'۸','9':'۹'}
def EN_2_PR(NUM):
	NUM = str(NUM)
	NUM_l=list(NUM)
	for i in range(0,len(NUM)):
		NUM_l[i] = str(numbers[NUM[i]])
	ss = "".join(NUM_l)
	return ss
#_Search_Person_Gived_#
def search_gived(person):
	global Gived_person
	find = False
	if person in Gived_person:
		find = True
	return find
#_Search_Person_in_File_#
def search_person(person):
	global person_names
	global Gived_person
	find = False
	if person in person_names:
		find = True
		person_names = string.replace(person_names, person, '----------')
		Gived_person = Gived_person + person + "\n"
	return find
#__Reserved_mode__#	
def clear_func_Reserved(Reserved_img):
	os.system("aplay /home/pi/FanAvard/Tones/Pass.wav")
	time.sleep(1)
	w.delete(Reserved_img)
	GPIO.output(LED_GN,False)
#_NotReserved_mode_#		
def clear_func_Not_Reserved(Not_Reserved_img):
	os.system("aplay /home/pi/FanAvard/Tones/Error.wav")
	#time.sleep(4)
	w.delete(Not_Reserved_img)
	GPIO.output(LED_RD,False)
def clear_func_Gived(Gived_img):
	os.system("aplay /home/pi/FanAvard/Tones/Error.wav")
	w.delete(Gived_img)
	GPIO.output(LED_RD,False)
	GPIO.output(LED_GN,False)
def clear_func_Finish(Finish_img):
	os.system("aplay /home/pi/FanAvard/Tones/Error.wav")
	w.delete(Finish_img)
#_Exit_#
def quit_def():
	global Gived_person
	global person_names
	print "Gived:"
	print Gived_person
	print "Global:"
	print person_names
	GPIO.cleanup()
	root.destroy()
	sys.exit()
#######__Start__#######
#_Create_GUI_#
root = Tk()
screenx = root.winfo_screenwidth()
screeny = root.winfo_screenheight()
root.overrideredirect(True)
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
w = Canvas(root,width=screenx,height=screeny)
w.grid(row = 0, column = 0)
#_Create_font_#
BTitr = tkFont.Font(family ="B Traffic",size=60,weight="bold")
TIME_Font = tkFont.Font(family="B Traffic",size=15,weight="bold")
#__Resize_Pics__#
print "Resizing Pictures"
if first==False:
	#this Section execute Only one time when We use program for first time
	os.system('sudo mkdir /home/pi/FanAvard/Pics_Resized')
	#Reserved.PNG
	img = Image.open('/home/pi/FanAvard/Pics/Reserved.png')
	img = img.resize((screenx/4,screeny/6), PIL.Image.ANTIALIAS)
	img.save('/home/pi/FanAvard/Pics_Resized/Reserved_1.png')
	#Not_Reserved.PNG
	img = Image.open('/home/pi/FanAvard/Pics/Not_Reserved.png')
	img = img.resize((screenx/4,screeny/6), PIL.Image.ANTIALIAS)
	img.save('/home/pi/FanAvard/Pics_Resized/Not_Reserved_1.png')
	#Gived.PNG
	img = Image.open('/home/pi/FanAvard/Pics/Gived.png')
	img = img.resize((screenx/4,screeny/5), PIL.Image.ANTIALIAS)
	img.save('/home/pi/FanAvard/Pics_Resized/Gived_1.png')
	#Exit.PNG
	img = Image.open('/home/pi/FanAvard/Pics/Exit.png')
	img = img.resize((screenx/10,screeny/15), PIL.Image.ANTIALIAS)
	img.save('/home/pi/FanAvard/Pics_Resized/Exit_1.png')
	#Reserve_Status.PNG
	img = Image.open('/home/pi/FanAvard/Pics/Reserve_Status.png')
	img = img.resize((screenx/10,screeny/10), PIL.Image.ANTIALIAS)
	img.save('/home/pi/FanAvard/Pics_Resized/Reserve_Status_1.png')
	#Reserve_Total.PNG
	img = Image.open('/home/pi/FanAvard/Pics/Reserve_Total.png')
	img = img.resize((screenx/10,screeny/10), PIL.Image.ANTIALIAS)
	img.save('/home/pi/FanAvard/Pics_Resized/Reserve_Total_1.png')
	#Reserve_Now.PNG
	img = Image.open('/home/pi/FanAvard/Pics/Reserve_Now.png')
	img = img.resize((screenx/10,screeny/10), PIL.Image.ANTIALIAS)
	img.save('/home/pi/FanAvard/Pics_Resized/Reserve_Now_1.png')
	#custmer_Information.PNG
	img = Image.open('/home/pi/FanAvard/Pics/custmer_Information.png')
	img = img.resize((screenx/4,screeny/6), PIL.Image.ANTIALIAS)
	img.save('/home/pi/FanAvard/Pics_Resized/custmer_Information_1.png')
	#Company_Information.PNG
	img = Image.open('/home/pi/FanAvard/Pics/Company_Information.png')
	img = img.resize((screenx/4,screeny/6), PIL.Image.ANTIALIAS)
	img.save('/home/pi/FanAvard/Pics_Resized/Company_Information_1.png')
	#Information.PNG
	img = Image.open('/home/pi/FanAvard/Pics/Information.png')
	img = img.resize((screenx/10,screeny/10), PIL.Image.ANTIALIAS)
	img.save('/home/pi/FanAvard/Pics_Resized/Information_1.png')
	#Finish.PNG
	img = Image.open('/home/pi/FanAvard/Pics/Finish.png')
	img = img.resize((2*screenx/3,screeny/3), PIL.Image.ANTIALIAS)
	img.save('/home/pi/FanAvard/Pics_Resized/Finish_1.png')
	#########################
	#_RESIZE_PERSON_PHOTOs_#
	os.system('sudo mkdir /home/pi/FanAvard/Faces_Resized')
	opened_file = open("/home/pi/FanAvard/All_Students.txt", 'r')
	person_Photos = opened_file.read()
	opened_file.close()
	for line in person_Photos.splitlines():
		photo_location = '/home/pi/FanAvard/Faces/'+line+'.png'
		img = Image.open(photo_location)
		img = img.resize((screenx/10,screeny/10+screeny/20), PIL.Image.ANTIALIAS)
		photo_location = ""
		photo_location = '/home/pi/FanAvard/Faces_Resized/'+line+'.png'
		img.save(photo_location)
		
			
print "Resize Process...OK"
#_Import_Pics_#
print "Create GUI"
Reserved = PhotoImage(file='/home/pi/FanAvard/Pics_Resized/Reserved_1.png')
Not_Reserved = PhotoImage(file='/home/pi/FanAvard/Pics_Resized/Not_Reserved_1.png')
Gived = PhotoImage(file='/home/pi/FanAvard/Pics_Resized/Gived_1.png')
Exit = PhotoImage(file='/home/pi/FanAvard/Pics_Resized/Exit_1.png')
Reserve_Status = PhotoImage(file='/home/pi/FanAvard/Pics_Resized/Reserve_Status_1.png')
Reserve_Total = PhotoImage(file='/home/pi/FanAvard/Pics_Resized/Reserve_Total_1.png')
Reserve_Now = PhotoImage(file='/home/pi/FanAvard/Pics_Resized/Reserve_Now_1.png')
Information = PhotoImage(file='/home/pi/FanAvard/Pics_Resized/Information_1.png')
Finish = PhotoImage(file='/home/pi/FanAvard/Pics_Resized/Finish_1.png')
custmer_Information = PhotoImage(file='/home/pi/FanAvard/Pics_Resized/custmer_Information_1.png')
Company_Information = PhotoImage(file='/home/pi/FanAvard/Pics_Resized/Company_Information_1.png')
#_BackGround_#
w.create_rectangle(0,0,screenx,screeny, fill="White")
#_Exit_Button_#
button1 = Button(root, text = "Quit", command = quit_def, anchor = W)
button1.configure(image=Exit,width = screenx/10,height = screeny/15, relief = FLAT)
button1_window = w.create_window(10, 10, anchor=NW, window=button1)
#_Align_Pics_#
w.create_image(screenx/2,screeny/12, image = custmer_Information)
w.create_image(screenx/8,(5*screeny/6)+(screeny/12), image = Company_Information)
w.create_image((9*screenx/10),(2*screeny/10), image = Reserve_Status)
w.create_image((4*screenx/10),(3*screeny/10), image = Reserve_Now)
w.create_image((4*screenx/10),(6*screeny/10), image = Reserve_Total)
w.create_image((9*screenx/10),(6*screeny/10), image = Information)
#_Text(s)_#
w.create_text((2*screenx/10),(7*screeny/10),text=EN_2_PR(NUM_OF_RESERVED),font=BTitr)
TIME_img = w.create_text((8*screenx/10),(9*screeny/10),text=jdatetime.datetime.now().strftime("%Y %b %d  %H:%M:%S"),font = TIME_Font)
print "GUI...ok"
####################################################
################______Main______####################
####################################################
Status = ""

def readSerial():
	global Status
	global photo
	global person_photo
	global Reserved_img
	global Not_Reserved_img
	global Gived_img
	global Finish_img
	global delete_flag
	global NUM_OF_NOW_img
	global NUM_OF_NOW
	global NUM_OF_RESERVED
	global datetime
	global TIME_img
	# Date and Time
	w.delete(TIME_img)
	TIME_img = w.create_text((8*screenx/10),(9*screeny/10),text=jdatetime.datetime.now().strftime("%Y %b %d  %H:%M:%S"),font = TIME_Font)
	if Status == "GIVED":
		clear_func_Gived(Gived_img)
		w.delete(person_photo)
		Status = ""
	if Status == "RESERVED":
		clear_func_Reserved(Reserved_img)
		w.delete(person_photo)
		Status = ""
	if Status == "NOT_RESERVED":
		clear_func_Not_Reserved(Not_Reserved_img)
		w.delete(person_photo)
		Status = ""
	if Status == "Finish":
		clear_func_Finish(Finish_img)
		Status = ""
	while True:
		input_state = GPIO.input(IN_REL)
		if input_state == True:
			serial_number.open()
			ch = ""
			ch = serial_number.readline()
			serial_number.flushInput
			serial_number.close()
			if len(ch)!= 11:
				break
			if len(ch)== 11:
				out = ""
				out = ch[0:10]
				print out
				if NUM_OF_NOW==NUM_OF_RESERVED:
						Finish_img = w.create_image(screenx/2,screeny/2, image = Finish)
						Status = "Finish"
						break
				photo_location = ""
				photo_location = '/home/pi/FanAvard/Faces_Resized/'+out+'.png'
				print photo_location
				photo = PhotoImage(file=photo_location)
				person_photo = w.create_image(screenx/2+screenx/50,8*screeny/10-screeny/20, image = photo)
				result= False
				result=search_gived(out)
				if result==True:
					Gived_img = w.create_image(3*screenx/4,4*screeny/10, image = Gived)
					GPIO.output(LED_RD,True)
					GPIO.output(LED_GN,True)
					Status = "GIVED"
					break
				result= False
				result=search_person(out)
				if result==True:
					if NUM_OF_NOW<=NUM_OF_RESERVED:
						NUM_OF_NOW += 1
					if delete_flag==1:
						w.delete(NUM_OF_NOW_img)
					else:
						delete_flag = 1
					NUM_OF_NOW_img = w.create_text((2*screenx/10),(4*screeny/10+screeny/20),text=EN_2_PR(NUM_OF_NOW),font=BTitr)
					Reserved_img = w.create_image(3*screenx/4,4*screeny/10, image = Reserved)
					GPIO.output(LED_GN,True)
					Status = "RESERVED"
					break
				else:
					Not_Reserved_img = w.create_image(3*screenx/4,4*screeny/10, image = Not_Reserved)
					GPIO.output(LED_RD,True)
					Status = "NOT_RESERVED"
					break
				
		else:
			break
	root.after(10, readSerial)
root.after(10, readSerial)
root.mainloop()
