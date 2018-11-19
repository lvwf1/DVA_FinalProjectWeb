// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

// Area Chart Example
function getplayerstats() {
  var player = document.getElementById("playername").value;
  $('#myPlayerStatsChart').remove();
  $('#myChartArea1').append('<canvas id="myPlayerStatsChart" width="100%" height="30"><canvas>');
  $.ajax({
    url: "http://localhost:5000/player/" + player, success: function (result) {
      drawGraph1(result)
    }
  });
}
function getplayermip() {
  var year = document.getElementById("mipyear").value;
  $('#myMIP').remove();
  $('#myChartArea2').append('<canvas id="myMIP" width="100%" height="30"><canvas>');
  $.ajax({
    url: "http://localhost:5000/mostimprovedplayer/" + year, success: function (result) {
      drawGraph2(result,year)
    }
  });
}
function getteamwinshare() {
  var year = document.getElementById("teamyear").value;
  $('#myteamwinshare').remove();
  $('#myChartArea3').append('<canvas id="myMIP" width="100%" height="30"><canvas>');
  $.ajax({
    url: "http://localhost:5000/teamwinshare/" + year, success: function (result) {
      console.log(result)      
      drawGraph3(result,year)
    }
  });
}
function drawGraph1(result){
  var ctx = document.getElementById("myPlayerStatsChart");
  var attr = document.getElementById("selectattribute1").value;
  var xlabel = []
  var ydata = []
  xlabel = Object.keys(result)
      for (var i = 0; i < Object.keys(result).length; i++) {
        ydata[i] = result[xlabel[i]][attr]
        xlabel[i] = parseInt(xlabel[i])
      }
      new Chart(ctx, {
        type: 'line',
        data: {
          labels: xlabel,
          datasets: [{
            label: attr,
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
                max: Math.max(...ydata)*1.1,
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
}

function drawGraph2(result,year) {
  var ctx = document.getElementById("myMIP");
  var attr = document.getElementById("selectattribute2").value;
  var xlabel = []
  var ydata1 = []
  var ydata2 = []
  for (var i = 0; i < 30; i++) {
    ydata1[i] = result[i][attr+'_old']
    ydata2[i] = result[i][attr]
    xlabel[i] = result[i]['Player']
  }
  var barChartData = {
    labels: xlabel,
    datasets: [{
      label: attr+' of '+(year-1).toString(),
      backgroundColor: "rgba(2,117,216,0.2)",
      borderColor: "rgba(2,117,216,1)",
      borderWidth: 1,
      data: ydata1
    }, {
      label: attr+' of '+year.toString(),
      backgroundColor: "rgba(216,117,2,0.2)",
      borderColor: "rgba(216,117,2,1)",
      borderWidth: 1,
      data: ydata2
    }]

  };
  console.log(barChartData)
  new Chart(ctx, {
    type: 'bar',
    data: barChartData,
    options: {
      responsive: true,
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: year.toString()+' Top 5 MIP '+attr
      }
    }
  });
}
function drawGraph3(result,year) {
  var ctx = document.getElementById("myteamwinshare");
  var teamlist = ['ATL', 'BOS', 'BRK', 'CHI', 'CHO', 'CLE', 'DAL', 'DEN', 'DET', 'GSW', 'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA', 'MIL', 'MIN', 'NOP', 'NYK', 'OKC', 'ORL', 'PHI', 'PHO', 'POR', 'SAC', 'SAS', 'TOR', 'TOT', 'UTA', 'WAS']
  var ChartData = []
  for (var i=0; i<teamlist.length;i++){
    ChartData[i]={
      label: teamlist[i],
      data:sumarray(result[teamlist[i]].WS)
    }
  }
  var barChartData = {
    labels:teamlist, 
    datasets:ChartData
  }
  console.log(barChartData)
  new Chart(ctx, {
    type: 'bar',
    data: barChartData,
    options: {
      title: {
        display: true,
        text: 'Chart.js Bar Chart - Stacked'
      },
      tooltips: {
        mode: 'index',
        intersect: false
      },
      responsive: true,
      scales: {
        xAxes: [{
          stacked: true,
        }],
        yAxes: [{
          stacked: true
        }]
      }
    }
  });
}
function sumarray(numbers) {
  var sum = 0
  for (var i = 0; i < numbers.length; i++) {
    sum += numbers[i]
  }
  return sum;
}