// Топ-10 игр (Horizontal Bar Chart)
const topDownloadsCtx = document.getElementById('topDownloadsChart').getContext('2d');
const topDownloadsChart = new Chart(topDownloadsCtx, {
    type: 'bar',
    data: {
        labels: topDownloadedNames,
        datasets: [{
            label: 'Количество загрузок',
            data: topDownloadedNumbers,
            backgroundColor: [
                'rgba(13, 110, 253, 0.7)',
                'rgba(13, 110, 253, 0.7)',
                'rgba(13, 110, 253, 0.7)',
                'rgba(13, 110, 253, 0.7)',
                'rgba(13, 110, 253, 0.7)',
                'rgba(13, 110, 253, 0.5)',
                'rgba(13, 110, 253, 0.5)',
                'rgba(13, 110, 253, 0.5)',
                'rgba(13, 110, 253, 0.5)',
                'rgba(13, 110, 253, 0.5)'
            ],
            borderColor: [
                'rgba(13, 110, 253, 1)',
                'rgba(13, 110, 253, 1)',
                'rgba(13, 110, 253, 1)',
                'rgba(13, 110, 253, 1)',
                'rgba(13, 110, 253, 1)',
                'rgba(13, 110, 253, 1)',
                'rgba(13, 110, 253, 1)',
                'rgba(13, 110, 253, 1)',
                'rgba(13, 110, 253, 1)',
                'rgba(13, 110, 253, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        indexAxis: 'y',
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                display: false
            }
        },
        scales: {
            x: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: 'Количество загрузок'
                }
            }
        }
    }
});

// Топ-10 игр (горизонтальный бар)
const topVisitedCtx = document.getElementById('topVisitedChart').getContext('2d');
const topVisitedChart = new Chart(topVisitedCtx, {
    type: 'bar',
    data: {
        labels: topVisitedNames,
        datasets: [{
            label: 'Количество просмотров',
            data: topVisitedNumbers,
            backgroundColor: [
                'rgba(0, 134, 7, 0.7)',
                'rgba(0, 134, 7, 0.7)',
                'rgba(0, 134, 7, 0.7)',
                'rgba(0, 134, 7, 0.7)',
                'rgba(0, 134, 7, 0.7)',
                'rgba(0, 134, 7, 0.7)',
                'rgba(0, 134, 7, 0.7)',
                'rgba(0, 134, 7, 0.7)',
                'rgba(0, 134, 7, 0.7)',
                'rgba(0, 134, 7, 0.7)'
            ],
            borderColor: [
                'rgba(0, 160, 8, 0.7)',
                'rgba(0, 160, 8, 0.7)',
                'rgba(0, 160, 8, 0.7)',
                'rgba(0, 160, 8, 0.7)',
                'rgba(0, 160, 8, 0.7)',
                'rgba(0, 160, 8, 0.7)',
                'rgba(0, 160, 8, 0.7)',
                'rgba(0, 160, 8, 0.7)',
                'rgba(0, 160, 8, 0.7)',
                'rgba(0, 160, 8, 0.7)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        indexAxis: 'y',
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                display: false
            }
        },
        scales: {
            x: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: 'Количество просмотров'
                }
            }
        }
    }
});

// % Выбранных платформ
const osCtx = document.getElementById('osChart').getContext('2d');
const osChart = new Chart(osCtx, {
    type: 'doughnut',
    data: {
        labels: osNames,
        datasets: [{
            data: osPercents,
            backgroundColor: [
                'rgba(13, 110, 253, 0.7)',
                'rgba(108, 117, 125, 0.7)',
                'rgba(25, 135, 84, 0.7)',
                'rgba(13, 202, 240, 0.7)',
                'rgba(220, 53, 69, 0.7)'
            ],
            borderColor: [
                'rgba(13, 110, 253, 1)',
                'rgba(108, 117, 125, 1)',
                'rgba(25, 135, 84, 1)',
                'rgba(13, 202, 240, 1)',
                'rgba(220, 53, 69, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'right',
            },
            tooltip: {
                callbacks: {
                    label: function(context) {
                        return `${context.label}: ${context.raw}%`;
                    }
                }
            }
        }
    }
});