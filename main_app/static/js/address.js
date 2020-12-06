"use strict";

let placeSearch;
let autocomplete;

function initAutocomplete() {
  // Create the autocomplete object, restricting the search predictions to
  // geographical location types.
  autocomplete = new google.maps.places.Autocomplete(
    document.getElementById("id_address"),
    {
      types: ["geocode"]
    });
  // Avoid paying for data that you don't need by restricting the set of
  // place fields that are returned to just the address components.
  autocomplete.setFields(["geometry", "address_component"]);
  autocomplete.addListener("place_changed", fillInAddress);
}

const componentForm = {
  street_number: "short_name",
  route: "long_name",
  locality: "long_name",
  administrative_area_level_1: "short_name",
  country: "long_name",
  postal_code: "short_name"
};

const addressForm = {
  street_number: "id_street_number",
  route: "id_street_name",
  locality: "id_city",
  administrative_area_level_1: "id_state",
  country: "id_country",
  postal_code: "id_postal_code"
};

function fillInAddress() {
  const place = autocomplete.getPlace();
  document.getElementById('id_lat').value = place.geometry.location.lat();
  document.getElementById('id_long').value = place.geometry.location.lng();
  for (const component of place.address_components) {
    const addressType = component.types[0];

    if (componentForm[addressType]) {
      const val = component[componentForm[addressType]];
      document.getElementById(addressForm[addressType]).value = val;
    }
  }
}
