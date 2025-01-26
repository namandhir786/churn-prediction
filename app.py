from flask import Flask, render_template, request
from jinja2 import Template
import pandas as pd

import requests
import pickle
import numpy as np
import sklearn
import matplotlib

from sklearn.preprocessing import StandardScaler


app = Flask(__name__)
model = pickle.load(open('Customer_Churn_Prediction.pkl', 'rb'))

def preprocessing(X_test):
    X_train=pd.read_csv("X_train")
    sc = StandardScaler()
    sc.fit(X_train)
    X_test = np.array(X_test).reshape(1, -1)

    X_test = sc.transform(X_test)
    return X_test

@app.route('/', methods=['GET'])
def index():
    return render_template('image.html')
@app.route('/form',methods=['GET'])
def form():
    return render_template('predict.html')

standard_to = StandardScaler()
@app.route('/predict',methods=['POST'])
def predict():
    if request.method == 'POST':
        CreditScore = int(request.form['CreditScore'])
        Age = int(request.form['Age'])
        Tenure = int(request.form['Tenure'])
        Balance = float(request.form['Balance'])
        NumOfProducts = int(request.form['NumOfProducts'])
        HasCrCard = int(request.form['HasCrCard'])
        IsActiveMember = int(request.form['IsActiveMember'])
        EstimatedSalary = float(request.form['EstimatedSalary'])
        Geography_Germany = request.form['Geography_Germany']
        if(Geography_Germany == 'Germany'):
            Geography_Germany = 1
            Geography_Spain= 0
            Geography_France = 0
                
        elif(Geography_Germany == 'Spain'):
            Geography_Germany = 0
            Geography_Spain= 1
            Geography_France = 0
        
        else:
            Geography_Germany = 0
            Geography_Spain= 0
            Geography_France = 1
        Gender_Male = request.form['Gender_Male']
        if(Gender_Male == 'Male'):
            Gender_Male = 1
            Gender_Female = 0
        else:
            Gender_Male = 0
            Gender_Female = 1

        X_test= [CreditScore,Age,Tenure,Balance,NumOfProducts,HasCrCard,IsActiveMember,EstimatedSalary,Geography_France,Geography_Germany,Geography_Spain]
        X_test=preprocessing(X_test)
        prediction = model.predict(X_test)
        if prediction==1:
             return render_template('predict.html',prediction_text="The Customer will  leave the bank")
        else:
             return render_template('predict.html',prediction_text="The Customer will not leave the bank")
                

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/data', methods=['GET', 'POST'])
def data():
    if request.method == 'POST':
        file = request.form['upload-file']
        data = pd.read_csv(file)
        return render_template('data.html', data=data.to_html())
    




if __name__=='__main__':
    app.run(port='5000',debug=True)