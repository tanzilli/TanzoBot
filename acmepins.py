# acmepins.py 
#
# raspberry-gpio-python like GPIO functions for Acme boards
# http://sourceforge.net/projects/raspberry-gpio-python/
#
# (C) 2016 Sergio Tanzilli <tanzilli@acmesystems.it>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

__version__ = 'v0.0.2'

import os.path
import platform
import time
import fcntl
import struct
import thread
import threading
import select
import math
import time

if platform.platform().find("Linux-2")!=-1:
	legacy_id=True
else: 	
	legacy_id=False

#Pin to Kernel ID table
pin2kid = {

#Arietta G25
	'J4.7'   :  55, #PA23
	'J4.8'   :  54, #PA22
	'J4.10'  :  53, #PA21
	'J4.11'  :  56, #PA24
	'J4.12'  :  63, #PA31
	'J4.13'  :  57, #PA25
	'J4.14'  :  62, #PA30
	'J4.15'  :  58, #PA26
	'J4.17'  :  59, #PA27
	'J4.19'  :  60, #PA28
	'J4.21'  :  61, #PA29
	'J4.23'  :  32, #PA0
	'J4.24'  :  33, #PA1
	'J4.25'  :  40, #PA8
	'J4.26'  :  39, #PA7
	'J4.27'  :  38, #PA6
	'J4.28'  :  37, #PA5
	'J4.29'  : 124, #PC28
	'J4.30'  : 123, #PC27
	'J4.31'  : 100, #PC4
	'J4.32'  : 127, #PC31
	'J4.33'  :  99, #PC3
	'J4.34'  :  75, #PB11
	'J4.35'  :  98, #PC2
	'J4.36'  :  76, #PB12
	'J4.37'  :  97, #PC1
	'J4.38'  :  77, #PB13
	'J4.39'  :  96, #PC0
	'J4.40'  :  78, #PB14

#Aria G25
	'N2'  :  96,
	'N3'  :  97,
	'N4'  :  98,
	'N5'  :  99,
	'N6'  : 100,
	'N7'  : 101,
	'N8'  : 102,
	'N9' :  103,
	'N10' : 104,
	'N11' : 105,
	'N12' : 106,
	'N13' : 107,
	'N14' : 108,
	'N15' : 109,
	'N16' : 110,
	'N17' : 111,
	'N18' : 112,
	'N19' : 113,
	'N20' : 114,
	'N21' : 115,
	'N22' : 116,
	'N23' : 117,
	'E2'  : 118,
	'E3'  : 119,
	'E4'  : 120,
	'E5'  : 121,
	'E6'  : 122,
	'E7'  : 123,
	'E8'  : 124,
	'E9' :  125,
	'E10' : 126,
	'E11' : 127,
	'S2'  :  53,
	'S3'  :  52,
	'S4'  :  51,
	'S5'  :  50,
	'S6'  :  49,
	'S7'  :  48,
	'S8'  :  47,
	'S9' :   46,
	'S10' :  45,
	'S11' :  44,
	'S12' :  43,
	'S13' :  42,
	'S14' :  41,
	'S15' :  40,
	'S16' :  39,
	'S17' :  38,
	'S18' :  37,
	'S19' :  36,
	'S20' :  35,
	'S21' :  34,
	'S22' :  33,
	'S23' :  32,
	'W9' :   54,
	'W10' :  55,
	'W11' :  56,
	'W12' :  57,
	'W13' :  58,
	'W14' :  59,
	'W15' :  60,
	'W16' :  61,
	'W17' :  62,
	'W18' :  63,
	'W20' :  75,
	'W21' :  76,
	'W22' :  77,
	'W23' :  78,

#FOX Board G20

	'J7.3'  :  82,
	'J7.4'  :  83,
	'J7.5'  :  80,
	'J7.6'  :  81,
	'J7.7'  :  66,
	'J7.8'  :  67,
	'J7.9'  :  64,
	'J7.10' :  65,
	'J7.11' : 110,
	'J7.12' : 111,
	'J7.13' : 108,
	'J7.14' : 109,
	'J7.15' : 105,
	'J7.16' : 106,
	'J7.17' : 103,
	'J7.18' : 104,
	'J7.19' : 101,
	'J7.20' : 102,
	'J7.21' :  73,
	'J7.22' :  72,
	'J7.31' :  87,
	'J7.32' :  86,
	'J7.33' :  89,
	'J7.34' :  88,
	'J7.35' :  60,
	'J7.36' :  59,
	'J7.37' :  58,
	'J7.38' :  57,
	'J6.3'  :  92,
	'J6.4'  :  71,
	'J6.5'  :  70,
	'J6.6'  :  93,
	'J6.7'  :  90,
	'J6.8'  :  69,
	'J6.9'  :  68,
	'J6.10' :  91,
	'J6.13' :  75,
	'J6.14' :  74,
	'J6.15' :  77,
	'J6.16' :  76,
	'J6.17' :  85,
	'J6.18' :  84,
	'J6.19' :  95,
	'J6.20' :  94,
	'J6.21' :  63,
	'J6.22' :  62,
	'J6.24' :  38,
	'J6.25' :  39,
	'J6.26' :  41,
	'J6.27' :  99,
	'J6.28' :  98,
	'J6.29' :  97,
	'J6.30' :  96,
	'J6.31' :  56,
	'J6.32' :  55,
	'J6.36' :  42,
	'J6.37' :  54,
	'J6.38' :  43,

#Acqua A5

	'J1.9'  :   1+32,
	'J1.10'  :   0+32,
	'J1.11'  :   3+32,
	'J1.12'  :   2+32,
	'J1.13'  :   5+32,
	'J1.14'  :   4+32,
	'J1.15'  :   7+32,
	'J1.16'  :   6+32,
	'J1.17'  :   9+32,
	'J1.18'  :   8+32,
	'J1.19'  :  11+32,
	'J1.20'  :  10+32,
	'J1.21'  :  13+32,
	'J1.22'  :  12+32,
	'J1.23'  :  15+32,
	'J1.24'  :  14+32,
	'J1.25'  :  77+32,
	'J1.26'  :  78+32,
	'J1.27'  :  75+32,
	'J1.28'  :  76+32,
	'J1.29'  :  79+32,
	'J1.30'  :  74+32,
	'J1.31'  : 156+32,
	'J1.32'  : 155+32,
	'J1.33'  :  25+32,
	'J1.35'  :  27+32,
	'J1.36'  :  28+32,
	'J1.37'  :  29+32,
	'J1.38'  :  26+32,
	'J1.39'  :  24+32,
	'J1.40'  : 116+32,
	'J1.41'  : 117+32,
	'J1.42'  : 118+32,
	'J1.43'  : 119+32,
	'J1.44'  : 120+32,
	'J1.45'  : 121+32,
	'J1.46'  : 122+32,
	'J1.47'  : 123+32,
	'J1.48'  : 124+32,
	'J1.49'  : 125+32,
	
	 'J2.1'  : 127+32,
	 'J2.2'  : 126+32,
	 'J2.3'  : 115+32,
	 'J2.5'  : 109+32,
	 'J2.6'  : 108+32,
	 'J2.7'  : 107+32,
	 'J2.8'  : 106+32,
	 'J2.9'  : 111+32,
	'J2.10'  : 110+32,
	'J2.11'  : 113+32,
	'J2.12'  : 112+32,
	'J2.13'  :  34+32,
	'J2.14'  : 114+32,
	'J2.15'  :  38+32,
	'J2.16'  :  35+32,
	'J2.17'  :  39+32,
	'J2.18'  :  43+32,
	'J2.19'  :  42+32,
	'J2.23'  :  36+32,
	'J2.25'  :  37+32,
	'J2.29'  :  32+32,
	'J2.31'  :  33+32,
	'J2.32'  :  46+32,
	'J2.33'  :  40+32,
	'J2.34'  :  47+32,
	'J2.35'  :  41+32,
	'J2.36'  :  48+32,
	'J2.37'  :  44+32,
	'J2.38'  :  49+32,
	'J2.39'  :  45+32,
	'J2.40'  :  50+32,
	'J2.42'  :  59+32,
	'J2.43'  :  58+32,
	'J2.44'  :  57+32,
	'J2.45'  :  60+32,
	'J2.46'  :  61+32,

	 'J3.5'  : 145+32, #PE17
	 'J3.6'  : 144+32, #PE16
	 'J3.7'  : 147+32, #PE19
	 'J3.8'  : 146+32, #PE18
	 'J3.9'  : 143+32, #PE15
	'J3.10'  : 151+32, #PE23
	'J3.11'  : 152+32, #PE24
	'J3.12'  : 153+32, #PE25
	'J3.13'  : 154+32, #PE26
	'J3.14'  : 148+32, #PE20
	'J3.15'  :  54+32, #PB22
	'J3.16'  :  55+32, #PB23
	'J3.17'  :  51+32, #PB19
	'J3.18'  :  53+32, #PB21
	'J3.19'  :  56+32, #PB24
	'J3.20'  :  52+32, #PB20
	'J3.22'  :  87+32, #PC23
	'J3.23'  :  89+32, #PC25
	'J3.24'  :  86+32, #PC22
	'J3.25'  :  88+32, #PC24
	'J3.26'  :  90+32, #PC26
	'J3.28'  :  91+32, #PC27
	'J3.29'  :  92+32, #PC28
	'J3.30'  :  94+32, #PC30
	'J3.31'  :  93+32, #PC29
	'J3.32'  :  95+32, #PC31
	'J3.33'  :  17+32, #PA17
	'J3.34'  :  16+32, #PA16
	'J3.35'  :  19+32, #PA19
	'J3.36'  :  18+32, #PA18
	'J3.37'  :  21+32, #PA21
	'J3.38'  :  20+32, #PA20
	'J3.39'  :  23+32, #PA23
	'J3.40'  :  22+32, #PA22
	'J3.41'  :  31+32, #PA31
	'J3.42'  :  30+32, #PA30
	'J3.43'  : 159+32, #PE31
	'J3.44'  : 157+32, #PE29
	'J3.45'  :  80+32, #PC16
	'J3.46'  :  81+32, #PC17
	'J3.47'  :  82+32, #PC18
	'J3.48'  :  83+32, #PC19
	'J3.49'  :  84+32, #PC20
	'J3.50'  :  85+32 #PC21
}

pinmode = {
	"OUTPUT" : "low",
	"LOW" : "low",
	"HIGH" : "high",
	"INPUT" : "in"
}

mcuName2pinname = {
#Arietta G25
    'Arietta_G25' : {
        'PA23' :  'J4.7',
        'PA22' :  'J4.8',
        'PA21' : 'J4.10',
        'PA24' : 'J4.11',
        'PA31' : 'J4.12',
        'PA25' : 'J4.13',
        'PA30' : 'J4.14',
        'PA26' : 'J4.15',
        'PA27' : 'J4.17',
        'PA28' : 'J4.19',
        'PA29' : 'J4.21',
         'PA0' : 'J4.23',
         'PA1' : 'J4.24',
         'PA8' : 'J4.25',
         'PA7' : 'J4.26',
         'PA6' : 'J4.27',
         'PA5' : 'J4.28',
        'PC28' : 'J4.29',
        'PC27' : 'J4.30',
         'PC4' : 'J4.31',
        'PC31' : 'J4.32',
         'PC3' : 'J4.33',
        'PB11' : 'J4.34',
         'PC2' : 'J4.35',
        'PB12' : 'J4.36',
         'PC1' : 'J4.37',
        'PB13' : 'J4.38',
         'PC0' : 'J4.39',
        'PB14' : 'J4.40'
        },
    
#Acqua A5
    'Acqua_A5' : {
         'PA1' :  'J1.9',
         'PA0' : 'J1.10',
         'PA3' : 'J1.11',
         'PA2' : 'J1.12',
         'PA5' : 'J1.13',
         'PA4' : 'J1.14',
         'PA7' : 'J1.15',
         'PA6' : 'J1.16',
         'PA9' : 'J1.17',
         'PA8' : 'J1.18',
        'PA11' : 'J1.19',
        'PA10' : 'J1.20',
        'PA13' : 'J1.21',
        'PA12' : 'J1.22',
        'PA15' : 'J1.23',
        'PA14' : 'J1.24',
        'PC13' : 'J1.25',
        'PC14' : 'J1.26',
        'PC11' : 'J1.27',
        'PC12' : 'J1.28',
        'PC15' : 'J1.29',
        'PC10' : 'J1.30',
        'PE28' : 'J1.31',
        'PE27' : 'J1.32',
        'PA25' : 'J1.33',
        'PA27' : 'J1.35',
        'PA28' : 'J1.36',
        'PA29' : 'J1.37',
        'PA26' : 'J1.38',
        'PA24' : 'J1.39',
        'PD20' : 'J1.40',
        'PD21' : 'J1.41',
        'PD22' : 'J1.42',
        'PD23' : 'J1.43',
        'PD24' : 'J1.44',
        'PD25' : 'J1.45',
        'PD26' : 'J1.46',
        'PD27' : 'J1.47',
        'PD28' : 'J1.48',
        'PD29' : 'J1.49',

        'PD31' :  'J2.1',
        'PD30' :  'J2.2',
        'PD19' :  'J2.3',
        'PD13' :  'J2.5',
        'PD12' :  'J2.6',
        'PD11' :  'J2.7',
        'PD10' :  'J2.8',
        'PD15' :  'J2.9',
        'PD14' : 'J2.10',
        'PD17' : 'J2.11',
        'PD16' : 'J2.12',
         'PB2' : 'J2.13',
        'PD18' : 'J2.14',
         'PB6' : 'J2.15',
         'PB3' : 'J2.16',
         'PB7' : 'J2.17',
        'PB11' : 'J2.18',
        'PB10' : 'J2.19',
         'PB4' : 'J2.23',
         'PB5' : 'J2.25',
         'PB0' : 'J2.29',
         'PB1' : 'J2.31',
        'PB14' : 'J2.32',
         'PB8' : 'J2.33',
        'PB15' : 'J2.34',
         'PB9' : 'J2.35',
        'PB16' : 'J2.36',
        'PB12' : 'J2.37',
        'PB17' : 'J2.38',
        'PB13' : 'J2.39',
        'PB18' : 'J2.40',
        'PB27' : 'J2.42',
        'PB26' : 'J2.43',
        'PB25' : 'J2.44',
        'PB28' : 'J2.45',
        'PB29' : 'J2.46',

        'PE17' :  'J3.5',
        'PE16' :  'J3.6',
        'PE19' :  'J3.7',
        'PE18' :  'J3.8',
        'PE15' :  'J3.9',
        'PE23' : 'J3.10',
        'PE24' : 'J3.11',
        'PE25' : 'J3.12',
        'PE26' : 'J3.13',
        'PE20' : 'J3.14',
        'PB22' : 'J3.15',
        'PB23' : 'J3.16',
        'PB19' : 'J3.17',
        'PB21' : 'J3.18',
        'PB24' : 'J3.19',
        'PB20' : 'J3.20',
        'PC23' : 'J3.22',
        'PC25' : 'J3.23',
        'PC22' : 'J3.24',
        'PC24' : 'J3.25',
        'PC26' : 'J3.26',
        'PC27' : 'J3.28',
        'PC28' : 'J3.29',
        'PC30' : 'J3.30',
        'PC29' : 'J3.31',
        'PC31' : 'J3.32',
        'PA17' : 'J3.33',
        'PA16' : 'J3.34',
        'PA19' : 'J3.35',
        'PA18' : 'J3.36',
        'PA21' : 'J3.37',
        'PA20' : 'J3.38',
        'PA23' : 'J3.39',
        'PA22' : 'J3.40',
        'PA31' : 'J3.41',
        'PA30' : 'J3.42',
        'PE31' : 'J3.43',
        'PE29' : 'J3.44',
        'PC16' : 'J3.45',
        'PC17' : 'J3.46',
        'PC18' : 'J3.47',
        'PC19' : 'J3.48',
        'PC20' : 'J3.49',
        'PC21' : 'J3.50'
    }
}

#Wrapper functions raspberry-gpio-python compatibility
#http://sourceforge.net/p/raspberry-gpio-python/wiki/BasicUsage/

#Note that just some function are implemented
#Replace "import RPi.GPIO as GPIO" with "import acmepins as GPIO"

BOARD = 0
BCM = 0
OUT = "out"
IN = "in"
HIGH=1
LOW=0
RISING='rising'
FALLING='falling'
BOTH='both'
PUD_UP='none'
PUD_DOWN='none'

def setmode(mode):
	return 0

def setwarnings(mode):
	return 0

def cleanup():
	pass

def setup(pin,mode,pull_up_down=0):
	kernel_id=pinname2kernelid(pin)
	export(kernel_id)
	direction(kernel_id,mode)

def output(pin,value):
	if value==True:
		value=1
	if value==False:
		value=0
			
	iopath=get_gpio_path(pinname2kernelid(pin))
	if os.path.exists(iopath): 
		f = open(iopath + '/value','w')
		f.write(str(value))
		f.close()

def input(pin):
	if kernel_id<>-1:
		iopath=get_gpio_path(pinname2kernelid(pin))
		if os.path.exists(iopath): 
			f = open(iopath + '/value','r')
			a=f.read()
			f.close()
			return int(a)

def getVersion ():
	return __version__
			
def add_event_detect(pin, value, callback, debouncingtime):
	iopath=get_gpio_path(pinname2kernelid(pin))
	if os.path.exists(iopath): 
		fd = open(iopath + '/value','w')
		fd.write(str(value))
	else:
		return

	kernel_id=pinname2kernelid(pin)
	if fd!=None:
		set_edge(kernel_id,value)
		thread.start_new_thread(wait_edge,(fd,pin,callback,debouncingtime))
		return
	else:		
		thread.exit()

	fd.close()
			

#End of RPi.GPIO wrapper functions 

def wait_edge(fd,pin,callback,debouncingtime):
	debouncingtime=debouncingtime/1000
	timestampprec=time.time()
	counter=0
	po = select.epoll()
	po.register(fd,select.EPOLLET)
	while True:
		events = po.poll()
		timestamp=time.time()
		if (timestamp-timestampprec>debouncingtime) and counter>0:
			callback(pin)
		counter=counter+1
		timestampprec=timestamp

def get_gpio_path(kernel_id):
	global legacy_id
	kernel_id=kernel_id-32	
	
	if (legacy_id==True):
		iopath="/sys/class/gpio/gpio%d" % (kernel_id+32)
		
	if (legacy_id==False):
		iopath="/sys/class/gpio/pio" 
		if kernel_id>=0 and kernel_id<=31:
			iopath="%sA%d" % (iopath,kernel_id-0)
		if kernel_id>=32 and kernel_id<=63:
			iopath="%sB%d" % (iopath,kernel_id-32)
		if kernel_id>=64 and kernel_id<=95:
			iopath="%sC%d" % (iopath,kernel_id-64)
		if kernel_id>=96 and kernel_id<=127:
			iopath="%sD%d" % (iopath,kernel_id-96)
		if kernel_id>=128 and kernel_id<=159:
			iopath="%sE%d" % (iopath,kernel_id-128)
	return iopath		


def get_kernel_id(connector_name,pin_number):
	return pinname2kernelid(connector_name + "." +pin_number)


def export(kernel_id):
	global legacy_id

	iopath=get_gpio_path(kernel_id)
	if not os.path.exists(iopath): 
		f = open('/sys/class/gpio/export','w')
		if (legacy_id==True):
			f.write(str(kernel_id))
		else:
			f.write(str(kernel_id-32))
		f.close()

def unexport(kernel_id):
	global legacy_id

	iopath=get_gpio_path(kernel_id)
	if os.path.exists(iopath): 
		f = open('/sys/class/gpio/unexport','w')
		if (legacy_id==True):
			f.write(str(kernel_id))
		else:
			f.write(str(kernel_id-32))
		f.close()

def direction(kernel_id,direction):
	iopath=get_gpio_path(kernel_id)
	if os.path.exists(iopath): 
		f = open(iopath + '/direction','w')
		f.write(direction)
		f.close()

def set_value(kernel_id,value):
	iopath=get_gpio_path(kernel_id)
	if os.path.exists(iopath): 
		f = open(iopath + '/value','w')
		f.write(str(value))
		f.close()

def get_value(kernel_id):
	if kernel_id<>-1:
		iopath=get_gpio_path(kernel_id)
		if os.path.exists(iopath): 
			f = open(iopath + '/value','r')
			a=f.read()
			f.close()
			return int(a)

def set_edge(kernel_id,value):
	iopath=get_gpio_path(kernel_id)
	if os.path.exists(iopath): 
		if value in ('none', 'rising', 'falling', 'both'):
		    f = open(iopath + '/edge','w')
		    f.write(value)
		    f.close()

def pwm_export(pwm_id):
	iopath='/sys/class/pwm/pwmchip0/pwm%d' % pwm_id
	if not os.path.exists(iopath): 
		iopath='/sys/class/pwm/pwmchip0'
		f = open(iopath + '/export','w')
		f.write(str(pwm_id))
		f.close()

def pwm_enable(pwm_id):
	iopath='/sys/class/pwm/pwmchip0/pwm%d' % pwm_id
	if os.path.exists(iopath): 
		f = open(iopath + '/enable','w')
		f.write(str(1))
		f.close()

def pwm_disable(pwm_id):
	iopath='/sys/class/pwm/pwmchip0/pwm%d' % pwm_id
	if os.path.exists(iopath): 
		f = open(iopath + '/enable','w')
		f.write(str(0))
		f.close()

def pwm_duty_cycle(pwm_id,ns):
	iopath='/sys/class/pwm/pwmchip0/pwm%d' % pwm_id
	if os.path.exists(iopath): 
		f = open(iopath + '/duty_cycle','w')
		f.write(str(ns))
		f.close()

def pwm_period(pwm_id,ns):
	iopath='/sys/class/pwm/pwmchip0/pwm%d' % pwm_id
	if os.path.exists(iopath): 
		f = open(iopath + '/period','w')
		f.write(str(ns))
		f.close()
		f.close()

def pinname2kernelid(pinname):
	"""
	Return the Kernel ID of any Pin using the MCU name
	or the board name
	"""

	offset=-1
	if pinname[0:2]=="PA":
		offset=32+0
	if pinname[0:2]=="PB":
		offset=32+32
	if pinname[0:2]=="PC":
		offset=32+64
	if pinname[0:2]=="PD":
		offset=32+96
	if pinname[0:2]=="PE":
		offset=32+128

	if offset!=-1:
		return offset+int(pinname[2:4])
	else:	
		return pin2kid[pinname]

class GPIO():
	kernel_id=None
	fd=None


	def __init__(self,pin,mode):
		self.kernel_id=pinname2kernelid(pin)
		export(self.kernel_id)
		direction(self.kernel_id,pinmode[mode])

		iopath=get_gpio_path(self.kernel_id)
		if os.path.exists(iopath): 
			self.fd = open(iopath + '/value','r')

	def high(self):
		set_value(self.kernel_id,1)
		
	def low(self):
		set_value(self.kernel_id,0)

	def on(self):
		set_value(self.kernel_id,1)
		
	def off(self):
		set_value(self.kernel_id,0)

	def digitalWrite(self,level):
		set_value(self.kernel_id,pinlevel[level])

	def set_value(self,value):
		return set_value(self.kernel_id,value)

	def digitalRead(self):
		return get_value(self.kernel_id)

	def get_value(self):
		return get_value(self.kernel_id)

	get = get_value

	def wait_edge(self,fd,callback,debouncingtime):
		# Convert in millisecondi
		debouncingtime=debouncingtime/1000.0 
		timestampprec=time.time()
		counter=0
		po = select.epoll()
		po.register(fd,select.EPOLLET)
		while True:
			events = po.poll()
			timestamp=time.time()
			if (timestamp-timestampprec>debouncingtime) and counter>0:
				callback()
			counter=counter+1
			timestampprec=timestamp

	def set_edge(self,value,callback,debouncingtime=0):
		if self.fd!=None:
			set_edge(self.kernel_id,value)
			thread.start_new_thread(self.wait_edge,(self.fd,callback,debouncingtime))
			return
		else:		
			thread.exit()

		return

