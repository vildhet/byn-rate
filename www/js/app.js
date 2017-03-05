window.onload = function() {
    $.get('data/eurrub', drawCharts);
};

function drawCharts(values) {
    var data = [
        {
            values: values,
            key: 'Brent'
        }
    ];

    nv.addGraph(function() {
    var chart = nv.models.lineChart().useInteractiveGuideline(true);

    chart.xAxis.tickFormat(function(d) {
      return d3.time.format('%x')(new Date(d * 1000));
    });

    d3.select('#chart svg')
        .datum(data)
        .call(chart);

    nv.utils.windowResize(chart.update);
    return chart;
  });
}