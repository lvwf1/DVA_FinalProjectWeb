//Width and height for whole
var w = 1024;
var h = 650;
var padding = 50;

// Offset adjust for screen resolution
var windowWidth = window.screen.availWidth;
var tipOffset = [0, (windowWidth - w) / 2];

//Image width and height
var image_w = 150;
var image_h = 150;

//For selected node
var active = d3.select(null);

//Define map projection
var projection = d3.geo.albersUsa();

//Define path generator
var path = d3.geo.path()
    .projection(projection);

//Map the winrate to opacity[0.3, 0.6]
var Opacity = d3.scale.linear()
    .range([0.3, 0.6]);

//Map the rank to radius[5, 15]
var Scale = d3.scale.linear()
    .range([5, 15]);

//Create SVG element
var svg = d3.select("#map")
    .append("svg")
    .attr("width", w)
    .attr("height", h);

svg.append("text")
    .text("Probability of Champion NBA 2018-2019 Season")
    .attr("x", w/2)
    .attr("y", padding/2)
    .style("font-family","sans-serif")
    .style("font-size","24px")
    .style("font-weight","bold")
    .style("text-anchor","middle");

//Creater a group to store states
var g = svg.append("g")
    .attr("class","map")
    .attr("transform","translate(0,"+padding+")");;


//Load in state data, draw the map
d3.csv("data/US-states.csv", function(data) {
    //Load in GeoJSON data
    d3.json("data/US-geo.json", function(json) {
        //Merge the EastorWest data and GeoJSON
        //Loop through once for each EastorWest data value
        for (var i = 0; i < data.length; i++) {
            var dataState = data[i].state;				//Grab state name
            var dataValue = parseFloat(data[i].value);	//Grab data value, and convert from string to float
            var dataEASTorWEST = data[i].EASTorWEST;
            //Find the corresponding state inside the GeoJSON
            for (var j = 0; j < json.features.length; j++) {
                var jsonState = json.features[j].properties.name;
                if (dataState == jsonState) {
                    //Copy the data value into the JSON
                    json.features[j].properties.EASTorWEST = dataEASTorWEST;
                    //Stop looking through the JSON
                    break;
                }
            }
        }

        //Bind data and create one path per GeoJSON feature
        g.selectAll("path")
            .data(json.features).enter()
            .append("path")
            .attr("stroke","white")
            .attr("stroke-width",2)
            .attr("d", path)
            .attr("class", function(d) {
                return d.properties.postal;})
            .style("fill", function(d) {
                //Get data value
                var EASTorWEST = d.properties.EASTorWEST;

                if (EASTorWEST) {
                    //If value exists…
                    if (EASTorWEST == "East") {
                        return "#FFB6C1";
                    } else {
                        return "#C6E2FF";
                    }
                } else {
                    //If value is undefined…
                    return "#CCCCCC";
                }
            })

        //Load in NBA teams data
        d3.csv("data/NBA-teams.csv", function(data) {
            //Map the rank to radius[2, 20]
            Scale.domain([0, d3.max(data, function(d) { return d.winrate; })]);

            //Map the rank to opacity[0.3, 0.9]
            Opacity.domain([0, d3.max(data, function(d) { return d.winrate; })]);

            //Map the winrate to fontsize[10, 20]
            var FontSize = d3.scale.linear()
                .domain([15, 1])
                .range([10, 20]);

            //Create nodes group
            var nodes = g.selectAll("nodes")
                .data(data)
                .enter()
                .append("g")
                .attr("class", "team")
                .attr("transform", function(d) {
                    return "translate(" + projection([d.lon, d.lat])[0] + "," + projection([d.lon, d.lat])[1] + ")";})
                .on("mouseover", nodeMouseover)
                .on("mouseout", nodeMouseout);


            //Circles for teams
            nodes.append("circle")
                .attr("class", function(d) { return d.abb })
                .attr("r", function(d){
                    return Scale(d.winrate);})
                .style("fill", function(d){
                    if (d.EASTorWEST == "East") {
                        return "red";
                    } else {
                        return "blue";
                    };
                })
                .style("opacity", function(d){
                    return Opacity(d.winrate);})
                .style("cursor", "pointer")
                .on("click",nodesClick);

            //Text for temm abbreviation
            nodes.append("text")
                .attr("class", function(d) {
                    return "text " + d.abb;})
                .attr("dx", function(d){
                    return Scale(d.winrate);})
                .attr("dy", ".3em")
                .attr("font-size", function(d) {
                    return FontSize(d.rank) + "px";})
                .style("fill", "#888888")
                .style("font-weight", "bold")
                .style("cursor", "default")
                .text(function(d) {
                    return d.abb;});
        });
    });
});

//Emphasize
function nodesClick(d) {
    if (d.isClicked=='FALSE') {d.isClicked = 'TRUE';}
    else {d.isClicked = 'FALSE';}

}

function nodeMouseover(d){
    d3.select(this).select("circle")
        .transition()
        .duration(200)
        .attr("r", function(d){
            return 1.5 * Scale(d.winrate); })
        .style("opacity", 1)
        .style("stroke-width", "2px");

    d3.select(this).select("text")
        .transition()
        .duration(200)
        .attr("dx", function(d){
            return 1.5 * Scale(d.winrate);})
        .style("fill", "#000000")
        .text(function(d) {
            return d.abb + " (" + d.winrate + "%)";});

    //Append the logo of the team
    g.append("image")
        .attr("class", d.abb)
        .attr("xlink:href", "logo/" + d.abb + "_logo.svg")
        .attr("width", image_w + "px")
        .attr("height", image_h + "px")
        //remove the blink effect
        .attr("x", projection([d.lon, d.lat])[0] + 5)
        .attr("y", projection([d.lon, d.lat])[1] + 5);
}

//Get back to original status
function nodeMouseout(d){
    if (d.isClicked=='FALSE') {
        d3.select(this).select("circle")
            .transition()
            .duration(200)
            .attr("r", function(d) {
                return Scale(d.winrate); })
            .style("stroke-width", "1px");

        d3.select(this).select("text")
            .transition()
            .duration(200)
            .attr("dx", function(d){
                return Scale(d.winrate);})
            .style("fill", "#888888")
            .text(function(d) {
                return d.abb});

    }
    d3.select(this).select("circle")
        .style("opacity", function(d){
                return Opacity(d.winrate);});
    g.select("image")
        .remove();
}
    
