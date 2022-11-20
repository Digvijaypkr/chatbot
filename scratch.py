import json  #helps to convert data into json and vice versa
# import os --helps to interact with os(mkdir,chdir,rmdir etc.)

import flask  #web application framework(flask is a library)
import requests  #helps to make http request to a web page
from flask import Flask, request, send_from_directory #(Flask is a class),sendfrom used to send files from a directory securely

app = flask.Flask(__name__) #app is variable,whose value is the obj of Flask class(__name__ is constructor, also contains the name of module)
#now app contains all attributes and methods of Flask class, __name__ is a built-in variable in py

@app.route('/') #@is decorator->modifies the function that follows it,route() contains path(partial url)
#app.route('/')- / is the root of the website(homepage)
@app.route('/home')
def home(): #this is the view function->decorator makes it's content visible on the webpage
    return "Hello World" #this return value is written into the web browser window

@app.route('/webhook', methods=['POST'])#decorating the next function 
#specifying POST method to be used for requests 

def webhook():#function to connect with dialogflow
    
    req = request.get_json(silent=True, force=True)#converts the request data to json
    #silent=true-> if this method fails,it should stop silently and return none
    # force=true->to ignore the content type i.e to convert the request data to json regardless of its type 
    query_result = req.get('queryResult') #stores the user query (this data is fetched from dialogflow)
    #get()->searches for the specified key in the argument 
    #request.get()->contains data that a browser sends us(url parameters,POST data

    if query_result.get('action')=='addition': #if user entered add keyword in query
        sum = 0
        num1 = int(query_result.get('parameters').get('number')) #int()->converts the data type to integer
        num2 = int(query_result.get('parameters').get('number1'))

        sum = str(num1 + num2) #str()->converts the data type to string
        # print('here num1 = {0}'.format(num1))->to debug
        # print('here num2 = {0}'.format(num2))->to debug
        return {
                "fulfillmentText": 'The sum of the two numbers is: '+sum #returns the sum to dialogflow in string format (json)
            }
    
    elif query_result.get('action')=='convert.currency': #if user entered convert keyword in query
         original_currency=req['queryResult']['parameters']['unit-currency']['currency'] 
         amount=req['queryResult']['parameters']['unit-currency']['amount']
         final_currency=req['queryResult']['parameters']['currency-name']
         #fetching data from json response in dialogflow

        #  print(source_currency)->to debug
        #  print(amount)->to debug
        #  print(target_currency)->to debug

         cf=fetch_conversion_factor(original_currency,final_currency) #fetching the currency conversion factor

         final_amount=amount*cf #stores the converted currency value
         final_amount=round(final_amount,2) #rounding off to 2 places

         #print(final_amount)->to debug

         return {
            "fulfillmentText":"{} {} is {} {}".format(amount,original_currency,final_amount,final_currency)
         }#ormat()->inserts the specified values in the placeholder
          #returning converted currency to dialogflow(json)

def fetch_conversion_factor(origin_curr,final_curr):
    url="https://free.currconv.com/api/v7/convert?q={}_{}&compact=ultra&apiKey=72fb3e9582667d53fce1".format(origin_curr,final_curr)
    res1=requests.get(url) #requests.get()->requests library method for our app to make http requests to other sites(APIs)
                           #it makes an outgoing request and returns the response from that site
    res1=res1.json() #resolves the result into json format

    return res1['{}_{}'.format(origin_curr,final_curr)] 

if __name__ == "__main__": #if this returns true=>program is being run by itself and was not imported

    app.debug = True #to debug errors(helps to pin-point the error)
    app.run() #runs local development server
    #run()->can listen to server ip address and port