from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler
app = Flask(__name__)

#loading our model from pickle file
model = pickle.load(open('model.pkl', 'rb'))

@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')


standard_to = StandardScaler()
@app.route("/predict", methods=['POST'])
def predict():
    
    if request.method == 'POST':
        #year
        year = int(request.form['year'])
        year=2020-year

        #km_driven
        km_driven=int(request.form['km_driven'])

        #mileage
        mileage=float(request.form['mileage'])

        #engine
        engine=int(request.form['engine'])

        #max_power
        max_power=int(request.form['max_power'])

        #seats
        seats=int(request.form['seats'])

        #fuel
        fuel=request.form['fuel']
        if(fuel=='Petrol'):
            fuel_Diesel=0
            fuel_Petrol=1
            fuel_LPG=0
        elif(fuel=='Diesel'):
            fuel_Diesel=1
            fuel_Petrol=0
            fuel_LPG=0
        elif(fuel=='LPG'):
            fuel_Diesel=0
            fuel_Petrol=0
            fuel_LPG=1
        #for CNG
        else:
            fuel_Diesel=0
            fuel_Petrol=0
            fuel_LPG=0

        #seller
        seller_type=request.form['seller_type']
        if(seller_type=='Individual'):
            seller_type_Individual=1
            seller_type_Trustmark_Dealer=0
        elif(seller_type=='Trustmark Dealer'):
            seller_type_Individual=0
            seller_type_Trustmark_Dealer=1
        #for Dealer
        else:
            seller_type_Individual=0
            seller_type_Trustmark_Dealer=0

        #transmission	
        transmission=request.form['transmission']
        if(transmission=='Mannual'):
            transmission=1
        #for automatic
        else:
            transmission=0

        #owner
        owner=request.form['owner']
        if(owner=='Second Owner'):
            owner_Fourth_plus= 0
            owner_Second_Owner=1
            owner_Test_Drive_Car=0
            owner_Third_Owner=0
        elif(owner=='Third Owner'):
            owner_Fourth_plus= 0
            owner_Second_Owner=0
            owner_Test_Drive_Car=0
            owner_Third_Owner=1
        elif(owner=='Fourth & Above Owner'):
            owner_Fourth_plus= 1
            owner_Second_Owner=0
            owner_Test_Drive_Car=0
            owner_Third_Owner=0
        #for first owner
        else:
            owner_Fourth_plus= 0
            owner_Second_Owner=0
            owner_Test_Drive_Car=0
            owner_Third_Owner=0

        # print([year,km_driven,mileage,engine,max_power,seats,fuel_Diesel,fuel_LPG,fuel_Petrol,seller_type_Individual,seller_type_Trustmark_Dealer,transmission,owner_Fourth_plus,owner_Second_Owner,owner_Test_Drive_Car,owner_Third_Owner])

        #prediction
        prediction=model.predict([[year,km_driven,mileage,engine,max_power,seats,fuel_Diesel,fuel_LPG,fuel_Petrol,seller_type_Individual,seller_type_Trustmark_Dealer,transmission,owner_Fourth_plus,owner_Second_Owner,owner_Test_Drive_Car,owner_Third_Owner]])
        
        output=round(prediction[0],2)

        #screen the output
        if output<0:
            return render_template('index.html',prediction_texts="Sorry you cannot sell this car")
        else:
            return render_template('index.html',prediction_text="You Can Sell The Car at Rs{}".format(output))
    else:
        return render_template('index.html')



if __name__=="__main__":
    app.run(debug=True)

