let chart;
let historyLabels = [];
let historyData = [];
async function predict() {
    let humidity = document.getElementById("humidity").value;
    let pressure = document.getElementById("pressure").value;

    if (!humidity || !pressure) {
        document.getElementById("status").innerText = "Please enter humidity and pressure";
        return;
    }

    document.getElementById("status").innerText = "Loading...";

    try {

        let response = await fetch("http://127.0.0.1:5000/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                humidity: Number(humidity),
                pressure: Number(pressure)
            })
        });

        let data = await response.json();
        if (data.error) {
            document.getElementById("status").innerText = data.error;
            return;
        }


        document.getElementById("predTemp").innerText =
            data.temperature.toFixed(2);
        historyLabels.push("P" + (historyLabels.length + 1));
        historyData.push(data.temperature);
        document.getElementById("status").innerText =
            "ML Prediction completed";

    } catch (error) {
        document.getElementById("status").innerText = "⚠️ Server error or connection issue";

    }
}


async function getWeather() {
    let city = document.getElementById("city").value;

    if (!city) {
        document.getElementById("status").innerText = "Please enter a city";
        return;
    }

    document.getElementById("status").innerText = "Loading...";
    try {
        let response = await fetch(`http://127.0.0.1:5000/weather?city=${city}`);
        let data = await response.json();
        if (data.error) {
            document.getElementById("status").innerText = data.error;
            return;
        }

        document.getElementById("status").innerText =
            `Temp: ${data.temperature}°C | Humidity: ${data.humidity}% | Pressure: ${data.pressure}`;
    } catch (error) {
        document.getElementById("status").innerText = "⚠️ Server error or connection issue";
    }
}


async function predictLive() {
    let city = document.getElementById("city").value;

    if (!city) {
        document.getElementById("status").innerText = "Please enter a city";
        return;
    }

    document.getElementById("status").innerText = "Loading...";
    try {
        let response = await fetch(`http://127.0.0.1:5000/predict-live?city=${city}`);
        let data = await response.json();
        if (data.error) {
            document.getElementById("status").innerText = data.error;
            return;
        }

        document.getElementById("cityName").innerText = "City: " + data.city;

        document.getElementById("realTemp").innerText = data.real_temp;

        document.getElementById("predTemp").innerText =
            data.predicted_temp.toFixed(2);

        document.getElementById("error").innerText =
            data.prediction_error.toFixed(2);

        document.getElementById("confidence").innerText =
            data.confidence;

        document.getElementById("humidityValue").innerText =
            data.humidity;

        document.getElementById("wind").innerText =
            data.wind_speed;

        document.getElementById("clouds").innerText =
            data.clouds;

        historyLabels.push(data.city + " " + (historyLabels.length + 1));
        historyData.push(data.predicted_temp);



        const ctx = document.getElementById("weatherChart").getContext("2d");

        if (!chart) {
            chart = new Chart(ctx, {
                type: "line",
                data: {
                    labels: historyLabels,
                    datasets: [{
                        label: "Prediction History",
                        data: historyData
                    }]
                }
            });
        } else {
            chart.data.labels = historyLabels;
            chart.data.datasets[0].data = historyData;
            chart.update();
        }
        document.getElementById("status").innerText =
            "Live AI prediction completed";
    } catch (error) {
        document.getElementById("status").innerText = "⚠️ Server error or connection issue";
    }
}
