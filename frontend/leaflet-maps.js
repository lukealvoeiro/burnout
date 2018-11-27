// JavaScript that works with the leaflet library
// to display an interactive map

$.getScript( "https://unpkg.com/leaflet@1.3.4/dist/leaflet.js", function() {
    console.log('Successfully loaded leaflet.js');
    initializeMap();
});

// import { addActiveFireMarkers } from './set-map-markers.js';
import * as activeFireData from './fire_locations.js';
import * as setMapMarkers from './set-map-markers.js';


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

    // TEST
    setMapMarkers.default(map);
    // setMapMarkers.addActiveFireMarkers(map);

    // L.marker([39.122, -122.097]).addTo(map).bindPopup("<b>2018-10-22</b><br>Time: 19:10<br>Latitude: 39.122<br>Longitude: -122.097");
    // L.marker([38.272, -120.31]).addTo(map).bindPopup("<b>2018-10-23</b><br>Time: 06:10<br>Latitude: 38.272<br>Longitude: -120.31");
    // L.marker([36.665, -121.375]).addTo(map).bindPopup("<b>2018-10-23</b><br>Time: 21:30<br>Latitude: 36.665<br>Longitude: -121.375");
    // L.marker([36.214, -118.641]).addTo(map).bindPopup("<b>2018-10-25</b><br>Time: 06:00<br>Latitude: 36.214<br>Longitude: -118.641");
    // L.marker([39.698, -122.285]).addTo(map).bindPopup("<b>2018-10-25</b><br>Time: 21:15<br>Latitude: 39.698<br>Longitude: -122.285");
    // L.marker([36.227, -118.628]).addTo(map).bindPopup("<b>2018-10-27</b><br>Time: 10:00<br>Latitude: 36.227<br>Longitude: -118.628");
    

    // Latitude
    
    //     "36.212",
    //     "36.218",
    //     "36.227"
    // Longitude
    
    //     "-118.643",
    //     "-118.636",
    //     "-118.628"
    // Time
    
    // "21:15",
    // "05:45",
    // "10:00"
    // 
    // Date
    
    //     "2018-10-25",
    //     "2018-10-27",
    //     "2018-10-27"
}

function addActiveFireMarkers(map) {
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

    for(let i = arraySize - 20; i < arraySize; i++) {
        activeFires.dates.push(dates[i]);
        activeFires.times.push(times[i]);
        activeFires.lats.push(lats[i]);
        activeFires.lons.push(lons[i]);
        
        let popupText = `<b>${dates[i]}</b><br>Time: ${times[i]}<br>Latitude: ${lats[i]}<br>Longitude: ${lons[i]}`;
        L.marker([lats[i], lons[i]]).addTo(map).bindPopup(popupText);
    }


    console.log(activeFires);
    console.log(arraySize);
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