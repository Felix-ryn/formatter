// Memastikan variabel CHART_DATA sudah tersedia
if (typeof CHART_DATA !== 'undefined') {
    
    // Data sudah berupa objek, tidak perlu JSON.parse()
    const data = CHART_DATA;
    
    // Ambil konteks canvas
    const ctx = document.getElementById('myBarChart').getContext('2d');

    // Ciptakan gradient
    const gradient = ctx.createLinearGradient(0, 0, 0, 400);
    gradient.addColorStop(0, 'rgba(0, 123, 255, 0.5)'); 
    gradient.addColorStop(1, 'rgba(0, 123, 255, 0)');  

    const config = {
        type: 'line', 
        data: {
            labels: data.labels, 
            datasets: [{
                label: data.dataset_label, 
                data: data.data_values,
                
                // Styling Chart
                backgroundColor: gradient,
                borderColor: '#007bff',
                borderWidth: 2,
                fill: true,             
                tension: 0.3,           
                pointRadius: 3,         
                pointBackgroundColor: '#007bff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false, 
            plugins: {
                legend: {
                    display: true,
                    position: 'top',
                },
                title: {
                    display: true,
                    text: 'Tren Nilai Matriks (Kolom 0 vs Kolom 3)',
                    font: {
                        size: 16
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: false,
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    },
                    title: {
                        display: true,
                        text: 'Nilai (Kolom 3)'
                    }
                },
                x: {
                     grid: {
                        display: false
                    },
                    title: {
                        display: true,
                        text: 'Indeks Data (Kolom 0)'
                    }
                }
            }
        }
    };

    new Chart(ctx, config);

} else {
    console.error("Data chart tidak ditemukan.");
}
