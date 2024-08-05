// Define a function to fetch race IDs based on selected date
function getRaceIds() {
    const date = document.getElementById('date').value;
    fetch('/get_race_ids', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ date: date })
    })
    .then(response => response.json())
    .then(data => {
        const raceIdsSelect = document.getElementById('race-id');
        raceIdsSelect.innerHTML = '';
        data.race_ids.forEach(raceId => {
            const option = document.createElement('option');
            option.value = raceId;
            option.text = raceId;
            raceIdsSelect.appendChild(option);
        });
    })
    .catch(error => {
        console.error('Error fetching race IDs:', error);
    });
}

// Define a function to predict the winner based on selected race ID
function predictWinner() {
    const raceId = document.getElementById('race-id').value;
    fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ race_id: raceId })
    })
    .then(response => response.json())
    .then(data => {
        const predictionResult = document.getElementById('prediction-result');
        if ('error' in data) {
            predictionResult.innerText = data.error;
        } else {
            predictionResult.innerText = `Winner Horse Number: ${data.winner_horse_number}, Winning Percentage: ${data.winning_percentage.toFixed(2)}%`;
        }
    })
    .catch(error => {
        console.error('Error predicting winner:', error);
    });
}
