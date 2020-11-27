"use strict";

const tenderloinLatLng = { lat:37.7847, lng:-122.4145 };

const categories = [
  "FOOD",
  "CLOTHING",
  "ADDICTION_RECOVERY",
  "HYGIENE",
  "FINANCIAL_EMPOWERMENT",
  "SHELTER",
  "WOMEN_AND_CHILDREN",
  "MENTAL_HEALTH_SERVICES",
  "MEDICAL_ASSISTANCE"
];

const category_names = [
  "Food",
  "Clothing",
  "Addiction Recovery",
  "Hygiene",
  "Financial Empowerment",
  "Shelter",
  "Women and Children",
  "Mental Health Services",
  "Medical Assistance"
];

const card_prefix_html = `
<div class="card col shadow p-3 m-2 bg-white"
     id="card">
     <div class="card-content">`

const card_suffix_html = `</div></div>`

function initMap() {
  var map = new google.maps.Map(document.getElementById("map"), {
    center: tenderloinLatLng,
    zoom: 16,
  });

  var tables_by_category = {};

  for (var i = 0; i < resources_from_database.length; i++) {
    var resource = resources_from_database[i];
    var resourceLatLng = { lat: parseFloat(resource.lat), lng: parseFloat(resource.long) };
    var category_index = categories.indexOf(resource.category);
    var category =
      category_index == -1 ? "Unknown Category" : category_names[category_index];

    var contentString = `
        <div class='resource_name'>${resource.resource_name}</div>
        <div class='resource_street'>offered by <div class="bold" style="display:inline;">${resource.org_name}</div></div>
        <br>
        <div class='resource_street'>${resource.hrs}</div>
        <div class='resource_street'>${resource.address}</div>
        <div class='resource_street'>${resource.phone}</div>
        <div class='resource_notes'>${resource.notes}</div>
        <div class='resource_notes'><a href='${resource.link}'>${resource.link}</a></div>`;

    var infoWindow = new google.maps.InfoWindow({
      content: contentString,
    });

    var marker = new google.maps.Marker({
      position: resourceLatLng,
      map: map,
      icon: category_index == -1 ? default_icon : icons[category_index],
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

    if (!(category in tables_by_category)) {
      tables_by_category[category] = '';
    }
    tables_by_category[category] = tables_by_category[category] + card_prefix_html + contentString + card_suffix_html;
  }

  var tableRef = document.getElementById("resource_listings");
  for (category in tables_by_category) {
    var div = document.createElement('div');
    div.style.width = '100%';
    div.className = "row m-4";
    
    var title_div = document.createElement('div');
    title_div.style = 'width:100%';
    title_div.style['font-size'] = 'x-large';
    title_div.style.color = '#00AECB';
    title_div.className = 'row m-1';
    title_div.innerHTML = category;

    var listings_div = document.createElement('div')
    listings_div.className = 'row m-2';
    listings_div.innerHTML = tables_by_category[category]

    div.appendChild(title_div);
    div.appendChild(listings_div);
    tableRef.appendChild(div);
  }

}
