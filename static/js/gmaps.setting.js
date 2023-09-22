let map;

async function initMap() {
  // The location of Uluru
  const position = { lat: 41.6971593, lng: 44.8128641 };
  // Request needed libraries.
  //@ts-ignore
  const { Map } = await google.maps.importLibrary("maps");
  const { AdvancedMarkerView } = await google.maps.importLibrary("marker");

  // The map, centered at Uluru
  map = new Map(document.getElementById("map"), {
    zoom: 14,
    center: position,
    mapId: "DEMO_MAP_ID",
  });

  // The marker, positioned at Uluru
  new google.maps.Marker({
    position: position,
    map,
    title: "Clinic",
  });


}

initMap();
