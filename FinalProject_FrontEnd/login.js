    $.ajax({url: "http://localhost:5000/player/2017", success: function(result){
        alert(result.Player)
    }});