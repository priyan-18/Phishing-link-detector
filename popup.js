document.getElementById("linkForm").addEventListener("submit", function(event) {
    event.preventDefault();  // Prevent form submission from reloading the page

    const url = document.getElementById("url").value;  // Get the URL entered by the user

    // Send the URL to the Flask backend for phishing check
    fetch(`http://127.0.0.1:5000/check_link?url=${encodeURIComponent(url)}`)
        .then(response => response.json())
        .then(data => {
            const resultElement = document.getElementById("result");
            if (data.result === 'phishing') {
                resultElement.textContent = `Warning! This link might be phishing: ${url}`;
                resultElement.style.color = 'red';
            } else if (data.result === 'safe') {
                resultElement.textContent = `This link is safe: ${url}`;
                resultElement.style.color = 'green';
            } else {
                resultElement.textContent = `Error checking the link. Please try again.`;
                resultElement.style.color = 'orange';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById("result").textContent = 'An error occurred. Please try again.';
            document.getElementById("result").style.color = 'orange';
        });
});
