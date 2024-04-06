from flask import Flask, request
from sklearn.ensemble import IsolationForest
import pandas as pd

app = Flask(__name__)

# Initialize model
model = IsolationForest()

@app.route('/train', methods=['POST'])
def train():
    data = pd.DataFrame(request.get_json())
    model.fit(data)
    return {"message": "Model trained successfully"}

@app.route('/predict', methods=['POST'])
def predict():
    data = pd.DataFrame(request.get_json())
    prediction = model.predict(data)
    if prediction[0] == -1:
        return {"fraud": True}
    else:
        return {"fraud": False}

if __name__ == '__main__':
    app.run(debug=True)