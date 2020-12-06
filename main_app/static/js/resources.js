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
  const category = urlParams.get('category')
  passlist_categories = []
  title = 'All Resources'
  if (category == null) {
    return {title, passlist_categories};
  }

  var i = categories.indexOf(category.toUpperCase());
  if (i != -1) {
    passlist_categories = [categories[i]];
    title = 'Resources For ' + category_names[i]
    return {title, passlist_categories};
  }

  if (category === 'shelter_and_hygiene') {
    passlist_categories = ['HYGIENE', 'SHELTER'];
    title = 'Resources For Shelter And Hygiene';
  } else if (category === 'health') {
    passlist_categories = ['ADDICTION_RECOVERY', 'MENTAL_HEALTH_SERVICES', 'MEDICAL_ASSISTANCE'];
    title = 'Resources For Physical And Mental Health';
  }

  return {title, passlist_categories};
}
