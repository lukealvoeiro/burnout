// Funtion that parses through active fire data and adds
// recent active fires to the map

import * as activeFireData from './fire_locations.js';
// import * as leafletHeat from './leaflet-heat.js';

$.getScript( "https://unpkg.com/leaflet@1.3.4/dist/leaflet.js", function() {
    console.log('Successfully loaded leaflet.js');
});

let globalMapVar;
let globalMapMarkers = [];

export default function addActiveFireMarkers(map, numOfMarkers) {
    const dates = activeFireData.default.Date,
          times = activeFireData.default.Time,
          lats = activeFireData.default.Latitude,
          lons = activeFireData.default.Longitude;
    const arraySize = dates.length;

    let activeFires = {
        dates: [],
        times: [],
        lats: [],
        lons: []
    }

    globalMapVar = map;

    const flameIcon = L.icon({
        iconUrl: './img/flame_icon.ico',
        iconSize: [40, 40],
        iconAnchor: [0, 0],
        popupAnchor: [20, -5],
    });

    // for(let i = arraySize - 100; i < arraySize; i++) {
    console.log(`numOfMarkers: ${numOfMarkers}`);
    if (numOfMarkers === undefined || numOfMarkers === null || numOfMarkers > arraySize) {
        numOfMarkers = arraySize;
    }
    for(let i = 0; i < numOfMarkers; i++) {
        activeFires.dates.push(dates[i]);
        activeFires.times.push(times[i]);
        activeFires.lats.push(lats[i]);
        activeFires.lons.push(lons[i]);
        
        let popUpText = `<b>${dates[i]}</b><br>Time: ${times[i]}<br>Latitude: ${lats[i]}<br>Longitude: ${lons[i]}`;
        globalMapMarkers.push(L.marker([lats[i], lons[i]], {icon: flameIcon}).addTo(map).bindPopup(popUpText));
    }

    // $.getScript( "./heatmap.js", function() {
    //     console.log('Successfully loaded heatmap.js');
    //     heatmapTest(map);
    // });


    console.log(activeFires);
    console.log(arraySize);
}

function getMarkerNumber() {
    // ToDo: Add button next to spinner that reruns the add active fire markers
    // Remove old markers first and then add new ones
}

export function reloadMarkers(numOfMarkers) {
    // Where to get map from???
    for (let i = 0; i < globalMapMarkers.length; i++) {
        globalMapMarkers[i].remove();
    }
    addActiveFireMarkers(globalMapVar, numOfMarkers);
    console.log(`Number of markers: ${numOfMarkers}`);
}

function heatmapTest(map) {
    $.getScript( "./leaflet-heatmap.js", function() {
        console.log('Successfully loaded leaflet-heatmap.js');
        // let heatMapArray = [];
        let heatMapArray = [{lat: 34, lng: -118.794, value: 5}, {lat: 34.1, lng: -118.9, value: 5}];
        let testData = {max: 8, data: heatMapArray};
        // for(let i = 0; i < arraySize; i++) {
        //     heatMapArray.push([lats[i], lons[i]])
        // }
        let cfg = {
            // radius should be small ONLY if scaleRadius is true (or small radius is intended)
            // if scaleRadius is false it will be the constant radius used in pixels
            "radius": 2,
            "maxOpacity": .8, 
            // scales the radius based on map zoom
            "scaleRadius": true, 
            // if set to false the heatmap uses the global maximum for colorization
            // if activated: uses the data maximum within the current map boundaries 
            //   (there will always be a red spot with useLocalExtremas true)
            "useLocalExtrema": true,
            // which field name in your data represents the latitude - default "lat"
            latField: 'lat',
            // which field name in your data represents the longitude - default "lng"
            lngField: 'lng',
            // which field name in your data represents the data value - default "value"
            valueField: 'value'
        };
        let heatmapLayer = new HeatmapOverlay(cfg);
        heatmapLayer.setData(testData);

        L.tileLayer(heatmapLayer).addTo(map);
        // let heat = L.heatLayer(heatMapArray).addTo(map);
    });
}
