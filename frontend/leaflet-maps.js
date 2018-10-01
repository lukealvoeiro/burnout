// JavaScript that works with the leaflet library
// to display an interactive map

import {leaflet} from 'leaflet';

L = leaflet;

var map = L.map('map', {
    center: [51.505, -0.09],
    zoom: 13
});

L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox.streets',
    accessToken: 'sk.eyJ1IjoiZ2tsaW5lIiwiYSI6ImNqbXByeWI3cTAwb2szcHFxOGYzd2Nma2sifQ.iOVtTFJBs_1AvF_6JPmVyw'
}).addTo(map);