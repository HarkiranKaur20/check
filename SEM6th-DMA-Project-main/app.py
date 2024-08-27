import pickle
import numpy as np
from sklearn.preprocessing import StandardScaler
from flask import Flask, render_template, request

# Load model
model = pickle.load(open('Caloriesmodel.pkl', "rb"))


# Flask constructor
app = Flask(__name__)


@app.route('/')
@app.route('/main_template', methods=["GET"])
def main_template():
    # Render form
    return render_template('Index.html')


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        gender = request.form['gender']
        age = float(request.form['age'])
        duration = float(request.form['duration'])
        heart_rate = float(request.form['heart_rate'])
        temp = float(request.form['temp'])
        height_cm = float(request.form['height'])
        weight_kg = float(request.form['weight'])

       # if '' in [gender, age, duration, heart_rate, temp, height_cm, weight_kg]:
        #    return render_template('Index.html', error_message="Please fill all entries before submitting")
        # Calculate BMI
        height_m = height_cm / 100
        bmi = round(weight_kg / (height_m ** 2), 2)


        # Convert gender to numeric value
        gender_numeric = 1 if gender == 'Male' else 0

        # Scale the input values
        values = [gender_numeric, age, height_cm, weight_kg, duration, heart_rate, temp]
        input_array = np.asarray(values).reshape(1, -1)
        #scaled_input = scaler.transform(input_array)

        # Predict with input values
        predicted = model.predict(input_array)

        # Determine weight status based on BMI
        if bmi < 18.5:  # Underweight
            weight_status = "Underweight"
            comment = "Gain calories, burn less."
        elif bmi >= 18.5 and bmi < 25:  # Normal weight
            weight_status = "Normal weight"
            comment = "Maintain current weight with balanced diet and regular activity."
        elif bmi >= 25 and bmi < 30:  # Overweight
            weight_status = "Overweight"
            comment = "Focus on burning more calories through increased activity."
        elif bmi >= 30 and bmi < 35:  # Obese
            weight_status = "Obese"
            comment = "Focus on significant weight loss with proper diet and exercise."
        else:  # Severely Obese
            weight_status = "Severely Obese"
            comment = "Medical attention required for weight management."
        # Display predicted values in result.html file
        return render_template('result.html',bmi=bmi, predicted_value=predicted,weight_status=weight_status, comment=comment)
    else:
        return render_template('Index.html')


if __name__ == '__main__':
    app.run(debug=True)
