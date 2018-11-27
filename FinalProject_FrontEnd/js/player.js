// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

// Area Chart Example
function getplayerstats(action) {
  var player = document.getElementById("playername").value;
  var game = document.getElementById("selectgame1").value;
  var url = "http://localhost:5000/player" + game + "/"
  $('#playerstatsinput').append('<div class="loader" id="loader"></div>');
  $.ajax({
    url: url + player, success: function (result) {
      if (Object.keys(result).length>0){
        if(action=='update'){
          $('#myPlayer').remove();
          $('#myplayerstats').remove();
          $('#myplayerrank').remove();
          $('#myPlayerArea').append('<div id="myPlayer" class="col-sm-6 col-xl-4"></div>');
          $('#myPlayerArea').append('<div id="myplayerstats" class="col-sm-6 col-xl-4"></div>');
          $('#myPlayerArea').append('<div id="myplayerrank" class="col-sm-6 col-xl-4"></div>');
        }
        if (imageExists("/img/"+player.replace(" ","%20")+".png")){
          $('#myPlayer').append("<img src=/img/"+player.replace(" ","%20")+".png />"); 
        }
        var url2 = "http://localhost:5000/sortstats/" + Object.keys(result)[Object.keys(result).length-1] + "/" + game
        $.ajax({
          url: url2, success: function (rank) {
            attrlist = ['FG%', 'FT%', '3P%', 'PTS/G', 'TRB/G', 'AST/G', 'BLK/G', 'STL/G']
            for (var i = 0; i < attrlist.length; i++) {
              $('#myplayerstats').append("<div>" + attrlist[i] + ": " + Math.round(result[Object.keys(result)[Object.keys(result).length - 1]][attrlist[i]]*100)/100 + "</div>")
              $('#myplayerrank').append("<div>" + attrlist[i] + " Rank: #" + (rank[attrlist[i]].indexOf(player)+1) + "</div>")
            }
          }
        })
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
  $('#mostimproveplayerinput').append('<div class="loader" id="loader"></div>');
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
  $('#teamwinshareinput').append('<div class="loader" id="loader"></div>');
  $.ajax({
    url: url + year, success: function (result) {
      var ctx = document.getElementById("myteamwinshare");
      var attr = document.getElementById("selectattribute3").value;
      var teamlist = Object.keys(result)
      if (teamlist.indexOf('TOT') > -1) {
        teamlist.splice(teamlist.indexOf('TOT'), 1);
      }
      var WS = [], OWS = [], DWS = []
      var CWS = [], PFWS = [], SFWS = [], SGWS = [], PGWS = []
      for (var i = 0; i < teamlist.length; i++) {
        WS[i] = Math.round(sumarray(result[teamlist[i]].WS)*10)/10
        OWS[i] = Math.round(sumarray(result[teamlist[i]].OWS)*10)/10
        DWS[i] = Math.round(sumarray(result[teamlist[i]].DWS)*10)/10
        CWS[i] = Math.round(sumarraypos(result[teamlist[i]], 'C')*10)/10
        PFWS[i] = Math.round(sumarraypos(result[teamlist[i]], 'PF')*10)/10
        SFWS[i] = Math.round(sumarraypos(result[teamlist[i]], 'SF')*10)/10
        SGWS[i] = Math.round(sumarraypos(result[teamlist[i]], 'SG')*10)/10
        PGWS[i] = Math.round(sumarraypos(result[teamlist[i]], 'PG')*10)/10
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
function estimateAllStar() {
  var method = document.getElementById("selectalgorithm").value;
  var dataset = document.getElementById("selectdatasets").value;
  var norm = document.getElementById("selectnorm").value;
  var url = "http://localhost:5000/allstar/"+method+"/"+dataset+"/"+norm
  $('#allstarinput').append('<div class="loader" id="loader"></div>');
  $.ajax({
    url: url, success: function (result) {
      if(dataset=='d1'){
        drawRadar(result,2018)
      }
      if(dataset=='d2'){
        drawRadar(result,2017)
      }
    },
    error: function (jqXHR, exception) {
      $('#loader').remove();
      alert("Error occurs, please restart Python application then try again")
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
  $('#loader').remove();
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
  $('#loader').remove();
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
  $('#loader').remove();
}

function drawRadar(result,year){
  playerlist=[]
  allstar=[]
  $('#myplayerradar').remove();
  $('#myChartArea4').append('<div id="myplayerradar" class="row"></div>');
  var url2 = "http://localhost:5000/sortstats/" + year + "/seasons"
  $.ajax({
    url: url2, success: function (rank) {
  for(var i=0;i<Object.keys(result.Player).length;i++){
    playerlist[i]=result.Player[Object.keys(result.Player)[i]]
    allstar[i]=result.AllStar[Object.keys(result.AllStar)[i]]
    var canvas=$('<canvas width="100%" height="30" class="col-sm-12 col-xl-6"></canvas>');
    $('#myplayerradar').append(canvas)
    canvas.attr('id', 'allstar'+i.toString());
    if (imageExists("/img/"+playerlist[i].replace(" ","%20")+".png")){
      $('#myplayerradar').append("<img src=/img/"+playerlist[i].replace(" ","%20")+".png align='center'/>"); 
    }
        var all_star_percentile = {
          'FG%':(1-rank['FG%'].indexOf(playerlist[i])/rank['FG%'].length)*100,
          'FT%':(1-rank['FT%'].indexOf(playerlist[i])/rank['FT%'].length)*100,
          '3P%':(1-rank['3P%'].indexOf(playerlist[i])/rank['3P%'].length)*100, 
          'PTS/G':(1-rank['PTS/G'].indexOf(playerlist[i])/rank['PTS/G'].length)*100, 
          'TRB/G':(1-rank['TRB/G'].indexOf(playerlist[i])/rank['TRB/G'].length)*100, 
          'AST/G':(1-rank['AST/G'].indexOf(playerlist[i])/rank['AST/G'].length)*100, 
          'BLK/G':(1-rank['BLK/G'].indexOf(playerlist[i])/rank['BLK/G'].length)*100, 
          'STL/G':(1-rank['STL/G'].indexOf(playerlist[i])/rank['STL/G'].length)*100
        }
        var rgb = [];
        for (var j = 0; j < 3; j++) {
          rgb.push(Math.floor(Math.random() * 255));
        }
        var config = {
          type: 'radar',
          data: {
            labels: ['FG%', 'FT%', '3P%', 'PTS/G', 'TRB/G', 'AST/G', 'BLK/G', 'STL/G'],
            datasets: [{
              label: "Stats Percentile",
              backgroundColor: 'rgb(' + rgb.join(',') + ',0.2)',
              borderColor: 'rgb(' + rgb.join(',') + ',1)',
              pointBackgroundColor: 'rgb(' + rgb.join(',') + ',1)',
              data: [
                all_star_percentile['FG%'],
                all_star_percentile['FT%'],
                all_star_percentile['3P%'],
                all_star_percentile['PTS/G'],
                all_star_percentile['TRB/G'],
                all_star_percentile['AST/G'],
                all_star_percentile['BLK/G'],
                all_star_percentile['STL/G']
              ]
            }]
          },
          options: {
            legend: {
              position: 'top',
            },
            title: {
              display: true,
              text: playerlist[i]
            },
            scale: {
              ticks: {
                beginAtZero: true
              }
            }
          }
        };
        new Chart(document.getElementById('allstar'+i.toString()), config);
        $('#loader').remove();
      }
    }
})
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
function imageExists(image_url){
  var http = new XMLHttpRequest();
  http.open('HEAD', image_url, false);
  http.send();
  return http.status != 404;
}