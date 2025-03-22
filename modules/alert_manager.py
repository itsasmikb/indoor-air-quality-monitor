
document.addEventListener("DOMContentLoaded", function() {
    // Simulate checking air quality
    setTimeout(function() {
        const alertBox = document.getElementById('alert-box');
        alertBox.className = 'moderate'; // Change class to moderate
        alertBox.textContent = 'Air quality is moderate.';
    }, 3000); // Change after 3 seconds
});


