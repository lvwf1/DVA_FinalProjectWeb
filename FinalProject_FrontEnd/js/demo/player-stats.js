// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

// Area Chart Example
function getplayerstats(action) {
  var player = document.getElementById("playername").value;
  var game = document.getElementById("selectgame1").value;
  var url = "http://localhost:5000/player" + game + "/"
  $.ajax({
    url: url + player, success: function (result) {
      if (Object.keys(result).length>0){
        $('#myPlayerStatsChart').remove();
        $('#myChartArea1').append('<canvas id="myPlayerStatsChart" width="100%" height="30"><canvas>');
        ctx = document.getElementById("myPlayerStatsChart");
        attr = document.getElementById("selectattribute1").value;
        ydata = []
      if (action == 'update') {
        xlabel = Object.keys(result)
      }
      if (action == 'add') {
        frontarray = []
        backarray = []
        for (var i = 0; i < Object.keys(result).length; i++) {
          if (Object.keys(result)[i] < xlabel[0]) {
            frontarray.push(Object.keys(result)[i])
          }
          if (Object.keys(result)[i] > xlabel[xlabel.length - 1]) {
            backarray.push(Object.keys(result)[i])
          }
        }
        xlabel = frontarray.concat(xlabel)
        xlabel = xlabel.concat(backarray)
      }
        var rgb = [];
        for (var i = 0; i < 3; i++) {
          rgb.push(Math.floor(Math.random() * 255));
        }
        for (var i = 0; i < xlabel.length; i++) {
          if (Object.keys(result).includes(xlabel[i])) {
            ydata[i] = result[xlabel[i]][attr]
          }
          else {
            ydata[i] = 0
          }
        }
        if (action == 'update') {
          datasets = [{
            label: attr + ' of ' + player + ' in ' + game,
            lineTension: 0.3,
            backgroundColor: 'rgb(' + rgb.join(',') + ',0.2)',
            borderColor: 'rgb(' + rgb.join(',') + ',1)',
            pointRadius: 5,
            pointBackgroundColor: 'rgb(' + rgb.join(',') + ',1)',
            pointBorderColor: "rgba(255,255,255,0.8)",
            pointHoverRadius: 5,
            pointHoverBackgroundColor: 'rgb(' + rgb.join(',') + ',1)',
            pointHitRadius: 50,
            pointBorderWidth: 2,
            data: ydata,
          }]
          min_y = Math.min(...ydata)
          max_y = Math.max(...ydata)
        }
        if (action == 'add') {
          prev_ydata = new Array(frontarray.length).fill(0).concat(datasets[datasets.length - 1].data).concat(new Array(backarray.length).fill(0))
          datasets[datasets.length - 1].data = prev_ydata
          datasets.push(
            {
              label: attr + ' of ' + player + ' in ' + game,
              lineTension: 0.3,
              backgroundColor: 'rgb(' + rgb.join(',') + ',0.2)',
              borderColor: 'rgb(' + rgb.join(',') + ',1)',
              pointRadius: 5,
              pointBackgroundColor: 'rgb(' + rgb.join(',') + ',1)',
              pointBorderColor: "rgba(255,255,255,0.8)",
              pointHoverRadius: 5,
              pointHoverBackgroundColor: 'rgb(' + rgb.join(',') + ',1)',
              pointHitRadius: 50,
              pointBorderWidth: 2,
              data: ydata,
            }
          )
          min_y = Math.min(min_y, Math.min(...ydata))
          max_y = Math.max(max_y, Math.max(...ydata))

        }
        drawGraph1(ctx, xlabel, datasets, min_y, max_y)
      }
      else{
        alert('Please enter a valid player name')
      }
    }
  });
}
function getplayermip() {
  var year = document.getElementById("mipyear").value;
  var game = document.getElementById("selectgame2").value
  var url = "http://localhost:5000/mostimprovedplayer" + game + "/"
  $('#myMIP').remove();
  $('#myChartArea2').append('<canvas id="myMIP" width="100%" height="30"><canvas>');
  $.ajax({
    url: url + year, success: function (result) {
      var ctx = document.getElementById("myMIP");
      var attr = document.getElementById("selectattribute2").value;
      var xlabel = []
      var ydata1 = []
      var ydata2 = []
      for (var i = 0; i < 5; i++) {
        ydata1[i] = result[i][attr + '_old']
        ydata2[i] = result[i][attr]
        xlabel[i] = result[i]['Player']
      }
      var barChartData = {
        labels: xlabel,
        datasets: [{
          label: attr + ' of ' + (year - 1).toString(),
          backgroundColor: "rgba(2,117,216,0.2)",
          borderColor: "rgba(2,117,216,1)",
          borderWidth: 1,
          data: ydata1
        }, {
          label: attr + ' of ' + year.toString(),
          backgroundColor: "rgba(216,117,2,0.2)",
          borderColor: "rgba(216,117,2,1)",
          borderWidth: 1,
          data: ydata2
        }]

      };
      drawGraph2(ctx, barChartData, year, attr, game)
    }
  });
}
function getteamwinshare() {
  var year = document.getElementById("teamyear").value;
  var game = document.getElementById("selectgame3").value
  $('#myteamwinshare').remove();
  $('#myChartArea3').append('<canvas id="myteamwinshare" width="100%" height="50"><canvas>');
  var url = "http://localhost:5000/teamwinshare" + game + "/"
  $.ajax({
    url: url + year, success: function (result) {
      var ctx = document.getElementById("myteamwinshare");
      var attr = document.getElementById("selectattribute3").value;
      console.log(result)
      var teamlist = Object.keys(result)
      if (teamlist.indexOf('TOT') > -1) {
        teamlist.splice(teamlist.indexOf('TOT'), 1);
      }
      var WS = [], OWS = [], DWS = []
      var CWS = [], PFWS = [], SFWS = [], SGWS = [], PGWS = []
      for (var i = 0; i < teamlist.length; i++) {
        WS[i] = sumarray(result[teamlist[i]].WS)
        OWS[i] = sumarray(result[teamlist[i]].OWS)
        DWS[i] = sumarray(result[teamlist[i]].DWS)
        CWS[i] = sumarraypos(result[teamlist[i]], 'C')
        PFWS[i] = sumarraypos(result[teamlist[i]], 'PF')
        SFWS[i] = sumarraypos(result[teamlist[i]], 'SF')
        SGWS[i] = sumarraypos(result[teamlist[i]], 'SG')
        PGWS[i] = sumarraypos(result[teamlist[i]], 'PG')
      }
      datasets = [{
        label: 'OWS',
        backgroundColor: "rgba(216,117,117,0.2)",
        borderColor: "rgba(216,117,117,1)",
        borderWidth: 1,
        stack: 'stack 0',
        data: OWS
      }, {
        label: 'DWS',
        backgroundColor: "rgba(117,117,216,0.2)",
        borderColor: "rgba(117,117,216,1)",
        borderWidth: 1,
        stack: 'stack 0',
        data: DWS
      }, {
        label: 'C',
        backgroundColor: "rgba(2,117,216,0.2)",
        borderColor: "rgba(2,117,216,1)",
        borderWidth: 1,
        stack: 'stack 1',
        data: CWS
      }, {
        label: 'PF',
        backgroundColor: "rgba(216,117,2,0.2)",
        borderColor: "rgba(216,117,2,1)",
        borderWidth: 1,
        stack: 'stack 1',
        data: PFWS
      }, {
        label: 'SF',
        backgroundColor: "rgba(117,216,2,0.2)",
        borderColor: "rgba(117,216,2,1)",
        borderWidth: 1,
        stack: 'stack 1',
        data: SFWS
      }, {
        label: 'SG',
        backgroundColor: "rgba(216,2,117,0.2)",
        borderColor: "rgba(216,2,117,1)",
        borderWidth: 1,
        stack: 'stack 1',
        data: SGWS
      }, {
        label: 'PG',
        backgroundColor: "rgba(117,2,216,0.2)",
        borderColor: "rgba(117,2,216,1)",
        borderWidth: 1,
        stack: 'stack 1',
        data: PGWS
      }]
      if (attr == 'OD') {
        datasets = datasets.slice(0, 2)
      }
      if (attr == 'POS') {
        datasets = datasets.slice(2, 7)
      }
      var barChartData = {
        labels: teamlist,
        datasets: datasets
      }
      drawGraph3(ctx, barChartData, year, game)
    }
  });
}
function drawGraph1(ctx, xlabel, datasets, min, max) {
  new Chart(ctx, {
    type: 'line',
    data: {
      labels: xlabel,
      datasets: datasets,
    },
    options: {
      scales: {
        yAxes: [{
          ticks: {
            min: Math.min(min, 0),
            max: max * 1.1,
            maxTicksLimit: 5
          },
          gridLines: {
            color: "rgba(0, 0, 0, .125)",
          }
        }],
      },
      tooltips: {
        mode: 'index',
        intersect: false
      },
      responsive: true,
      legend: {
        display: true
      }
    }
  });
}

function drawGraph2(ctx, barChartData, year, attr, game) {
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
        text: year.toString() + ' Top 5 MIP ' + attr + ' in ' + game
      }
    }
  });
}
function drawGraph3(ctx, barChartData, year, game) {
  new Chart(ctx, {
    type: 'bar',
    data: barChartData,
    options: {
      title: {
        display: true,
        text: 'Team WinShare of ' + year + ' in ' + game
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
          stacked: true,
          ticks: {
            min: 0
          }
        }]
      }
    }
  });
}
function estimateAllStar() {

  var method = document.getElementById("selectalgorithm").value;
  var dataset = document.getElementById("selectdatasets").value;
  var norm = document.getElementById("selectnorm").value;
  var url = "http://localhost:5000/allstar/"+method+"/"+dataset+"/"+norm
  $.ajax({
    url: url, success: function (result) {
      drawTable(result)
    }
  });
}

function drawTable(result){
  console.log(result)
	var dataToTable = function (dataset) {
    var html = '<table>';
    html += '<thead><tr><th style="width:120px;">#</th>';
    
    var columnCount = 0;
    jQuery.each(dataset.datasets, function (idx, item) {
        html += '<th style="background-color:' + item.fillColor + ';">' + item.label + '</th>';
        columnCount += 1;
    });

    html += '</tr></thead>';

    jQuery.each(dataset.labels, function (idx, item) {
        html += '<tr><td>' + item + '</td>';
        for (i = 0; i < columnCount; i++) {
            html += '<td style="background-color:' + dataset.datasets[i].fillColor + ';">' + (dataset.datasets[i].data[idx] === '0' ? '-' : dataset.datasets[i].data[idx]) + '</td>';
        }
        html += '</tr>';
    });

    html += '</tr><tbody></table>';

    return html;
};

playerlist=[]
allstar=[]
for(var i=0;i<Object.keys(result.Player).length;i++){
  playerlist[i]=result.Player[Object.keys(result.Player)[i]]
  allstar[i]=result.AllStar[Object.keys(result.AllStar)[i]]
}

var data = {
    labels: playerlist,
    datasets: [
        {
            label: "My First dataset",
            fillColor: "rgba(220,220,220,0.2)",
            strokeColor: "rgba(220,220,220,1)",
            pointColor: "rgba(220,220,220,1)",
            pointStrokeColor: "#fff",
            pointHighlightFill: "#fff",
            pointHighlightStroke: "rgba(220,220,220,1)",
            data: allstar
        },
        {
            label: "My Second dataset",
            fillColor: "rgba(151,187,205,0.2)",
            strokeColor: "rgba(151,187,205,1)",
            pointColor: "rgba(151,187,205,1)",
            pointStrokeColor: "#fff",
            pointHighlightFill: "#fff",
            pointHighlightStroke: "rgba(151,187,205,1)",
            data: [28, 48, 40, 19, 86, 27]
        },
        {
            label: "My Third dataset",
            fillColor: "rgba(55,187,205,0.2)",
            strokeColor: "rgba(55,187,205,1)",
            pointColor: "rgba(55,187,205,1)",
            pointStrokeColor: "#fff",
            pointHighlightFill: "#fff",
            pointHighlightStroke: "rgba(151,187,205,1)",
            data: [18, 48, 40, 29, 86, 57]
        }
    ]
};
jQuery('#allstar').html(dataToTable(data));
}
function sumarray(numbers) {
  var sum = 0
  for (var i = 0; i < numbers.length; i++) {
    sum += numbers[i]
  }
  return sum;
}
function sumarraypos(numbers, pos) {
  var sum = 0
  for (var i = 0; i < numbers.WS.length; i++) {
    if (pos == numbers.Pos[i]) {
      sum += numbers.WS[i]
    }
  }
  return sum;
}