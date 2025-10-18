document.addEventListener('DOMContentLoaded', function() {
    const chartContainer = document.getElementById('chart-container');
    const hallOfFame = document.getElementById('hall-of-fame');

    function fetchLeaderboardData() {
        fetch('/leaderboard/data')
            .then(response => response.json())
            .then(data => {
                // Create the chart
                Highcharts.chart(chartContainer, {
                    chart: {
                        type: 'column'
                    },
                    title: {
                        text: 'Department Standings'
                    },
                    xAxis: {
                        categories: data.categories,
                        crosshair: true
                    },
                    yAxis: {
                        min: 0,
                        title: {
                            text: 'Medals'
                        }
                    },
                    tooltip: {
                        headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
                        pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
                            '<td style="padding:0"><b>{point.y}</b></td></tr>',
                        footerFormat: '</table>',
                        shared: true,
                        useHTML: true
                    },
                    plotOptions: {
                        column: {
                            pointPadding: 0.2,
                            borderWidth: 0
                        }
                    },
                    series: data.series
                });

                // Populate the Hall of Fame
                data.hall_of_fame.forEach(winner => {
                    const winnerElement = `
                        <div class="card m-2" style="width: 18rem;">
                            <div class="card-body">
                                <h5 class="card-title">${winner.name}</h5>
                                <p class="card-text">${winner.event} - ${winner.year}</p>
                            </div>
                        </div>
                    `;
                    hallOfFame.innerHTML += winnerElement;
                });
            })
            .catch(error => console.error('Error fetching leaderboard data:', error));
    }

    fetchLeaderboardData();
});
