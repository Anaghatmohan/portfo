from flask import Flask, render_template, request, redirect
import csv
import psycopg2

connection = psycopg2.connect(
   database="postgres", user='postgres', password='Anagha@12345', host='127.0.0.1', port='5432'
)
cursor = connection.cursor()
connection.autocommit = True


app = Flask(__name__)
print(__name__)


@app.route("/")
def my_home():
    return render_template('index.html')


@app.route("/<string:page_name>")
def page_name(page_name):
    return render_template(page_name)


def write_to_file(data):
    with open('database.txt', mode='a') as database:
        email = data['email']
        subject = data['subject']
        message = data['message']
        file = database.write(f"\n{email},{subject},{message}")


def write_to_csv(data):
    with open('database.csv', mode='a', newline='') as database2:
        email = data['email']
        subject = data['subject']
        message = data['message']
        csv_writer = csv.writer(database2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([email, subject, message])

def write_to_db(data):
    email = data['email']
    subject = data['subject']
    message = data['message']
    try:
        img = (email,subject,message)
        insertquery = "insert into tab1 (id,email,subject,message) values(1,\'{}\',\'{}\',\'{}\')".format(email,subject,message)
        print('Insert Query : ', insertquery)
        cursor.execute(insertquery)
        select_all = "SELECT * from tab1"
        cursor.execute(select_all)
        result = cursor.fetchall()
        for r in result:
            print(r)
        connection.commit()

    except Exception as e:
        print('Caught Exception : ', e)




@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        try:
            data = request.form.to_dict()
            write_to_file(data)
            write_to_csv(data)
            write_to_db(data)
            return redirect('thankyou.html')
        except:
            return 'Did not save to database'
    else:
        return 'something went wrong'

@app.route('/get_value.html',methods=['POST','GET'])
def disp_value():
    connection = psycopg2.connect(
        database="postgres", user='postgres', password='Anagha@12345', host='127.0.0.1', port='5432'
    )
    cursor = connection.cursor()
    cursor.execute("select * from tab1")
    result = cursor.fetchall()
    return render_template("get_value.html", data=result)
connection.close()