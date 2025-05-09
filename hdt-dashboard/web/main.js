// Update dashboard data every 5 seconds
function updateDashboard() {
    eel.fetch_dashboard_data()(function(data) {
        if (!data) return;

        // Update timestamp
        document.getElementById("last-updated").innerText = data.timestamp;

        // Update patient info
        document.getElementById("patient-name").innerText = data.patient.Name;
        document.getElementById("patient-age").innerText = data.patient.Age;
        document.getElementById("patient-gender").innerText = data.patient.Gender;
        document.getElementById("patient-diagnosis").innerText = data.patient.Diagnosis;
        document.getElementById("patient-id").innerText = data.patient.PatientId;
        document.getElementById("patient-status").innerText = data.patient.Status;

        // Update room info
        document.getElementById("room-number").innerText = data.room.RoomNumber;
        document.getElementById("room-type").innerText = data.room.RoomType;
        document.getElementById("room-id").innerText = data.room.RoomId;
        document.getElementById("room-status").innerText = data.room.Status;

        // Update sensor info
        document.getElementById("sensor-bodytemp-value").innerText = data.sensors.bodyTemp.value;
        document.getElementById("sensor-bodytemp-id").innerText = data.sensors.bodyTemp.sensorId;
        document.getElementById("sensor-bodytemp-status").innerText = data.sensors.bodyTemp.status;

        document.getElementById("sensor-heartrate-value").innerText = data.sensors.heartRate.value;
        document.getElementById("sensor-heartrate-id").innerText = data.sensors.heartRate.sensorId;
        document.getElementById("sensor-heartrate-status").innerText = data.sensors.heartRate.status;

        document.getElementById("sensor-spo2-value").innerText = data.sensors.spo2.value;
        document.getElementById("sensor-spo2-id").innerText = data.sensors.spo2.sensorId;
        document.getElementById("sensor-spo2-status").innerText = data.sensors.spo2.status;

        document.getElementById("sensor-roomtemp-value").innerText = data.sensors.roomTemp.value;
        document.getElementById("sensor-roomtemp-id").innerText = data.sensors.roomTemp.sensorId;
        document.getElementById("sensor-roomtemp-status").innerText = data.sensors.roomTemp.status;

        document.getElementById("sensor-roomhumidity-value").innerText = data.sensors.roomHumidity.value;
        document.getElementById("sensor-roomhumidity-id").innerText = data.sensors.roomHumidity.sensorId;
        document.getElementById("sensor-roomhumidity-status").innerText = data.sensors.roomHumidity.status;

        // Global alert
        if (data.globalAlert) {
            document.getElementById("global-alert").style.display = "flex";
        } else {
            document.getElementById("global-alert").style.display = "none";
        }

        // Toggle alert style for cards if status is not "Normal"
        toggleAlertStyle("patient-card", data.patient.Status);
        toggleAlertStyle("room-card", data.room.Status);
        toggleAlertStyle("sensor-bodytemp-card", data.sensors.bodyTemp.status);
        toggleAlertStyle("sensor-heartrate-card", data.sensors.heartRate.status);
        toggleAlertStyle("sensor-spo2-card", data.sensors.spo2.status);
        toggleAlertStyle("sensor-roomtemp-card", data.sensors.roomTemp.status);
        toggleAlertStyle("sensor-roomhumidity-card", data.sensors.roomHumidity.status);
    });
}

function toggleAlertStyle(elementId, statusValue) {
    const card = document.getElementById(elementId);
    if (!card) return;
    if (statusValue && statusValue.toLowerCase() !== "normal") {
        card.classList.add("alert-state");
    } else {
        card.classList.remove("alert-state");
    }
}

// Fetch and display current logged-in user
function loadUser() {
    eel.get_current_user()(function(username) {
        if (username) {
            document.getElementById("welcome-user").innerText = "Welcome, " + username;
        }
    });
}

// Fetch AI suggestion on button click with loading animation
function fetchAISuggestion() {
    const btn = document.getElementById("ai-btn");
    const suggestionText = document.getElementById("ai-suggestion-text");
    
    // Show loading spinner and disable button
    btn.disabled = true;
    suggestionText.innerHTML = '<div class="spinner"></div> Loading AI suggestion...';
    
    eel.get_ai_suggestion()(function(suggestion) {
        // Display suggestion in the marquee-effect container
        suggestionText.innerText = suggestion;
        btn.disabled = false;
    });
}

window.onload = function() {
    loadUser();
    updateDashboard();
    setInterval(updateDashboard, 5000);
};

function updateTime() {
    const now = new Date();
    const formattedTime = `${String(now.getMonth() + 1).padStart(2, '0')}.${String(now.getDate()).padStart(2, '0')}.${now.getFullYear()} ` +
                          `${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}:${String(now.getSeconds()).padStart(2, '0')}`;

    document.getElementById("current-time").textContent = formattedTime;
}

// 每秒更新一次时间
setInterval(updateTime, 1000);

// 初始加载时更新一次时间
updateTime();
