function updateWeeklyOpeningHoursEnable(id) {
    console.log('updateEnable: ')
    console.log(id)

    weekday = document.getElementById(id)

    i = id.slice(-1)
    prefix = 'id_opening_hours_' + i + '_'
    toggle = document.getElementById(prefix + '0')
    opening_hours = document.getElementById('opening_hours_times_' + i)
    opening_time = document.getElementById(prefix + '1')
    closing_time = document.getElementById(prefix + '2')

    idx = weekday.innerHTML.indexOf(' closed')

    if (idx === -1) {
        weekday.innerHTML = weekday.innerHTML + ' closed' 
        toggle.checked = false
        opening_hours.style.visibility = 'hidden'
        opening_time.style.visibility = 'hidden'
        closing_time.style.visibility = 'hidden'
    } else {
        weekday.innerHTML = weekday.innerHTML.substring(0, idx)
        toggle.checked = true
        opening_hours.style.visibility = 'visible'
        opening_time.style.visibility = 'visible'
        closing_time.style.visibility = 'visible'
    }
}
