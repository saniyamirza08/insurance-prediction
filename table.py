import mysql.connector as mc

conn = mc.connect(user='root', password='SaniyaMirza@23', host='localhost', database='insurance')

if conn.is_connected():
    print("You are connected.")
else:
    print('Unable to connect.')

mycursor = conn.cursor()

query = """CREATE TABLE insurance_data(
    age INT,
    sex VARCHAR(10),
    bmi DECIMAL(5, 2),
    children INT,
    smoker VARCHAR(10),
    region VARCHAR(20),
    predicted DECIMAL(10, 2)
)
"""

mycursor.execute(query)
print('Your table is created.')

mycursor.close()
conn.close()
