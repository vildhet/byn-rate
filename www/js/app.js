const nv = require('nvd3');
const d3 = require('d3');
const $ = require('jquery');
const async = require('async');

window.onload = function() {
    async.parallel([
        next => $.get('data/brent', data => {
            next(null, {
                values: data,
                key: 'Brent',
                color: '#ff7f0e'
            });
        }),
        next => $.get('data/eurrub', data => {
            next(null, {
                values: data,
                key: 'Eur/Rub',
                color: '#2ca02c'
            });
        })
    ], function(error, results) {
        drawCharts(results);
    });
};

function drawCharts(data) {
    nv.addGraph(() => {
        var chart = nv.models.lineChart().useInteractiveGuideline(true);

        chart.xAxis.tickFormat(d => {
            return d3.time.format('%x')(new Date(d * 1000));
        });

        d3.select('#chart svg').datum(data).call(chart);

        nv.utils.windowResize(chart.update);
        return chart;
    });
}