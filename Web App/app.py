from flask import Flask, render_template, request, jsonify
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import numpy as np

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/schedule', methods=['POST'])
def schedule():
    try:
        # Get data from the request
        file = request.files['dataset']
        num_vehicles = int(request.form['numVehicles'])
        vehicle_capacity = int(request.form['vehicleCapacity'])

        # Read the dataset
        df = pd.read_excel(file)

        # Convert 'prefered_time1' to a string and then to datetime
        df['prefered_time1'] = pd.to_datetime(df['prefered_time1'].astype(str))

        # Extract hour from 'prefered_time1'
        df['hour_of_day'] = df['prefered_time1'].dt.hour

        # Define features
        X = df[['hour_of_day']]

        # Scale features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # Perform K-Means clustering
        kmeans = KMeans(n_clusters=num_vehicles, random_state=42, n_init=10)
        df['cluster'] = kmeans.fit_predict(X_scaled)

        # Calculate mean time for each cluster
        schedule = []
        for i in range(num_vehicles):
            cluster_group = df[df['cluster'] == i]
            mean_time = int(cluster_group['hour_of_day'].mean())
            schedule.append({'vehicle': i + 1, 'time': mean_time})

        return jsonify({'status': 'success', 'schedule': schedule})

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True)