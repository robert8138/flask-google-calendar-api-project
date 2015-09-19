d3.select("#clickme").on("click", make_graph);

function make_graph() {
  url = "http://localhost:5000/api/all"
  d3.json(url, function(error, data) {
    console.log(mydata)
  });
}