// File that controls jQuery UI elements on the webpage

import * as setMapMarkers from './set-map-markers.js';

$(function() {
    let spinner = $('#markerNumber').spinner({
        min: 0,
        max: 1000,
        step: 1
    });
    let markerNumber;

    $("#reloadFires").on("click", function() {
        // alert(spinner.spinner("value"));
        markerNumber = spinner.spinner("value");
        if(markerNumber < 0) {
            alert('Number of fires must be greater than 0!');
        } else {
            setMapMarkers.reloadMarkers(markerNumber);
        }
    });

    $("button").button();
});