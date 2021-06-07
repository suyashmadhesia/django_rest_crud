import requests
import json

URL = 'http://localhost:8000/student.api/'


def delete_data(id):
    data = {'id': id}
    json_data = json.dumps(data)
    r = requests.delete(url=URL, data=json_data)
    print(r.json())


def post_data(name, roll, city):
    data = {
        'name': name,
        'roll': roll,
        'city': city,
    }
    json_data = json.dumps(data)
    r = requests.post(url=URL, data=json_data)
    data_r = r.json()
    print(data_r)


def update_data(id, name, city):
    data = {
        'id': id,
        'name': name,
        'city': city,
    }
    json_data = json.dumps(data)
    r = requests.put(url=URL, data=json_data)
    data_r = r.json()
    print(data_r)


def get_data(id=None):
    data = {}
    if id is not None:
        data = {'id': id}
    json_data = json.dumps(data)
    r = requests.get(url=URL, data=json_data)
    data_r = r.json()
    print(data_r)


def runFunction():
    n = input("For Post Run enter p for get enter g for update press u for delete press d: ")
    if n == "g":
        x = input('get data id wise press y else n :')
        if x == "y":
            id = int(input("Enter Id : "))
            get_data(id)
            runFunction()
        elif x == "n":
            get_data()
            runFunction()
        else:
            runFunction()
    elif n == "p":
        name = input("Enter name : ")
        roll = int(input("Enter roll no : "))
        city = input("Enter City: ")
        post_data(name, roll, city)
        runFunction()
    elif n == 'u':
        name = input("Enter name : ")
        id = int(input("Enter id no : "))
        city = input("Enter City: ")
        update_data(id, name, city)
        runFunction()
    elif n == 'd':
        id = int(input("Enter id no of deleting data : "))
        delete_data(id)
        runFunction()
    else:
        runFunction()


runFunction()
