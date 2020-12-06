"use strict";

const sfLatLng = { lat: 37.7749, lng: -122.4194 };

const categories = [
  "Food",
  "Clothing",
  "Addiction Recovery",
  "Hygiene",
  "Financial Empowerment",
  "Shelter",
  "Women/Children",
  "Mental health services",
  "Financial Empowerment",
  "Medical Assistance",
];

const icons = [
  "icons/food.gif",
  "icons/clothing.gif",
  "icons/addiction_recovery.gif",
  "icons/hygiene.gif",
  "icons/financial_empowerment.gif",
  "icons/shelter.gif",
  "icons/women_and_children.gif",
  "icons/mental_health.gif",
  "icons/financial_empowerment.gif",
  "icons/medical_assistance.gif",
];

function initMap() {
  var map = new google.maps.Map(document.getElementById("map"), {
    center: sfLatLng,
    zoom: 13,
  });

  var tableRef = document.getElementById("resources");

  for (var i = 0; i < resources.length; i++) {
    var resource = resources[i];
    var resourceLatLng = { lat: resource.lat, lng: resource.long };
    var category_index = categories.indexOf(resource.category);
    var category =
      category_index == -1 ? "------" : `--- ${resource.category} ---`;

    var contentString = `<div class='resource_category'>${category}</div>
        <div class='resource_name'>${resource.resource}</div>
        <div class='resource_org_name'>offered by ${resource.org_name}</div>
        <div class='resource_street'>${resource.address}</div>
        <div class='resource_street'>${resource.hrs}</div>
        <div class='resource_street'>${resource.phone}</div>
        <div class='resource_notes'>${resource.notes}</div>
        <div class='resource_notes'><a href='${resource.link}'>${resource.link}</div>`;

    var infoWindow = new google.maps.InfoWindow({
      content: contentString,
    });

    var marker = new google.maps.Marker({
      position: resourceLatLng,
      map: map,
      icon: category_index == -1 ? "icons/default.gif" : icons[category_index],
      title: resource.resource_name,
    });

    google.maps.event.addListener(
      marker,
      "click",
      (function (marker, contentString, infowWindow) {
        return function () {
          infowWindow.setContent(contentString);
          infowWindow.open(map, marker);
        };
      })(marker, contentString, infoWindow)
    );

    // Insert a row in the table at the last row
    var newRow = tableRef.insertRow();
    var newCell = newRow.insertCell(0);
    newCell.innerHTML = contentString;
  }
}
