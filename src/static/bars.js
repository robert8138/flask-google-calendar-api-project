d3.select("#study").on("click", function() { make_graph("Study Time"); });
d3.select("#outsidereading").on("click", function() { make_graph("Outside Reading"); });
d3.select("#birthday").on("click", function() { make_graph("Birthdays"); });
d3.select("#misc").on("click", function() { make_graph("Misc"); });
d3.select("#deadline").on("click", function() { make_graph("Deadline"); });
d3.select("#exercise").on("click", function() { make_graph("Exercise"); });

var width = 1300,
    height = 250;

var svg = d3.select("body").append("svg")
               .attr("width", width)
               .attr("height", height)

var tip = d3.tip()
            .attr('class', 'd3-tip')
            .offset([-10, 0])
            .html(function(d) {
              return "<strong>event:</strong> <span style='color:#2ca25f' class='spanClass'>" + d.event_name + "</span>" +
                     "<strong>date:</strong> <span style='color:#2ca25f' class='spanClass'>" + d.date + "</span>";
            })

//http://bl.ocks.org/Caged/6476579
svg.call(tip); 

function make_graph(event_type) {
  url = "http://127.0.0.1:5000/api/".concat(event_type)
  d3.json(url, function(error, data) {
    
    console.log(event_type.concat("is loaded!"))
    console.log(data['json_list'])
    
    var dataset = data['json_list']
    var barwidth = width / dataset.length;

    // http://bost.ocks.org/mike/bar/3/
    var x = d3.scale.linear()
              .domain([0, dataset.length])
              .range([0, width]);

    var y = d3.scale.linear()
              .domain([0, d3.max(dataset, function(d) { return d.duration; })])
              .range([height - 10, 0]);

    var xAxis = d3.svg.axis()
                  .scale(x)
                  .ticks(25)
                  .orient("bottom");

    var yAxis = d3.svg.axis()
                  .scale(y)
                  .ticks(10)
                  .orient("left");

    // This is more of a hack, because there is no transition
    // I basically removed the old axes, rebuild news ones, and plot them

    svg.selectAll("g").remove();

    svg.append("g")
          .attr("class", "xaxis")
          .attr("transform", "translate(50," + (height - 30 - 10) + ")")
          .transition()
          .duration(750)
          .call(xAxis);

    svg.append("g")
          .attr("class", "yaxis")
          .attr("transform", "translate(50, 0)")
          .transition()
          .duration(750)
          .call(yAxis);


    // http://bl.ocks.org/mbostock/3808218
    // Enter, Update, Exit Design Pattern - suggested by Krist
    
    var bars = svg.selectAll(".bar")
                  .data(dataset);

    bars.enter()
        .append("rect")
        .classed("bar", true)
        .transition()
        .duration(2000)
        .attr("transform", function(d, i) {
            return "translate(" + (i * barwidth + 50) + ",0)"; })    
        .attr("y", function(d) { return y(d.duration); })
        .attr("height", function(d) { return height - 40 - y(d.duration); })
        .attr("width", barwidth - 1)
        .attr("fill", "#fdae6b");

    bars
        .attr("transform", function(d, i) {
            return "translate(" + (i * barwidth + 50) + ",0)"; })    
        .attr("y", function(d) { return y(d.duration); })
        .attr("height", function(d) { return height - 40 - y(d.duration); })
        .attr("width", barwidth - 1);

    bars.exit().remove();

    bars.on('mouseover', tip.show)
        .on('mouseout', tip.hide);

  });
}