// JavaScript that works with the leaflet library
// to display an interactive map

$.getScript( "https://unpkg.com/leaflet@1.3.4/dist/leaflet.js", function() {
    console.log('Successfully loaded leaflet.js');
    initializeMap();
});

// import L from 'leaflet';

function initializeMap() {
    // L = leaflet;

    var map = L.map('mapid', {
        center: [37.641, -120.761], // Waterford, CA
        zoom: 6
    });

    L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        maxZoom: 18,
        id: 'mapbox.streets',
        accessToken: 'sk.eyJ1IjoiZ2tsaW5lIiwiYSI6ImNqbXByeWI3cTAwb2szcHFxOGYzd2Nma2sifQ.iOVtTFJBs_1AvF_6JPmVyw'
    }).addTo(map);
}

function addActiveFireMarkers() {
    var fireDataCSV = 'fire_locations.csv';
    var activeFireData = $.csv.toObjects(fireDataCSV, {separator: ' '}, (err, data) => {
        console.log(activeFireData);
    });
}


////////////////////////////////////////////////////////////////////////

// L = leaflet;

// $.getScript( "https://unpkg.com/leaflet@1.3.4/dist/leaflet.js", function() {
//     console.log('Successfully loaded leaflet.js');
//   });

// var map = L.map('mapid', {
//     center: [37.641, -120.761], // Waterford, CA
//     zoom: 6
// });

// L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
//     attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
//     maxZoom: 18,
//     id: 'mapbox.streets',
//     accessToken: 'sk.eyJ1IjoiZ2tsaW5lIiwiYSI6ImNqbXByeWI3cTAwb2szcHFxOGYzd2Nma2sifQ.iOVtTFJBs_1AvF_6JPmVyw'
// }).addTo(map);

// create script elements and link to them within the head
// JQuery get script function
// Inititialize map once and pass it around (figure out how to import it in HTML and use it this JS file)
// Map out what different classes and stuff that we'd need
// Make an option to show band layers and other layers in final map cause it's cool
// and also shows users how we calculated the final result
// 
// good first stop: use pymodis to get an image and display it on our map/frontend
// run whole thing on Node.js
// python provides local HTTP server capabilities using localhost (simpleHTTPserver)