function scheduleTransport() {
    // Get form data
    const form = document.getElementById('schedulingForm');
    const formData = new FormData(form);

    // Make a POST request to the Flask server
    axios.post('/schedule', formData)
        .then(response => {
            if (response.data.status === 'success') {
                displaySchedule(response.data.schedule);
            } else {
                alert('Error: ' + response.data.message);
            }
        })
        .catch(error => {
            alert('Error: ' + error.message);
        });
}

function displaySchedule(schedule) {
    const outputDiv = document.getElementById('output');
    outputDiv.innerHTML = '<h2>Schedule</h2>';

    schedule.forEach(vehicle => {
        outputDiv.innerHTML += `<p>Vehicle ${vehicle.vehicle} should be scheduled at ${vehicle.time}:00</p>`;
    });
}