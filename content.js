// content.js - Automatically scans all links and current page for phishing

// Function to check every link on the page
document.querySelectorAll("a").forEach(link => {
    const url = link.href;

    // Send each link to the Flask backend for phishing check
    fetch(`http://127.0.0.1:5000/check_link?url=${encodeURIComponent(url)}`)
        .then(response => response.json())
        .then(data => {
            if (data.result === 'phishing') {
                link.style.color = 'red';
                link.style.fontWeight = 'bold';
                link.title = 'Warning: This link might be phishing!';
            }
        })
        .catch(error => console.error('Error checking link:', error));
});

// Check the current website's domain
const currentUrl = window.location.href;

// Send current website's domain to the Flask backend for phishing check
fetch(`http://127.0.0.1:5000/check_link?url=${encodeURIComponent(currentUrl)}`)
    .then(response => response.json())
    .then(data => {
        if (data.result === 'phishing') {
            console.log('%cWARNING: The website you are visiting may be phishing!', 'color: red; font-weight: bold');
        }
    })
    .catch(error => console.error('Error checking website:', error));
