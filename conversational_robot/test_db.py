import mysql.connector


# Initialization for mysql database for medication
mydb = mysql.connector.connect(host = '10.42.0.174', user = 'mahmoud',passwd = 'mahmoud', database = 'myAlexa')
mycursor = mydb.cursor()
print(mydb)