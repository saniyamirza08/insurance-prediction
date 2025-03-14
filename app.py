from flask import Flask, render_template, url_for, request, redirect
app = Flask(__name__)
import mysql.connector as mc
conn = mc.connect(user='root', password='SaniyaMirza@23', host='localhost', database='insurance')
import joblib
model = joblib.load("randomforestregressor.lb")


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/form')
def form():
    return render_template('userdata.html') 

@app.route('/userdata', methods=['GET', 'POST'])
def userdata():
    if request.method == 'POST':
        # Get data from the form
        age = int(request.form['age'])
        sex = request.form['sex']
        bmi = float(request.form['bmi'])
        children = int(request.form['children'])
        smoker = request.form['smoker']
        region = request.form['region']

        sex_encoded = 1 if sex == 'Female' else 0  
        smoker_encoded = 0 if smoker == 'Yes' else 1  
        region_encoded = {'Southwest': 0, 'Southeast': 1, 'Northwest': 2, 'Northeast': 3}.get(region, -1)

        unseen_data = [[age, sex_encoded, bmi, children, smoker_encoded, region_encoded]]

        output = model.predict(unseen_data)[0] 

        
        query = """INSERT INTO insurance_data(age, sex, bmi, children, smoker, region, predicted)
                   VALUES (%s, %s, %s, %s, %s, %s, %s)"""

        mycursor = conn.cursor()
        details = (age, sex, bmi, children, smoker, region, int(output))
        mycursor.execute(query, details)
        conn.commit()

        mycursor.close()

        return f"The predicted insurance premium is: {output}"

    return render_template('userdata.html')


@app.route('/history')
def history():
    
    conn = mc.connect(user='root', password='SaniyaMirza@23', host='localhost', database='insurance')
    mycursor = conn.cursor()

    query = "SELECT age, sex, bmi, children, smoker, region, predicted FROM insurance_data"
    mycursor.execute(query)

    data = mycursor.fetchall()

    mycursor.close()
    conn.close()

    return render_template('history.html', userdetails=data)


if __name__ == "__main__":
    app.run(debug=True)
