from collections import deque
from datetime import date, time, datetime
from typing import get_origin
import json
import time
import schedule
from plyer import notification
import threading
import requests
import sys

tasks = {}
count = 0

def run_schedule_task():
    while True:
        schedule.run_pending()
        time.sleep(1)

th = threading.Thread(target = run_schedule_task)
th.daemon = True
th.start()

def show_task():
    print()
    global tasks
    for key in tasks.keys():
        print("taskid: ", tasks[key]['id'], "name: ", tasks[key]['name'], "datetime: ", tasks[key]['datetime']) 
    show_menu()

def push_notification(n_title, n_message, n_app_icon):
    notification.notify(
      title = n_title,
      message = n_message, 
      app_icon = n_app_icon,
      timeout = 7
       )
    _data = {
        #use your own token.... Install NotifyMe app copy token.. paste here...
  "to": "ExponentPushToken[]",
  "title":n_title,
  "body": n_message
}
    response = requests.post("https://exp.host/--/api/v2/push/send", data = _data)
    time.sleep(1)

def add_task():
    print()
    global tasks
    global count
    count += 1
    _id = count
    print("Enter task name")
    _name = input()
    print("Enter task description")
    _description = input()
    print("Enter task date-time : [year month day hour minute seconds]")
    val = list(map(int, input().split(' ')))
    _time = datetime(val[0], val[1], val[2], val[3], val[4], val[5])
    task = {"id" : _id, "name" : _name, "description" : _description ,"datetime" : _time}
    tasks[_id] = task
    #scheduling task :: Assume date is the same date
    _time = str(datetime.time(_time))
    #schedule.every().day.at(_time).do(notification.notify, title=_name, message=_name, app_icon="favicon.ico" ,timeout = 7) 
    schedule.every().day.at(_time).do(push_notification, n_title=_name, n_message = _description, n_app_icon="favicon.ico") 
    print("task added successully!!!")
    show_menu()

def delete_task():
    print()
    global tasks
    print("Enter task id")
    _id = int(input())
    global tasks
    for key in tasks.keys():
        if key == _id:
            tasks.pop(key)
            break
    print("task deleted successully!!!")
    show_menu()

def update_task():
    print()
    global tasks
    print("Enter task id")
    _id = int(input())
    print("Enter task name")
    _name = input()
    print("Enter task description")
    _description = input()
    print("Enter task date-time : [year month day hour minute seconds]")
    val = list(map(int, input().split(' ')))
    _time = datetime(val[0], val[1], val[2], val[3], val[4], val[5])

    for key in tasks.keys():
        if key == _id:
            tasks[_id]["name"] = _name
            tasks[_id]["description"] = _description
            tasks[_id]["datetime"] = _time
    print("task updated successully!!!")
    show_menu()

def show_menu():
    print()
    print("*" * 50)
    print("Select : ")
    print("1. Show Tasks")
    print("2. Add Tasks")
    print("3. Update Tasks")
    print("4. Delete Tasks")
    print("5. Exit")
    print("6. Main Menu")
    print("*" * 50)
    get_response()

def welcome():
    print("Welcome to the task remainder!!")
    show_menu()

def get_response():
    print()
    opt = input()
    if opt == '1':
        show_task()
    elif opt == '2':
        add_task()
    elif opt == '3':
        update_task()
    elif opt == '4':
        delete_task()
    elif opt == '5':
        sys.exit()
        exit()
        
    elif opt == '6':
        show_menu()
    else:
        show_menu()

welcome()
