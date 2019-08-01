import sched
from datetime import datetime
import psycopg2
import schedule
import time

date_format = "%Y-%m-%d"

connection = False
cursor = None


def job(user_birthday): #Function called when date of birth is today
    print("It's", user_birthday,"\b's Birthday!\n")


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
        print("Birthday(month-date)", datetime.strptime(str(row[0]), date_format).date().month, "-", datetime.strptime(str(row[0]), date_format).date().day)
        print("Today(month-date)",datetime.now().date().month, "-", datetime.now().date().day,"\n")
        if (datetime.strptime(str(row[0]), date_format).date().month, "-", datetime.strptime(str(row[0]), date_format).date().day) == (datetime.now().date().month, "-", datetime.now().date().day):
            birthday_username = str(row[1])
            job(birthday_username)
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


#print(datetime.now().date().month,"-" , datetime.now().date().day)
#print(datetime.strptime("2019-08-01", date_format).date().month, "-", datetime.strptime("2019-08-01", date_format).date().day)
# while True:
#     schedule.run_pending()
#     time.sleep(1)

#schedule.every().day.at("13:06").do(job)
#schedule.every().second.do(job)
# schedule.every().hour.do(job)
# schedule.every(5).to(10).minutes.do(job)
# schedule.every().monday.do(job)
# schedule.every().wednesday.at("13:15").do(job)
# schedule.every().minute.at(":17").do(job)

#obj = datetime.now().date()