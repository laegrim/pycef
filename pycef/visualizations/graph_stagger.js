
var width = 1920,
	 height = 1080,
	 timer = null,
	 level = 1,
	 max = 110,
	 duration = 10000;
	


var force = d3.layout.force()
				.charge(-300)
				.linkDistance(60)
				.size([width, height]);

var svg = d3.select("body").append("svg")
				.attr("width", width)
				.attr("height", height)
				.append("g");

d3.json("test_stagger_graph.json", function(error, graph) {

	force.nodes(graph.nodes)
		 	.links(graph.links)
		 	.start();
	
	var link = svg.selectAll("line.link")
					.data(graph.links)
					.enter().append("line")
					.attr("class", "link")
					.style("stroke-width", function(d) { return 2;});
					
	var node = svg.selectAll("node")
					.data(graph.nodes)
					.enter().append("svg")
					.attr("class", "node")
					.call(force.drag);
					
	var circle = node.append("svg:circle")
					.attr("r", 5);
					
	var text = node.append("svg:text")
					.attr("dx", 12)
					.attr("dy", ".35em")
					.attr("color", "#00B")
					.attr("font", "10px sans-serif")
					.attr("font-size", "10")
					.text(function (d) {return d.id;});
			
 	force.on("tick", function () {
			link.attr("x1", function (d) { return d.source.x; })
				.attr("y1", function (d) { return d.source.y; })
				.attr("x2", function (d) { return d.target.x; })
				.attr("y2", function (d) { return d.target.y; });
				
			circle.attr("cx", function(d) { return d.x;})
				.attr("cy", function (d) { return d.y;});
				
			text.attr("x", function(d) {return d.x;})
				.attr("y", function(d) {return d.y;});
	});
});		
