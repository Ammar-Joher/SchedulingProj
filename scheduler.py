import ast
import sched
import psycopg2
import schedule
import time
import smtplib
import sendgrid
import os
from sendgrid.helpers.mail import *
from sendgrid import SendGridAPIClient
import json
from datetime import datetime, timedelta
from pytz import timezone
import pytz
date_format = "%Y-%m-%d"

connection = False
cursor = None

sg = sendgrid.SendGridAPIClient('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')

with open("C:\\Users\Debobroto.Talukder\PycharmProjects\SchedulingProj\countryCodes.txt", "r") as data:
    dictionary = ast.literal_eval(data.read())

user_cName = ''

def sendEmailGrid(toUser_birthdayGrid, user_emailGrid):
    message = Mail(
        from_email='adminteam@chartercross.com',
        to_emails= user_emailGrid,
        subject="It's your birthday!",
        html_content="<strong>Happy birthday " + toUser_birthdayGrid + "</strong>" + "<br> <br>Best Regards<br>Admin Team")

    try:
        #message.smtpapi.set_send_at(timestamp)
        response = sg.send(message)

    except Exception as e:
        print(response.e)

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


def job(user_birthday, user_email, user_country): #Function called when date of birth is today
    print("It's", user_birthday,"\b's Birthday!")
    for country_name in dictionary:
        # print(country_name['name'])
        if country_name['name'] == user_country:
            print("Time zone of user country:", str(country_name.get("timezones")).replace("['", "").replace("']", ""))
            ist = pytz.timezone(str(country_name.get("timezones")).replace("['", "").replace("']", ""))
            print('Hour in ' + user_country + ": ", datetime.now(tz=ist).hour, " (24 hour format)")
            if datetime.now(tz=ist).hour == 00:
                sendEmailGrid(user_birthday, user_email)
            else:
                print("Email will only send at 00 hour")

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
        print("email = ", row[2], )
        print("country = ", str(row[3]), "\n")
        print("Birthday(month-date)", datetime.strptime(str(row[0]), date_format).date().month, "-", datetime.strptime(str(row[0]), date_format).date().day)
        print("Today(month-date)",datetime.now().date().month, "-", datetime.now().date().day,"\n")
        if (datetime.strptime(str(row[0]), date_format).date().month, "-", datetime.strptime(str(row[0]), date_format).date().day) == (datetime.now().date().month, "-", datetime.now().date().day):
            birthday_username = str(row[1])
            email_user = str(row[2])
            country_user = str(row[3])
            job(birthday_username, email_user, country_user)
        else:
            print("Today is not his birthday\n")

    record = cursor.fetchone()
except (Exception, psycopg2.Error) as error :
    print ("Error while connecting to PostgreSQL", error)
    # closing database connection.
if connection:
    cursor.close()
    connection.close()
    print("PostgreSQL connection is closed")