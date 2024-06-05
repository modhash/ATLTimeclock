function logTime(logType) {
    const email = document.getElementById('email').value;

    fetch('/api/log', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, log_type: logType }),
    })
    .then(response => response.json())
    .then(data => {
        alert('Time log created successfully!');
        location.reload();
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

document.getElementById('export-btn').addEventListener('click', function () {
    const email = document.getElementById('email').value;
    window.location.href = `/api/export?email=${email}`;
});
