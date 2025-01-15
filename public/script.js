// public/script.js
const ctx = document.getElementById('roiChart').getContext('2d');

const roiData = {
    labels: ['Q1', 'Q2', 'Q3', 'Q4'], // Replace with dynamic labels if needed
    datasets: [{
        label: 'ROI (%)',
        data: [10, 20, 30, 40], // Replace with dynamic data
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 1
    }]
};

const config = {
    type: 'bar', // Choose from 'bar', 'line', 'pie', etc.
    data: roiData,
    options: {
        responsive: true,
        plugins: {
            legend: {
                position: 'top',
            },
        }
    }
};

new Chart(ctx, config);
