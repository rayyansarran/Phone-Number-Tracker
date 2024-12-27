
console.log("rayyan")

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('search').addEventListener('click', function() {
        var countryCode = document.getElementById('countryCode').value;
        var phoneNumber = document.getElementById('phoneNumber').value;
        var number = countryCode + phoneNumber;
        
        fetch('/track', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: 'number=' + encodeURIComponent(number)
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {
                document.getElementById('country').textContent = data.country || 'N/A';
                document.getElementById('sim').textContent = data.operator || 'N/A';
                document.getElementById('timezone').textContent = data.timezone || 'N/A';
                document.getElementById('longitude').textContent = data.longitude || 'N/A';
                document.getElementById('latitude').textContent = data.latitude || 'N/A';
                document.getElementById('clock').textContent = data.time || 'N/A';
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});
