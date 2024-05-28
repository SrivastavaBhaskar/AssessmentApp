var chart = circularHeatChart()

const domains_data = JSON.parse(document.getElementById('data').textContent);

console.log(domains_data)

var segments = []

const domains = Object.keys(domains_data.domains)

domains.forEach(domain => {
    const seg = Object.keys(domains_data.domains[domain]['subDomains'])
    segments.push(...seg)
});

console.log(segments)

var levels = []

for(i = 1; i <= domains_data.highestQuestionLevel; i++){
    levels.push("Level: " + i);
}

console.log(levels)

data = [];

for(var i=0; i<(levels.length * segments.length); i++) {
    data[i] = {title: "Segment "+i, value: Math.random()};
}

var margin = {
    top: 50,
    right: 50,
    bottom: 50,
    left: 50,
};
var width = 1250 - margin.left - margin.right;
var height = width;
var innerRadius = 100; 

var segmentHeight = (width - margin.top - margin.bottom - 2 * innerRadius) /
    (2 * levels.length);

chart.accessor(function(d) {return d.value;})
    .segmentHeight(segmentHeight)
    .innerRadius(30)
    .numSegments(segments.length)
    .range(["white", "#F6652B"])
    .radialLabels(levels)
    .segmentLabels(segments)

d3.select('#chart')
    .selectAll('svg')
    .data([data])
    .enter()
    .append('svg')
    .attr('width', '110%') // 70% forces the heatmap down
    .attr('height', height - margin.top - (2 * margin.bottom))
    .call(chart);

/* Add a mouseover event */
d3.selectAll("#chart path").on('click', function() {
	var d = d3.select(this).data()[0];
    d3.select(this).data()[0].value = d3.select(this).data()[0].value + 1;
    d3.select("#info").text(d.title + ' has value ' + d.value);
    d3.select("#info").text('this ' + JSON.stringify(d3.select(this)));
});
d3.selectAll("#chart svg").on('mouseout', function() {
    d3.select("#info").text('');	
});
