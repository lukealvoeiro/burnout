// Funtion that parses through active fire data and adds
// recent active fires to the map

import * as activeFireData from './fire_locations.js';

$.getScript( "https://unpkg.com/leaflet@1.3.4/dist/leaflet.js", function() {
    console.log('Successfully loaded leaflet.js');
});

let globalMapVar,
    globalMapMarkers = [],
    globalHeatmapToggled = false,
    globalHeatmapLayer,
    globalMarkersToggled,
    globalNumOfMarkers,
    globalStartDate,
    globalEndDate;
let caNorthLat = 42,
    caSouthLat = 32.7,
    caEastLon = -116.3,
    caWestLon = -123.7
let corner1 = L.latLng(caNorthLat, caEastLon),
    corner2 = L.latLng(caSouthLat, caWestLon);


export function setGlobalMapVar(map) {
    globalMapVar = map;
}

export default function addActiveFireMarkers(startDate, endDate) {
    const dates = activeFireData.default.Date,
          times = activeFireData.default.Time,
          lats = activeFireData.default.Latitude,
          lons = activeFireData.default.Longitude;
    const arraySize = dates.length;

    const flameIcon = L.icon({
        iconUrl: './img/flame_icon.ico',
        iconSize: [40, 40],
        iconAnchor: [0, 0],
        popupAnchor: [20, -5],
    });

    // Find the first index of the starting date
    let startDateIndex = dates.indexOf(startDate),
        currentDate = startDate;
    let startMonth = startDate.substr(5, 2),
        startDay = startDate.substr(8),
        startYear = startDate.substr(0, 4),
        endMonth = endDate.substr(5, 2),
        endDay = endDate.substr(8),
        endYear = endDate.substr(0, 4),
        nextDay = parseInt(startDay) + 1,
        nextMonth = parseInt(startMonth),
        nextYear = parseInt(startYear);

    while (startDateIndex === -1) {
        if (nextDay > 31) { // max num of days in a month // CHECK FOR LEN OF DAYS/MONTHS
            nextDay = 1;
            nextMonth++;
            if (nextMonth > 12) { // max num of months in a year
                nextMonth = 1;
                nextYear++;
            }
        }
        let dayStr = (nextDay.toString().length < 2) ? `0${nextDay.toString()}` : nextDay.toString(),
            monthStr = (nextMonth.toString().length < 2) ? `0${nextMonth.toString()}` : nextMonth.toString(),
            yearStr = nextYear.toString(),
            nextDate = `${yearStr}-${monthStr}-${dayStr}`;
        
        startDateIndex = dates.indexOf(nextDate);
        currentDate = nextDate;

        nextDay++;
        console.log(`nextDate: ${nextDate}`);
    }
    let i = startDateIndex,
        endDatetime = new Date(endDate),
        currentDatetime = new Date(currentDate);
    
    while (currentDatetime <= endDatetime) {
        let popUpText = `<b>${dates[i]}</b><br>Time: ${times[i]}<br>Latitude: ${lats[i]}<br>Longitude: ${lons[i]}`;
        globalMapMarkers.push(L.marker([lats[i], lons[i]], {icon: flameIcon}).addTo(globalMapVar).bindPopup(popUpText));
        i++;
        currentDatetime = new Date(dates[i]); // doing this after so it gets next date
        console.log(`currentDateTime: ${currentDatetime}`);
    }
    globalStartDate = startDate;
    globalEndDate = endDate;
    globalMarkersToggled = true;
}

export function reloadMarkers(startDate, endDate) {
    for (let i = 0; i < globalMapMarkers.length; i++) {
        globalMapMarkers[i].remove();
    }
    addActiveFireMarkers(startDate, endDate);
}

export function toggleMarkers() {
    if (globalMarkersToggled) {
        globalMarkersToggled = false;
        for (let i = 0; i < globalMapMarkers.length; i++) {
            globalMapMarkers[i].remove();
        }
        console.log('Markers Removed.');
    } else {
        globalMarkersToggled = true;
        addActiveFireMarkers(globalMapVar, globalNumOfMarkers);
        console.log('Markers Added.');
    }
}

export function toggleHeatmap() {
    if (globalHeatmapToggled) {
        globalHeatmapToggled = false;
        globalHeatmapLayer.remove();
    } else {
        globalHeatmapToggled = true;
        globalHeatmapLayer = L.tileLayer('/heatmap/tiles/{z}/{x}/{y}.png', {
            noWrap: true,
            tms: true,
            opacity: 0.5,
        }).addTo(globalMapVar)
    }
}
