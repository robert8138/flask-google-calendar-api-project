d3.select("#study").on("click", function() { make_calendar("studytime"); });
d3.select("#outsidereading").on("click", function() { make_calendar("outsidereading"); });
d3.select("#birthday").on("click", function() { make_calendar("birthdays"); });
d3.select("#misc").on("click", function() { make_calendar("misc"); });
d3.select("#deadline").on("click", function() { make_calendar("deadline"); });
d3.select("#exercise").on("click", function() { make_calendar("exercise"); });

var width = 1000,
    height = 150,
    cellSize = 15;

var percent = d3.format(".1%"),
    format = d3.time.format("%Y-%m-%d");

// Set up the skeleton by year
var svg = d3.select("body").selectAll("svg")
    .data(d3.range(2013, 2016))
    .enter().append("svg")
    .attr("width", width)
    .attr("height", height)
    .attr("class", "calendar")
    .append("g")
    .attr("transform", "translate(" + ((width - cellSize * 53) / 2) + "," + (height - cellSize * 7 - 1) + ")");

// Set up the YEAR text
svg.append("text")
    .attr("transform", "translate(-6," + cellSize * 3.5 + ")rotate(-90)")
    .style("text-anchor", "middle")
    .text(function(d) { return d; });

// Set up each day for plotting
var rect = svg.selectAll(".day")
    .data(function(d) { return d3.time.days(new Date(d, 0, 1), new Date(d + 1, 0, 1)); })
    .enter().append("rect")
    .attr("class", "day")
    .attr("width", cellSize)
    .attr("height", cellSize)
    .attr("x", function(d) { return d3.time.weekOfYear(d) * cellSize; })
    .attr("y", function(d) { return d.getDay() * cellSize; })
    .datum(format);

// Add title/date to each cell
rect.append("title")
    .text(function(d) { return d; });

// Set up each month for plotting
svg.selectAll(".month")
    .data(function(d) { return d3.time.months(new Date(d, 0, 1), new Date(d + 1, 0, 1)); })
  	.enter().append("path")
    .attr("class", "month")
    .attr("d", monthPath);

// Some voodoo magic that I don't understand about paths
function monthPath(t0) {
  var t1 = new Date(t0.getFullYear(), t0.getMonth() + 1, 0),
      d0 = t0.getDay(), 
      w0 = d3.time.weekOfYear(t0),
      d1 = t1.getDay(), 
      w1 = d3.time.weekOfYear(t1);
  return "M" + (w0 + 1) * cellSize + "," + d0 * cellSize
      + "H" + w0 * cellSize + "V" + 7 * cellSize
      + "H" + w1 * cellSize + "V" + (d1 + 1) * cellSize
      + "H" + (w1 + 1) * cellSize + "V" + 0
      + "H" + (w0 + 1) * cellSize + "Z";
}

function make_calendar(event_type) {
	
	url = "http://127.0.0.1:5000/api/".concat(event_type)
  	d3.json(url, function(error, data) {

  		console.log(event_type.concat("is loaded!"))
  	
    	var dataset = data['json_list']

    	var dataset_munged = d3.nest()
    		.key(function(d) { return format(new Date(d.date)); })
    		.rollup(function(events) { return d3.sum(events, function(d) {
    											return d.duration|| 0; }); })
    		.map(dataset);

    	var colors = ["#ffffd9","#edf8b1","#c7e9b4",
    	              "#7fcdbb","#41b6c4","#1d91c0",
    	              "#225ea8","#253494","#081d58"]
		var colorScale = d3.scale.quantize()
              // .domain([0, d3.max(dataset_munged, function (d) { return d.value; })])
              .domain([0, 200]) //TODO
              .range(colors);

    	rect
    	  .classed("day", true)
    	  .style("fill", function(d) { return colorScale(dataset_munged[d]); })

  	})
 }