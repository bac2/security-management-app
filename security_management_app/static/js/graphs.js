var margin = {top: 30, right: 20, bottom: 20, left: 80},
    width = 400 - margin.left - margin.right,
    height = 400 - margin.top - margin.bottom;

width = d3.select(d3.select("#graphs").node().parentNode).style("width");
width = width.substring(0, width.length-2) / 3 - 10;
width = width -margin.left - margin.right;
height = width * 3/4;

var y1 = d3.scale.ordinal()
    .rangeRoundBands([margin.top, height], .1);
	
var y2 = d3.scale.ordinal()
    .rangeRoundBands([margin.top, height], .1);

var y3 = d3.scale.ordinal()
    .rangeRoundBands([margin.top, height], .1);	
	
var y4 = d3.scale.ordinal()
    .rangeRoundBands([margin.top, height], .1);
	
var y5 = d3.scale.ordinal()
    .rangeRoundBands([margin.top, height], .1);	
	
var x1 = d3.scale.linear()
    .range([0, width]);
	
var x2 = d3.scale.linear()
    .range([0, width]);

var x3 = d3.scale.linear()
    .range([0, width]);

var x4 = d3.scale.linear()
    .range([0, width]);

var x5 = d3.scale.linear()
    .range([0, width]);	

var xAxis1 = d3.svg.axis()
    .scale(x1)
    .orient("top")
	.tickFormat(d3.format("d"))
	.ticks(5);
	
var xAxis2 = d3.svg.axis()
    .scale(x2)
    .orient("top")
	.tickFormat(d3.format("d"))
	.ticks(5);

var xAxis3 = d3.svg.axis()
    .scale(x3)
    .orient("top")
	.tickFormat(d3.format("d"))
	.ticks(5);
	
var xAxis4 = d3.svg.axis()
    .scale(x4)
    .orient("top")
	.tickFormat(d3.format("d"))
	.ticks(5);

var xAxis5 = d3.svg.axis()
    .scale(x5)
    .orient("top")
	.tickFormat(d3.format("d"))
	.ticks(5);	

var yAxis1 = d3.svg.axis()
    .scale(y1)
    .orient("left");
	
var yAxis2 = d3.svg.axis()
    .scale(y2)
    .orient("left");

var yAxis3 = d3.svg.axis()
    .scale(y3)
    .orient("left");

var yAxis4 = d3.svg.axis()
    .scale(y4)
    .orient("left");

var yAxis5 = d3.svg.axis()
    .scale(y5)
    .orient("left");	

var svg1 = d3.select("#graphs").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

var svg2 = d3.select("#graphs").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
	
var svg3 = d3.select("#graphs").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
	
var svg4 = d3.select("#graphs").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
	
var svg5 = d3.select("#graphs").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");	
	
d3.json("/dashboarddata", function(error, data){
	var selected = [];


	var devices = [];
	for (var i=0; i < data.length; i+=1) {
		devices.push(data[i]['fields']);
		if (!data[i]['fields']['vulnerability']) {
			data[i]['fields']['vulnerability'] = [];
		}
	}
	data = {'device':devices}
	
	var data = data['device'];
	
	var g1_data = g1(data);
	var g2_data = g2(data);
	var g3_data = g3(data);
	var g4_data = g4(data);
	var g5_data = g5(data);

	updateScales();	
	appendAxis();
	
	var filter = { uid : [], os : [], cve : [], severity : [], maxSeverity : [] }	
	
	//Number of Devices by OS
	svg1.append("text")
		.text("Devices by OS");
	svg1.selectAll(".bar")
		.data(g1_data)
	.enter().append("rect")
		.attr("class", "bar")
		.attr("y", function(d) { return y1(d.os); })
		.attr("height", function(d) { return y1.rangeBand(); })
		.attr("x", 0)
		.attr("width", function(d) { return x1(d.count); })
		.attr("fill", "steelblue")
		.on("click", function(d) {				
			var position = filter["os"].indexOf(d.os);
			if (position === -1){
				if (filter["os"].length === 0){
					svg1.selectAll("rect").attr("opacity", "0.5");
				}
				filter["os"].push(d.os);				
				d3.select(this).attr("opacity", "1");
			}
			else {
				if ( ~position ) filter["os"].splice(position, 1);
				if (filter["os"].length === 0){
					svg1.selectAll("rect").attr("opacity", "1");
				} else {
					d3.select(this).attr("opacity", "0.5");
				}
			}
			redraw();
		});		
	
	svg2.append("text")
		.text("Vulnerabilities by Machine");
	svg2.selectAll(".bar")
		.data(g2_data)
	.enter().append("rect")
		.attr("class", "bar")
		.attr("y", function(d) { return y2(d.nickname); })
		.attr("height", function(d) { return y2.rangeBand(); })
		.attr("x", 0)
		.attr("width", function(d) { return x2(d.count); })
		.attr("fill", "steelblue")		
		.on("click", function(d) {
			var position = filter["uid"].indexOf(d.nickname);
			if (position === -1){
				if (filter["uid"].length === 0){
					svg2.selectAll("rect").attr("opacity", "0.5");
				}			
				filter["uid"].push(d.nickname);
				d3.select(this).attr("opacity", "1");				
			}
			else {
				if ( ~position ) filter["uid"].splice(position, 1);
				if (filter["uid"].length === 0){
					svg2.selectAll("rect").attr("opacity", "1");
				} else {
					d3.select(this).attr("opacity", "0.5");
				}				
			}
			redraw();
		});
		
	svg3.append("text")
		.text("Vulnerabilities by Severity");
	svg3.selectAll(".bar")
		.data(g3_data)
	.enter().append("rect")
		.attr("class", "bar")
		.attr("y", function(d) { return y3(d.severity); })
		.attr("height", function(d) { return y3.rangeBand(); })
		.attr("x", 0)
		.attr("width", function(d) { return x3(d.count); })
		.attr("fill", function(d) {
			if (d.severity === "high") { return "red"; }
			if (d.severity === "medium") { return "orange"; }
			if (d.severity === "low") { return "yellow"; }
			return "grey";
		})
		.on("click", function(d) {
			var position = filter["severity"].indexOf(d.severity);
			if (position === -1){
				if (filter["severity"].length === 0){
					svg3.selectAll("rect").attr("opacity", "0.5");
				}			
				filter["severity"].push(d.severity);
				d3.select(this).attr("opacity", "1");	
			}
			else {
				if ( ~position ) filter["severity"].splice(position, 1);
				if (filter["severity"].length === 0){
					svg3.selectAll("rect").attr("opacity", "1");
				} else {
					d3.select(this).attr("opacity", "0.5");
				}						
			}
			redraw();
		});			
		

	svg4.append("text")
		.text("Devices By Max Severity");
	svg4.selectAll(".bar")
		.data(g4_data)
	.enter().append("rect")
		.attr("class", "bar")
		.attr("y", function(d) { return y4(d.severity); })
		.attr("height", function(d) { return y4.rangeBand(); })
		.attr("x", 0)
		.attr("width", function(d) { return x4(d.count); })
		.attr("fill", function(d) {
			if (d.severity === "high") { return "red"; }
			if (d.severity === "medium") { return "orange"; }
			if (d.severity === "low") { return "yellow"; }
			return "grey";
		})		
		.on("click", function(d) {
			var position = filter["maxSeverity"].indexOf(d.severity);
			if (position === -1){
				if (filter["maxSeverity"].length === 0){
					svg4.selectAll("rect").attr("opacity", "0.5");
				}			
				filter["maxSeverity"].push(d.severity);
				d3.select(this).attr("opacity", "1");		
			}
			else {
				if ( ~position ) filter["maxSeverity"].splice(position, 1);
				if (filter["maxSeverity"].length === 0){
					svg4.selectAll("rect").attr("opacity", "1");
				} else {
					d3.select(this).attr("opacity", "0.5");
				}				
			}
			redraw();
		});				
		
	svg5.append("text")
		.text("Devices by Vulnerability");
	svg5.selectAll(".bar")
		.data(g5_data)
	.enter().append("rect")
		.attr("class", "bar")
		.attr("y", function(d) { return y5(d.cve); })
		.attr("height", function(d) { return y5.rangeBand(); })
		.attr("x", 0)
		.attr("width", function(d) { return x5(d.count); })		
		.on("click", function(d) {
			var position = filter["cve"].indexOf(d.cve);
			if (position === -1){
				if (filter["cve"].length === 0){
					svg5.selectAll("rect").attr("opacity", "0.5");
				}			
				filter["cve"].push(d.cve);
				d3.select(this).attr("opacity", "1");					
			}
			else {
				if ( ~position ) filter["cve"].splice(position, 1);
				if (filter["cve"].length === 0){
					svg5.selectAll("rect").attr("opacity", "1");
				} else {
					d3.select(this).attr("opacity", "0.5");
				}						
			}
			redraw();
		});				
	
	
	
	function redraw(){
		var filtered_data = [];
		for (var i = 0; i < data.length; i++){
			var allowed = false;
			if (filter.uid.length === 0){ allowed = true; }
			for (var j = 0; j < filter.uid.length; j++){
				if (data[i].uid === filter.uid[j]){ allowed = true; }
			}
			if (!allowed) {	continue; }
			
			allowed = false;
			if (filter.os.length === 0){ allowed = true; }
			for (var j = 0; j < filter.os.length; j++){
				if (data[i].os === filter.os[j]){ allowed = true; }
			}
			if (!allowed) {	continue; }

			allowed = false;
			if (filter.cve.length === 0){ allowed = true; }
			for (var j = 0; j < filter.cve.length; j++){
				for (var k = 0; k < data[i]["vulnerability"].length; k++){
					if (data[i]["vulnerability"][k]["cve"] === filter.cve[j]){ allowed = true; }
				}
				
			}
			if (!allowed) {	continue; }

			allowed = false;
			if (filter.severity.length === 0){ allowed = true; }
			for (var j = 0; j < filter.severity.length; j++){
				for (var k = 0; k < data[i]["vulnerability"].length; k++){
					var score = data[i]["vulnerability"][k]["score"];
					var severity = "unknown";
					if (0 <= score && score <= 3.9){
						severity = "low";
					}
					else if (4.0 <= score && score <= 6.9){
						severity = "medium";
					}
					else if (7.0 <= score && score <= 10.0){
						severity = "high";
					}		
					if (severity === filter.severity[j]){ allowed = true; }	
				}				
			}
			if (!allowed) {	continue; }
			
			allowed = false;
			if (filter.maxSeverity.length === 0){ allowed = true; }
			for (var j = 0; j < filter.maxSeverity.length; j++){
				var maxSeverity = -1;
				for (var k = 0; k < data[i]["vulnerability"].length; k++){
					if (maxSeverity < data[i]["vulnerability"][k]["score"]){
						maxSeverity = data[i]["vulnerability"][k]["score"];
					}
				}
				var severity = "unknown";
				if (0 <= maxSeverity && maxSeverity <= 3.9){
					severity = "low";
				}
				else if (4.0 <= maxSeverity && maxSeverity <= 6.9){
					severity = "medium";
				}
				else if (7.0 <= maxSeverity && maxSeverity <= 10.0){
					severity = "high";
				}		
				if (severity === filter.maxSeverity[j]){ allowed = true; }						
			}					
			if (!allowed) {	continue; }			
			
			filtered_data.push(data[i]);
		}		
		
		console.log(filter);
		
		if (filter["os"].length === 0){
			g1_data = g1(filtered_data);
		}		
		
		if (filter["uid"].length === 0){
			g2_data = g2(filtered_data);
		}		
		
		if (filter["cve"].length === 0){
			g5_data = g5(filtered_data);
		}				
		
		if (filter["severity"].length === 0){
			g3_data = g3(filtered_data);
		}	
			
		if (filter["maxSeverity"].length === 0){
			g4_data = g4(filtered_data);
		}		

		if (filter["cve"].length === 0){
			g5_data = g5(filtered_data);
		}		

		updateScales();
		removeAxis();
		appendAxis();

		var new1 = svg1.selectAll("rect")
			.data(g1_data);
			
		new1.enter().append("rect")
			.attr("class", "bar")
			.on("click", function(d) {
				console.log(d);
				var position = filter["os"].indexOf(d.os);
				if (position === -1){
					filter["os"].push(d.os);
				}
				else {
					if ( ~position ) filter["os"].splice(position, 1);
				}
				redraw("g1");
			});
		
		new1.transition()			
			.duration(500)
			.delay(200)
			.attr("y", function(d) { return y1(d.os); })
			.attr("height", function(d) { return y1.rangeBand(); })
			.attr("x", 0)
			.attr("width", function(d) { return x1(d.count); });
		
		new1.exit().transition().duration(500).attr("width", 0).remove();
		
		var new2 = svg2.selectAll("rect")
			.data(g2_data);
			
		new2.enter().append("rect")
			.attr("class", "bar")
			.on("click", function(d) {
				var position = filter["uid"].indexOf(d.nickname);
				if (position === -1){
					filter["uid"].push(d.nickname);
				}
				else {
					if ( ~position ) filter["uid"].splice(position, 1);
				}
				redraw("g2");
			});	
		
		new2.transition()			
			.duration(500)
			.delay(200)
			.attr("y", function(d) { return y2(d.nickname); })
			.attr("height", function(d) { return y2.rangeBand(); })
			.attr("x", 0)
			.attr("width", function(d) { return x2(d.count); });
		
		new2.exit().transition().duration(500).attr("width", 0).remove();
		
		var new3 = svg3.selectAll("rect")
			.data(g3_data);
			
		new3.enter().append("rect")
			.attr("class", "bar")
			.on("click", function(d) {
				var position = filter["severity"].indexOf(d.severity);
				if (position === -1){
					filter["severity"].push(d.severity);
				}
				else {
					if ( ~position ) filter["severity"].splice(position, 1);
				}
				redraw("g3");
			});		
		
		new3.transition()			
			.duration(500)
			.delay(200)
			.attr("y", function(d) { return y3(d.severity); })
			.attr("height", function(d) { return y3.rangeBand(); })
			.attr("x", 0)
			.attr("width", function(d) { return x3(d.count); });
		
		new3.exit().transition().duration(500).attr("width", 0).remove();

		var new4 = svg4.selectAll("rect")
			.data(g4_data);
			
		new4.enter().append("rect")
			.attr("class", "bar")
			.on("click", function(d) {
				var position = filter["severity"].indexOf(d.severity);
				if (position === -1){
					filter["severity"].push(d.severity);
				}
				else {
					if ( ~position ) filter["severity"].splice(position, 1);
				}
				redraw("g4");
			});		
		
		new4.transition()			
			.duration(500)
			.delay(200)
			.attr("y", function(d) { return y4(d.severity); })
			.attr("height", function(d) { return y4.rangeBand(); })
			.attr("x", 0)
			.attr("width", function(d) { return x4(d.count); });
		
		new4.exit().transition().duration(500).attr("width", 0).remove();

		var new5 = svg5.selectAll("rect")
			.data(g5_data);
			
		new5.enter().append("rect")
			.attr("class", "bar")
			.on("click", function(d) {
				var position = filter["cve"].indexOf(d.cve);
				if (position === -1){
					filter["cve"].push(d.cve);
				}
				else {
					if ( ~position ) filter["cve"].splice(position, 1);
				}
				redraw("g5");
			});
		
		new5.transition()			
			.duration(500)
			.delay(200)
			.attr("y", function(d) { return y5(d.cve); })
			.attr("height", function(d) { return y5.rangeBand(); })
			.attr("x", 0)
			.attr("width", function(d) { return x5(d.count); });
		
		new5.exit().transition().duration(500).attr("width", 0).remove();		
		
	}
	
	//Number of Devices by OS
	function g1(data){
		var osCount = {};
		var g1_data = [];
		
		data.map(function (item) {
			if (osCount.hasOwnProperty(item.os)) {
				osCount[item.os] += 1;
			} else {
				osCount[item.os] = 1;
			}
		});
			
		for (var key in osCount) {
			if (osCount.hasOwnProperty(key)){
				g1_data.push({os : key, count : osCount[key]});
			}		
		}
		
		return g1_data;
	}
	
	//Number of Vulnerabilities by Device
	function g2(data){
		var g2_data = [];
		for (var i = 0; i < data.length; i++){
			g2_data.push({nickname: data[i].nickname, uid : data[i].uid, count : data[i].vulnerability.length});
		}
		return g2_data;
	}
	
	//Number of Vulnerabilities by Severity
	function g3(data){
		var severityCount = {};
		var g3_data = [];
		
		for (var i = 0; i < data.length; i++){			
			data[i]["vulnerability"].map(function (item) {
				var severity = "unknown";
				if (0 <= item.score && item.score <= 3.9){
					severity = "low";
				}
				else if (4.0 <= item.score && item.score <= 6.9){
					severity = "medium";
				}
				else if (7.0 <= item.score && item.score <= 10.0){
					severity = "high";
				}
				if (severityCount.hasOwnProperty(severity)) {
					severityCount[severity] += 1;
				}
				else {
					severityCount[severity] = 1;
				}
			});				
		}
		
		for (var key in severityCount){
			if (severityCount.hasOwnProperty(key)){
				g3_data.push({ severity : key, count : severityCount[key]});
			}				
		}
		
		return g3_data;
	}
	
	//Number of Devices by Max Severity
	function g4(data){
		var severityCount = {};
		var g4_data = [];
		
		for (var i = 0; i < data.length; i++){
			var maxSeverity = -1;
			for (var j = 0; j < data[i]["vulnerability"].length; j++){
				if (maxSeverity < data[i]["vulnerability"][j]["score"]){
					maxSeverity = data[i]["vulnerability"][j]["score"];
				}
			}
			var severity = "unknown";
			if (0 <= maxSeverity && maxSeverity <= 3.9){
				severity = "low";
			}
			else if (4.0 <= maxSeverity && maxSeverity <= 6.9){
				severity = "medium";
			}
			else if (7.0 <= maxSeverity && maxSeverity <= 10.0){
				severity = "high";
			}			
			if (severityCount.hasOwnProperty(severity)) {
				severityCount[severity] += 1;
			}
			else {
				severityCount[severity] = 1;
			}						
		}
		
		for (var key in severityCount){
			if (severityCount.hasOwnProperty(key)){
				g4_data.push({ severity : key, count : severityCount[key]});
			}				
		}				
		
		return g4_data;
	}
	
	//Number of Devices by Vulnerability
	function g5(data){
		var cveCount = {};
		var g5_data = [];
		
		for (var i = 0; i < data.length; i++){			
			data[i]["vulnerability"].map(function (item) {
				if (cveCount.hasOwnProperty(item.cve)) {
					cveCount[item.cve] += 1;
				}
				else {
					cveCount[item.cve] = 1;
				}
			});				
		}		
		
		for (var key in cveCount){
			if (cveCount.hasOwnProperty(key)){
				g5_data.push({ cve : key, count : cveCount[key]});
			}				
		}		
		return g5_data;
	}
	
	function updateScales(){
		x1.domain([0, d3.max(g1_data, function(d) { return d.count; })]);
		y1.domain(g1_data.map(function(d) { return d.os; }));	
		x2.domain([0, d3.max(g2_data, function(d) { return d.count; })]);
		y2.domain(g2_data.map(function(d) { return d.nickname; }));
		x3.domain([0, d3.max(g3_data, function(d) { return d.count; })]);
		y3.domain(g3_data.map(function(d) { return d.severity; }));
		x4.domain([0, d3.max(g4_data, function(d) { return d.count; })]);
		y4.domain(g4_data.map(function(d) { return d.severity; }));
		x5.domain([0, d3.max(g5_data, function(d) { return d.count; })]);
		y5.domain(g5_data.map(function(d) { return d.cve; }));
	}	

	function removeAxis(){
		svg1.selectAll("g").remove();
		svg2.selectAll("g").remove();
		svg3.selectAll("g").remove();
		svg4.selectAll("g").remove();
		svg5.selectAll("g").remove();
	}
	
	function appendAxis(){
		svg1.append("g")
			.attr("class", "x axis")
			.attr("transform", "translate(0, "+margin.top+")")
			.call(xAxis1);
		svg1.append("g")
			.attr("class", "y axis")
			.call(yAxis1);
			
		svg2.append("g")
			.attr("class", "x axis")
			.attr("transform", "translate(0, "+margin.top+")")
			.call(xAxis2);
		svg2.append("g")
			.attr("class", "y axis")
			.call(yAxis2);	
			
		svg3.append("g")
			.attr("class", "x axis")
			.attr("transform", "translate(0, "+margin.top+")")
			.call(xAxis3);
		svg3.append("g")
			.attr("class", "y axis")
			.call(yAxis3);
			
		svg4.append("g")
			.attr("class", "x axis")
			.attr("transform", "translate(0, "+margin.top+")")
			.call(xAxis4);
		svg4.append("g")
			.attr("class", "y axis")
			.call(yAxis4);	
			
		svg5.append("g")
			.attr("class", "x axis")
			.attr("transform", "translate(0, "+margin.top+")")
			.call(xAxis5);
		svg5.append("g")
			.attr("class", "y axis")
			.call(yAxis5);			
	}
	
})

