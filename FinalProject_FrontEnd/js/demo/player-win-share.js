// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

// Area Chart Example
var ctx = document.getElementById("myPlayerWinShareChart");
var xlabel = []
var ydata = []
$.ajax({url: "http://localhost:5000/playerwinshare/Stephen%20Curry", success: function(result){
  xlabel=Object.keys(result)
  console.log(result)
  for (var i = 0; i < Object.keys(result).length; i++) { 
    ydata[i]=result[xlabel[i]].WinShare
    xlabel[i]=parseInt(xlabel[i])
  }
  new Chart(ctx, {
    type: 'line',
    data: {
      labels: xlabel,
      datasets: [{
        label: "WinShare",
        lineTension: 0.3,
        backgroundColor: "rgba(2,117,216,0.2)",
        borderColor: "rgba(2,117,216,1)",
        pointRadius: 5,
        pointBackgroundColor: "rgba(2,117,216,1)",
        pointBorderColor: "rgba(255,255,255,0.8)",
        pointHoverRadius: 5,
        pointHoverBackgroundColor: "rgba(2,117,216,1)",
        pointHitRadius: 50,
        pointBorderWidth: 2,
        data: ydata,
      }],
    },
    options: {
      scales: {
        yAxes: [{
          ticks: {
            min: 0,
            max: 25,
            maxTicksLimit: 5
          },
          gridLines: {
            color: "rgba(0, 0, 0, .125)",
          }
        }],
      },
      legend: {
        display: false
      }
    }
  });
}});