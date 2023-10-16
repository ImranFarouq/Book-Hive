from flask import Flask, url_for, render_template, request, flash, redirect
from flask_mysqldb import MySQL
import pandas as pd


app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'project'

mysql = MySQL(app)

# @app.route('/')

# def home():
#     return render_template('index.html')

@app.route('/', methods=['GET','POST'])

def login():
    if request.method == 'POST':
        mail = request.form['username']
        pswd = request.form['password']

        cur = mysql.connection.cursor()

        query = 'SELECT * FROM users'
        cur.execute(query)
        data = pd.DataFrame(cur.fetchall(), columns=[i[0] for i in cur.description])
        # df = pd.read_sql_query("SELECT * FROM users", cur)

# Convert the dataframe to an Excel file
        data.to_excel('./output.xlsx', index=False)
        
        cur.execute("SELECT * FROM users WHERE username=%s and password=%s",
                        (mail, pswd))
            # cur.execute("ALTER TABLE UserAccounts userID int PRIMARY KEY AUTO_INCREMENT")
        row = cur.fetchone()
        
        mysql.connection.commit()
        cur.close()

        if row is None:
            flash('looks ike eroor..', category='error')
        
        
        

        return render_template('index.html')
    
    else:
        return render_template('login.html')
    
@app.route('/signup', methods=['GET','POST'])

def signup():
    if request.method == 'POST':
        # data = []
        fname = request.form['firstName']
        lname = request.form['lastName']
        username = request.form['username']
        pswd1 = request.form['password1']
        pswd2 = request.form['password2']
        
        # if pswd1 != pswd2:
        #     return 'Password dpese'
        # if ('@' in username) and (pswd1 == pswd2):

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (fname, lname,username, password) VALUES (%s, %s, %s, %s)", 
                    (fname, lname, username, pswd1))
        
        mysql.connection.commit()
        cur.close()
        print('success')
    
        return redirect(url_for('login'))
    
    else:

        return render_template('signup.html')
    
if __name__ == '__main__':
    app.run(debug=True)