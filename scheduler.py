import sched
from datetime import datetime
import psycopg2
import schedule
import time
import smtplib


date_format = "%Y-%m-%d"

connection = False
cursor = None


def sendEmail(user_email, user_birthday):
    fromaddr = 'savethewarrior@gmail.com'
    toUser_email = user_email
    msg = "\r\n".join([
        "From: savethewarrior@gmail.com",
        "To:" + toUser_email + "@gmail.com",
        "Subject: It's your birthday!",
        "",
        "Happy birthday " + user_birthday + "\n\nBest Regards\nAdmin Team"
    ])
    username = 'savethewarrior@gmail.com'
    password = 'smtplib4488'
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(username, password)
    server.sendmail(fromaddr, toUser_email, msg)
    server.quit()
    print("Email sent to user!!\n")


def job(user_birthday, user_email): #Function called when date of birth is today
    print("It's", user_birthday,"\b's Birthday!\n")
    sendEmail(user_email, user_birthday)

try:
    #Connection to database
    connection = psycopg2.connect(user="postgres",
                                  password="1234",
                                  host="",
                                  port="5432",
                                  database="schedule_db")
    #database object
    cursor = connection.cursor()

# Print PostgreSQL Connection properties
    postgreSQL_select_Query = "SELECT * FROM public.user_info"
    cursor.execute(postgreSQL_select_Query)
    user_records = cursor.fetchall()
    for row in user_records:
        print("DOB = ", row[0], )
        print("username = ", row[1], "\n")
        print("email = ", row[2], "\n")
        print("Birthday(month-date)", datetime.strptime(str(row[0]), date_format).date().month, "-", datetime.strptime(str(row[0]), date_format).date().day)
        print("Today(month-date)",datetime.now().date().month, "-", datetime.now().date().day,"\n")
        if (datetime.strptime(str(row[0]), date_format).date().month, "-", datetime.strptime(str(row[0]), date_format).date().day) == (datetime.now().date().month, "-", datetime.now().date().day):
            birthday_username = str(row[1])
            email_user = str(row[2])
            job(birthday_username, email_user)
        else:
            print("Not the same date\n")

    record = cursor.fetchone()
except (Exception, psycopg2.Error) as error :
    print ("Error while connecting to PostgreSQL", error)
    # closing database connection.
if connection:
    cursor.close()
    connection.close()
    print("PostgreSQL connection is closed")