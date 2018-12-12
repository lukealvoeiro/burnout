// JavaScript that works with the leaflet library
// to display an interactive map

$.getScript( "https://unpkg.com/leaflet@1.3.4/dist/leaflet.js", function() {
    console.log('Successfully loaded leaflet.js');
    initializeMap();
});

import * as activeFireData from './fire_locations.js';
import * as setMapMarkers from './set-map-markers.js';


function initializeMap() {
    var map = L.map('mapid', {
        center: [37.641, -120.761], // Waterford, CA; roughly the middle of the state
        zoom: 6
    });

    L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        maxZoom: 18,
        id: 'mapbox.streets',
        accessToken: 'sk.eyJ1IjoiZ2tsaW5lIiwiYSI6ImNqbXByeWI3cTAwb2szcHFxOGYzd2Nma2sifQ.iOVtTFJBs_1AvF_6JPmVyw'
    }).addTo(map);

    setMapMarkers.setGlobalMapVar(map);
    setMapMarkers.default('2018-10-01', '2018-12-01');
}