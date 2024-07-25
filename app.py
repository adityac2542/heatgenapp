from flask import Flask, request
from requests import request
import json
from datetime import datetime, timedelta, timezone

#Global values

#values of all the "values" inside the array data.
values = []
values_li = []

#values of all the "x_values" inside the array data.
x_values = []
x_values_li = []

#values of all the "y_values" inside the array data.
y_values = []
y_values_li = []

#"timestamp:values" only need to return total_with_time gives us timestamps with values.
total_with_time={}
TolVal_for_each_arr = 0

#hottest region variables
indexes_at_x =[]
values_around_max = []
total_int_in_hotzone = 0

#getting utc timestamp.
time_stamp = datetime.now(timezone.utc)
add_time = timedelta(seconds=10)
time = time_stamp

total_interaction = 0


app = Flask(__name__)

@app.route('/')
def index():
    return  "<h1>Working</h1>"


@app.route('/heatgen', methods=['POST']) #getting all the data from the node js
def postmethod():

    global TolVal_for_each_arr
    global total_with_time
    global values_li
    global x_values_li
    global y_values_li
    global x_values
    global y_values
    global time
    global indexes_at_x 
    global values_around_max 
    global total_int_in_hotzone

    #performing all the data handling
    data = request.json()
    data = json.load(data)
    time = time+add_time 
    for i in range(0,len(data)):
      #li= data[f"{i}"]
      #time=data[f"timestamp{i}"]
        values.append(data[i]["value"])

        if data[i]["value"]>1:
            TolVal_for_each_arr= TolVal_for_each_arr + data[i]["value"]

        x_values.append(data[i]["x"])
        y_values.append(data[i]["y"])
        total_with_time[f"{time.strftime('%H:%M:%S')}"]=TolVal_for_each_arr
    
    values_li.append(values)
    x_values_li.append(x_values)
    y_values_li.append(y_values)

    #hottest region calculation
    for i in range(0,len(values_li)):
        max_val = max(values_li[i])
        index = values_li[i].index(max_val)
        x_val_max = x_values_li[i][index]

    for i in range(x_val_max-20,x_val_max+20):
      if i in x_values_li[0]:
            indexes_at_x.append(x_values_li[0].index(i))

    for i in indexes_at_x:
      values_around_max.append(values_li[0][i])

    #total interaction will be the length of the values_around_max as it would be dynamic for every 10 seconds
    total_int_in_hotzone = len(values_around_max)

    return "heelo "

@app.rout('/heatgen', methods=['GET'])
def getmethod():
    # performing all the data analytics
    global values_li
    global total_interaction
    global total_with_time
    global total_int_in_hotzone

    for i in range(len(values_li)):
      for elements in values_li[i]:
            if elements>1:
                  total_interaction+=1

    return total_interaction,  total_with_time, total_int_in_hotzone

if __name__ == '__main__':
    app.run(debug=True)