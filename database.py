import mysql.connector as mc
conn=mc.connect(user='root',password='SaniyaMirza@23',host='localhost')
if conn.is_connected():
    print("you are connected")
else:
    print('unable to connect')


mycursor=conn.cursor()
mycursor.execute("create database insurance")
print('database is created')


mycursor.close()
conn.close()