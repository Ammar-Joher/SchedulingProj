import sched
from datetime import datetime
import psycopg2
import schedule
import time
import smtplib
import sendgrid
import os
from sendgrid.helpers.mail import *
from sendgrid import SendGridAPIClient

import json

date_format = "%Y-%m-%d"

connection = False
cursor = None

sg = sendgrid.SendGridAPIClient('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')


def sendEmailGrid(toUser_birthdayGrid, user_emailGrid):
    message = Mail(
        from_email='adminteam@chartercross.com',
        to_emails= user_emailGrid,
        subject="It's your birthday!",
        html_content="<strong>Happy birthday " + toUser_birthdayGrid + "</strong>" + "<br> <br>Best Regards<br>Admin Team")

    try:
        msg = sg.send(message)

    except Exception as e:
        print(e)

    print("Email to birthday user sent!\n")


def sendEmail(toUser_birthday, user_email):
    fromaddr = 'savethewarrior@gmail.com'
    toUser_email = user_email

    msg = "\r\n".join([
        "From: savethewarrior@gmail.com",
        "To:" + toUser_email + "@gmail.com",
        "Subject: It's your birthday!",
        "",
        "Happy birthday " + toUser_birthday + "\n\nBest Regards\nAdmin Team"
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
    print("It's", user_birthday,"\b's Birthday!")
    sendEmailGrid(user_birthday, user_email)

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
        print("username = ", row[1], )
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