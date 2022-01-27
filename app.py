
# importing the necessary dependencies
from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import pickle

app = Flask(__name__) # initializing a flask app

@app.route('/',methods=['GET'])  # route to display the home page
@cross_origin()
def homePage():
    return render_template("index.html")

@app.route('/predict',methods=['POST','GET']) # route to show the predictions in a web UI
@cross_origin()
def index():
    if request.method == 'POST':
        try:
            #  reading the inputs given by the user
            pclass=float(request.form['pclass'])
            sex = str(request.form['sex'])
            age = float(request.form['age'])
            sibsp = float(request.form['sibsp'])
            parch = float(request.form['parch'])
            fare = float(request.form['fare'])
            if sex == 'male':
                sex = 0
            else:
                sex = 1
            filename = 'dtmodelprediction.sav'
            loaded_model = pickle.load(open(filename, 'rb')) # loading the model file from the storage
            # predictions using the loaded model file
            prediction=loaded_model.predict([[pclass,sex,age,sibsp,parch,fare]])
            print(prediction[0])
            if prediction[0] == 0.0:
                prediction = "Passenger did not survive"
            else:
                prediction = 'Passenger survived'
            print('prediction is', prediction)
            # showing the prediction results in a UI
            return render_template('results.html',prediction=prediction)
        except Exception as e:
            print('The Exception message is: ',e)
            return 'something is wrong'
    # return render_template('results.html')
    else:
        return render_template('index.html')


if __name__ == "__main__":
    #app.run(host='127.0.0.1', port=8001, debug=True)
	app.run(debug=True) # running the app