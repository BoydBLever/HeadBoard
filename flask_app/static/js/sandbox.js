// //1 https://developer.mozilla.org/en-US/docs/Web/API/Geolocation_API/Using_the_Geolocation_API
// if ('geolocation' in navigator) {
//     /* geolocation is available */
// } else {
//     /* geolocation IS NOT available */
// }
// //getCurrentPosition()
// navigator.geolocation.getCurrentPosition((position) => {
//     doSomething(position.coords.latitude, position.coords.longitude);
// });

// const options = {
//     enableHighAccuracy: true,
//     timeout: 5000,
//     maximumAge: 0
// };

// function success(pos) {
//     const crd = pos.coords;

//     console.log('Your current position is:');
//     console.log(`Latitude : ${crd.latitude}`);
//     console.log(`Longitude: ${crd.longitude}`);
//     console.log(`More or less ${crd.accuracy} meters.`);
// }

// function error(err) {
//     alert('Position unavailale.')
// }

// navigator.geolocation.getCurrentPosition(success, error, options);
function geoFindMe() {

    const status = document.querySelector('#status');
    const mapLink = document.querySelector('#map-link');

    mapLink.href = '';
    mapLink.textContent = '';

    function success(position) {
        const latitude = position.coords.latitude;
        const longitude = position.coords.longitude;

        status.textContent = '';
        mapLink.href = `https://www.openstreetmap.org/#map=18/${latitude}/${longitude}`;
        mapLink.textContent = `Latitude: ${latitude} °, Longitude: ${longitude} °`;
    }

    function error() {
        status.textContent = 'Unable to retrieve user location';
    }

    if (!navigator.geolocation) {
        status.textContent = 'Geolocation is not supported by your browser';
    } else {
        status.textContent = 'Locating…';
        navigator.geolocation.getCurrentPosition(success, error);
    }

}

document.querySelector('#find-me').addEventListener('click', geoFindMe);
//
//In the above geoFindMe example the Geolocation API is used to retrieve the user's latitude and longitude. 
//If successful, the available hyperlink is populated with an openstreetmap.org URL that will show their location.