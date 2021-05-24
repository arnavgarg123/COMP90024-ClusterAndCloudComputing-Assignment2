mapboxgl.accessToken = 'pk.eyJ1IjoiZ3Vya2kwOSIsImEiOiJja29iejNiZjkxaWg0MndtdTFiZzdkcXVnIn0.hTqur4keYNgXKLjldLaVEw';
var map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/streets-v11',
    center: [134.946457, -26.840935],
    minZoom: 3.5,
    zoom: 3.8
});
var hoveredStateId = null;
var zoomThreshold = 4.4;

map.on('load', function () {
    map.resize();
    map.addSource('boundary', {
        'type': 'geojson',
        'data': '../static/data_files/aus_states_boundary.geojson'
    });

    map.addLayer({
        'id': 'aus_states',
        'type': 'fill',
        'source': 'boundary',
        'layout': {},
        'paint': {
            'fill-color': '#2f4f4f',
            'fill-opacity': [
                'case',
                ['boolean', ['feature-state', 'hover'], false],
                0.7,
                0.3
            ]
        }
    });
    map.addLayer({
        'id': 'outline',
        'type': 'line',
        'source': 'boundary',
        'layout': {},
        'paint': {
            'line-color': '#000',
            'line-width': 2
        }
    });

    map.addSource('pt', {
        "type": "geojson",
        "data": "../static/data_files/map_points.geojson"
    });

    map.addLayer({
        'id': 'aus_cities',
        'type': 'circle',
        'minzoom': zoomThreshold,
        'source': 'pt',
        'layout': {},
        'paint': {
            'circle-radius': ['get','radius'],
            'circle-color': '#B42222',
            'circle-opacity': 0.3
        }
    });
    var popup = new mapboxgl.Popup({
        closeButton: false,
        closeOnClick: false
    });

    map.on('mouseenter', 'aus_cities', function (e) {
        map.getCanvas().style.cursor = 'pointer';
        var coordinates = e.features[0].geometry.coordinates;
        var city = e.features[0].properties.city;
        var num_tweets=e.features[0].properties.num_tweets;
        var num_users=e.features[0].properties.num_users;
        var popup_text = '<h5>'+ city +'</h5><p> Number of Tweets: <strong>' + num_tweets + '</strong> <br>Number of Users: <strong>'+ num_users+ '</strong></p>'
        popup.setLngLat(coordinates).setHTML(popup_text).addTo(map);
    });

    map.on('mouseleave', 'aus_cities', function () {
        map.getCanvas().style.cursor = '';
        popup.remove();
    });


});

map.on('mousemove', 'aus_states', function (e) {
    if (e.features.length > 0) {
        if (hoveredStateId !== null) {
            map.setFeatureState(
                { source: 'boundary', id: hoveredStateId },
                { hover: false }
            );
        }
        hoveredStateId = e.features[0].id;
        map.setFeatureState(
            { source: 'boundary', id: hoveredStateId },
            { hover: true }
        );
    }
});

map.on('mouseenter', 'aus_states', function () {
    map.getCanvas().style.cursor = 'pointer';
});

map.on('mouseleave', 'aus_states', function () {
    if (hoveredStateId !== null) {
        map.setFeatureState(
            { source: 'boundary', id: hoveredStateId },
            { hover: false }
        );
    }
    hoveredStateId = null;
});

map.on('click', 'aus_states', function (e) {
    show_element('resetmap');
    var center_lat = e.features[0].properties.CENTER_LAT;
    var center_long = e.features[0].properties.CENTER_LONG;
    var zoom_pt = e.features[0].properties.ZOOM_PT;
    map.flyTo({ center: [center_lat, center_long], zoom: zoom_pt });
});

document.getElementById('resetmap').addEventListener('click', function () {
    map.flyTo({
        center: [134.946457, -26.840935],
        zoom: 3.8
    });
    hide_element('resetmap');
});
