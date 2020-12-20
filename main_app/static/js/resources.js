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

function getTitleAndPasslistFromUrlParams() {
  const queryString = window.location.search;
  const urlParams = new URLSearchParams(queryString);

  passlist_categories = []
  title = 'All Resources'
  for_youth = false
  for_seniors = false

  const youth = urlParams.get('youth')
  if (youth != null) {
    title = 'Resources For Youth'
    for_youth = true
    return {title, passlist_categories, for_youth, for_seniors}
  }

  const seniors = urlParams.get('seniors')
  if (seniors != null) {
    title = 'Resources For Seniors'
    for_seniors = true
    return {title, passlist_categories, for_youth, for_seniors}
  }

  const category = urlParams.get('category')
  if (category == null) {
    return {title, passlist_categories, for_youth, for_seniors};
  }

  var i = categories.indexOf(category.toUpperCase());
  if (i != -1) {
    passlist_categories = [categories[i]];
    title = 'Resources For ' + category_names[i]
    return {title, passlist_categories, for_youth, for_seniors};
  }

  if (category === 'shelter_and_hygiene') {
    passlist_categories = ['HYGIENE', 'SHELTER'];
    title = 'Resources For Shelter And Hygiene';
  } else if (category === 'health') {
    passlist_categories = ['ADDICTION_RECOVERY', 'MENTAL_HEALTH_SERVICES', 'MEDICAL_ASSISTANCE'];
    title = 'Resources For Physical And Mental Health';
  }

  return {title, passlist_categories, for_youth, for_seniors};
}
