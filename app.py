
import csv
import random
import numpy as np
from sklearn.linear_model import LinearRegression
from flask import Flask, request, jsonify, send_file, redirect, render_template, url_for
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Load the CSV file
with open('calorie.csv', 'r') as file:
    reader = csv.DictReader(file)
    data = [row for row in reader]

# Extract input features and target values from the data
X = []
y_calories = []
y_fat = []
y_protein = []
for row in data:
    X.append([float(row['Height (cm)']), float(row['Weight (kg)']), float(row['Age'])])
    y_calories.append(float(row['Calories']))
    y_fat.append(float(row['Fat']))
    y_protein.append(float(row['Protein']))

# Convert lists to numpy arrays
X = np.array(X)
y_calories = np.array(y_calories)
y_fat = np.array(y_fat)
y_protein = np.array(y_protein)

# Perform linear regression to predict calories, fat, and protein
reg_calories = LinearRegression().fit(X, y_calories)
reg_fat = LinearRegression().fit(X, y_fat)
reg_protein = LinearRegression().fit(X, y_protein)

# Define a function to predict calories, fat, and protein based on input values
def predict_calories_fat_protein(height, weight, age):
    # Convert input data to float
    height = float(height)
    weight = float(weight)
    age = float(age)

    # Predict calories, fat, and protein using linear regression models
    calories = reg_calories.predict([[height, weight, age]])[0]
    fat = reg_fat.predict([[height, weight, age]])[0]
    protein = reg_protein.predict([[height, weight, age]])[0]

    # Randomly select a food type
    food_items = [
    'Quinoa and vegetable stir-fry',
    'Roasted chickpeas',
    'Mixed green salad',
    'Roasted sweet potato wedges',
    'Mixed fruit salad',
    'Greek yogurt with honey',
    'Almonds and dried fruits',
    'Raw vegetables with hummus',
    'Oatmeal with berries',
    'Baked tofu with vegetables'
    ]

    food_type = random.choice(food_items)

    # Return the predicted values
    return {'calories': round(calories, 2), 'fat': round(fat, 2), 'protein': round(protein, 2), 'food_type': food_type}


# Set up a route for the frontend
@app.route('/')
def index():
    return "its working!"

# Define a Flask route to receive the input data and return the predicted values
@app.route('/predict', methods=['POST'])
def predict():
    # Parse the input data as JSON
    data = request.get_json()

    # Call the function to perform prediction
    result = predict_calories_fat_protein(data['height'], data['weight'], data['age'])

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
