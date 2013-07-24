var directionsDisplay;
var map;
var initialLocation;
var markers     = [];
var venues      = [];
var siberia     = new google.maps.LatLng(60, 105);
var stuttgart   = new google.maps.LatLng(48.77065656676112, 9.179780947082463);
var infowindow  = new google.maps.InfoWindow();
var bounds      = new google.maps.LatLngBounds();
var browserSupportFlag =  new Boolean();
var directionsService = new google.maps.DirectionsService();


foodninja = {
	init: function() {
		// load jQuery from google cdn or fallback to local version
		Modernizr.load([{
			load: '//ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js',
			complete: function () {
				if ( !window.jQuery ) {
					Modernizr.load('/js/libs/jquery-1.7.1.min.js');
				}
			}
		},{
			// load scripts with jquery dependencies
			load: plugins,
			callback: function() {
				foodninja.google.maps();
			}
		}]);
	},
	google: {
		maps: function() {
			directionsDisplay = new google.maps.DirectionsRenderer({
				markerOptions: {
					visible: false
				}
			});

			var myOptions = {
				zoom: 15,
				mapTypeId: google.maps.MapTypeId.ROADMAP
			};

			map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);
			directionsDisplay.setMap(map);

			google.maps.event.addListener(map, 'click', function(event) {
				foodninja.google.setmarker(event.latLng);
			});
			if(lat == '' && lon == '') {
				// Try W3C Geolocation method (Preferred)
				if(navigator.geolocation) {
					browserSupportFlag = true;

					navigator.geolocation.getCurrentPosition(function(position) {
						initialLocation = new google.maps.LatLng(position.coords.latitude,position.coords.longitude);

						$('#latitude').val(position.coords.latitude);
						$('#longitude').val(position.coords.longitude);

						foodninja.google.setmarker(initialLocation);
					}, function() {
						hereandleNoGeolocation(browserSupportFlag);
					});
				} else if (google.gears) {
					// Try Google Gears Geolocation
					browserSupportFlag = true;

					var geo = google.gears.factory.create('beta.geolocation');
					geo.getCurrentPosition(function(position) {
						initialLocation = new google.maps.LatLng(position.latitude,position.longitude);

						$('#latitude').val(position.latitude);
						$('#longitude').val(position.longitude);

						foodninja.google.setmarker(initialLocation);
					}, function() {
					 	handleNoGeolocation(browserSupportFlag);
					});
				} else {
					// Browser doesn't support Geolocation
					browserSupportFlag = false;

					handleNoGeolocation(browserSupportFlag);
				}
			} else {
				initialLocation = new google.maps.LatLng(lat,lon);

				$('#latitude').val(lat);
				$('#longitude').val(lon);

				foodninja.google.setmarker(initialLocation);
				foodninja.google.parsevenues();
			}
		},
		nolocation: function(errorFlag) {
			if (errorFlag == true) {
				initialLocation = stuttgart;
			} else {
				initialLocation = siberia;
			}
			foodninja.google.setmarker(initialLocation);
		},
		setmarker: function(location) {
			foodninja.google.clearmarkers();

			var marker = new google.maps.Marker({
				position: location,
				map: map,
				icon: 'http://maps.google.com/mapfiles/kml/pal3/icon56.png',
				title: 'You\'re here'
			});
			markers.push(marker);
			map.setZoom(15);
			map.setCenter(location);

			$('#latitude').val(location.jb);
			$('#longitude').val(location.kb);
		},
		clearmarkers: function() {
			if (markers) {
				for (i in markers) {
					markers[i].setMap(null);
				}
			}
		},
		parsevenues: function() {
			if (venuesArray) {
				for (i in venuesArray) {
					var contentString = '<img src="' + venuesArray[i].iconlarge.slice(0, -3) + '_bg' + venuesArray[i].iconlarge.slice(-3) +'.png" class="icon floatleft">' + 
										'<div class="floatleft"><h2>' + venuesArray[i].name + '</h2><h3>' + venuesArray[i].category + ' (' + venuesArray[i].distance + 'm) </h3>' + 
										'<a href="' + venuesArray[i].url + '" target="blank"><img src="https://playfoursquare.s3.amazonaws.com/press/logo/checkinon-blue.png"></a>';
					if (venuesArray[i].street) {
						contentString += '<p>' + venuesArray[i].street + '<br>'+ venuesArray[i].city +'<br>';
						if (venuesArray[i].phone) {
							contentString += 'T: ' + venuesArray[i].phone;
						}
						contentString += '</p>'
					}
					contentString += '</div>';

					var location = new google.maps.LatLng(venuesArray[i].lat, venuesArray[i].lng);

					venues.push(foodninja.google.createvenue(venuesArray[i],location,contentString));
					venues[i].setVisible(true);
				}
			}

			if (recommendedVenueObject) {
				var contentString = '<img src="' + venuesArray[i].iconlarge.slice(0, -3) + '_bg' + venuesArray[i].iconlarge.slice(-3) +'.png" class="icon floatleft">' + 
									'<div class="floatleft"><h2>' + venuesArray[i].name + '</h2><h3>' + venuesArray[i].category + ' (' + venuesArray[i].distance + 'm) </h3>' + 
									'<a href="' + venuesArray[i].url + '" target="blank"><img src="https://playfoursquare.s3.amazonaws.com/press/logo/checkinon-blue.png"></a>';
				if (venuesArray[i].street) {
					contentString += '<p>' + venuesArray[i].street + '<br>'+ venuesArray[i].city +'<br>';
					if (venuesArray[i].phone) {
						contentString += 'T: ' + venuesArray[i].phone;
					}
					contentString += '</p>'
				}
				contentString += '</div>';

				var location = new google.maps.LatLng(venuesArray[i].lat, venuesArray[i].lng);
				recommendedVenue = foodninja.google.createrecommendedvenue(recommendedVenueObject,location,contentString);
				recommendedVenue.setVisible(true);
				var request = {
					origin:initialLocation,
					destination:location,
					travelMode: google.maps.DirectionsTravelMode.WALKING
				};
				directionsService.route(request, function(response, status) {
				if (status == google.maps.DirectionsStatus.OK) {
					directionsDisplay.setDirections(response);
				}
				});

			}
		},
		createvenue: function(object,location,content) {
			var venue = new google.maps.Marker({
				position: location,
				map: map,
				title: object.name + ' - ' + object.category,
				icon: object.icon.slice(0, -3) + '_bg' + object.icon.slice(-3) + '.png',
			});

			google.maps.event.addListener(venue, 'click', function() {
				infowindow.setContent(content);
				infowindow.open(map,venue);
			});

			return venue;
		},
		createrecommendedvenue: function(object,location,content) {
			var venue = new google.maps.Marker({
				position: location,
				map: map,
				title: object.name + ' - ' + object.category,
				icon: object.icon.slice(0, -3) + '_bg' + object.icon.slice(-3) + '.png',
			});

			google.maps.event.addListener(venue, 'click', function() {
				infowindow.setContent(content);
				infowindow.open(map,venue);
			});

			infowindow.setContent(content);
			infowindow.open(map,venue);

			return venue;
		}

	}
};

foodninja.init();
