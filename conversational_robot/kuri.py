import logging

import requests

import mysql.connector

from datetime import date
import calendar

from random import randint

from flask import Flask, render_template, request

from flask_json import FlaskJSON, json_response

from flask_ask import Ask, statement, question, session

#If you get this error "AttributeError: module 'lib' has no attribute 'X509V3_EXT_ge" just run this command pip install 'cryptography<2.2'

app = Flask(__name__)

ask = Ask(app, "/")

url = "https://93a4a1e3.ngrok.io/postjson"

logging.getLogger("flask_ask").setLevel(logging.DEBUG)

mydb = mysql.connector.connect(host = 'localhost',user = 'pami',passwd = 'pamiuser', database = 'myAlexa')

mycursor = mydb.cursor()

week_days = {"Monday" : dict(), "Tuesday" : dict(), "Wednesday" : dict(), "Thursday" : dict(), "Friday" : dict(), "Saturday" : dict(), "Sunday" : dict()}

mycursor.execute("SELECT * FROM MedicationReminder")

myresult = mycursor.fetchall()

for x in week_days :
	for y in myresult:	
		if str(y[2]) == str(x):
			week_days[x][str(y[1])] = dict()

@ask.launch

def skill_launch():

    welcome_msg = 'What can I ask your robot to do	'

    return question(welcome_msg)


@ask.intent("FindIntent", convert={'object': str})

def findanswer(object):
    msg = 'Ok I will let it know'
    val = 'find a ' + object
    data = {'value': val}
    r = requests.post(url, data)

    return statement(msg)

@ask.intent("MoveIntent", convert={'direction': str, 'distance': str})

def moveanswer(direction, distance):
    if (distance):
	msg = 'Ok I will let it know'
 	val = 'go ' + direction + ' ' + distance 
    else:
	msg = 'Ok moving '+ direction
	if ('right' in direction):
 		val = 'turn right'
	elif ('left' in direction):
 		val = 'turn left'
	else:
		val = 'go ' + direction
    
    data = {'value': val}
    r = requests.post(url, data)

    return statement(msg)

@ask.intent("AddMedicationIntent", convert={'medication': str, 'day': str})

def addMedication_answer(medication,day):
    sql = 'insert into myAlexa.MedicationReminder (medication,medication_date) values(%s, %s)'
    if (not day):
	my_date = date.today()
	day = calendar.day_name[my_date.weekday()]
    val = (medication, day)
    mycursor.execute(sql, val)
    mydb.commit()
    print(mycursor.rowcount, "record inserted.")
    mycursor.execute("SELECT * FROM MedicationReminder")

    myresult = mycursor.fetchall()

    for x in week_days :
	for y in myresult:	
		if str(y[2]) == str(x):
			week_days[x][str(y[1])] = dict()
    print(week_days.items())
    return statement('ok added')

@ask.intent("RetrieveMedicationIntent", convert={'day': str})

def retrieveMedication_answer(day):
    if (day == 'today'):
	my_date = date.today()
	day = calendar.day_name[my_date.weekday()]
    #sql = 'select * from MedicationReminder where medication_date = \'' + day + '\''
    #mycursor.execute(sql)
    #result = mycursor.fetchall()
    #if (len(result)):
	#msg = 'you have on '+day+' to take '
	#for i, x in enumerate(result):
    		#print(i, x)    	
	#	msg = msg + x[1]
	#	if (i < len(result)-1):
	#		msg = msg + ' and '
    #else:
	#print ('enter else')
	#msg = 'you don\'t have medication '+day

    if (week_days[str(day)]):
	msg = 'you have on '+day+' to take '
	for x in week_days[str(day)]:
   	
		msg = msg + x + " , "
    else:
	msg = 'you don\'t have medication '+day
    return statement(msg)

@ask.intent("TakeMedicationIntent", convert={'medication': str})

def takeMedication_answer(medication):
    my_date = date.today()
    day = calendar.day_name[my_date.weekday()]
    #sql = 'DELETE FROM MedicationReminder WHERE medication = \'' + medication + '\' and medication_date = \'' +day+ '\''
    #print(sql)
    #mycursor.execute(sql)
    #mydb.commit()
    del week_days[str(day)][str(medication)]
    print(week_days.items())
    return statement('deleted')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
