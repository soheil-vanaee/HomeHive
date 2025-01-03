from flask import Flask, request, render_template, jsonify
import joblib
import numpy as np

app = Flask(__name__)

model = joblib.load('house_price_model.pkl')

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        house_meter = float(request.form.get('house_meter'))
        rooms = int(request.form.get('rooms'))
        latitude = float(request.form.get('latitude'))
        longitude = float(request.form.get('longitude'))
        floor = int(request.form.get('floor'))

        input_features = np.array([[house_meter, rooms, latitude, longitude, floor]])

        predicted_price = model.predict(input_features)[0]

        return jsonify({
            "status": "success",
            "predicted_price": round(predicted_price, 2)  
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400

if __name__ == '__main__':
    app.run(debug=True)
