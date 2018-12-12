// File that controls jQuery UI elements on the webpage

import * as setMapMarkers from './set-map-markers.js';

$(document).ready(function() {
    let startDatePicker = $("#startdate").datepicker({
        dateFormat: "mm/dd/yyyy"
    });
    let endDatePicker = $("#enddate").datepicker({
        dateFormat: "mm/dd/yyyy"
    });

    $("#reloadFires").on("click", function() {
        let startDate = $('#startdate').val();
        let endDate = $('#enddate').val();

        let startMonth = startDate.substr(0, 2),
            startDay = startDate.substr(3, 2),
            startYear = startDate.substr(6),
            endMonth = endDate.substr(0, 2),
            endDay = endDate.substr(3, 2),
            endYear = endDate.substr(6);
        
        let startYMD = `${startYear}-${startMonth}-${startDay}`,
            endYMD = `${endYear}-${endMonth}-${endDay}`;
        
        let today = new Date(),
            endDatetime = new Date(endYMD);
        console.log(`End Date: ${startYear}; endDatetime: ${endYear}-${endMonth}-${endDay}`);
        console.log(`StartYear: ${startYMD.substr(0, 4)} StartMonth: ${startYMD.substr(5, 2)} StartDay: ${startYMD.substr(8)}`)

        if(parseInt(startYear) < 2014) {
            alert('Please enter a start date on or after 01/01/2014!');
        } else if (endDatetime > today) {
            alert(`Please enter an end date before today's date!`);
        } else {
            setMapMarkers.reloadMarkers(startYMD, endYMD);
        }
    });

    $("#toggleHeatmap").on("click", function() {
        setMapMarkers.toggleHeatmap();
    });

    $("#toggleMarkers").on("click", function() {
        setMapMarkers.toggleMarkers();
    });

    $("button").button();
});