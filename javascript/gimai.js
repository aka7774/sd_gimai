
function show_voice(button, path, title, name, vtext) {
    textarea = gradioApp().querySelector('#gimai_title textarea')
    textarea.value = path + ',' + title + ',' + name + ',' + vtext
	textarea.dispatchEvent(new Event("input", { bubbles: true }))
    gradioApp().querySelector('#gimai_voice_button').click()
}

function show_image(button, path) {
    textarea = gradioApp().querySelector('#gimai_title textarea')
    textarea.value = path
	textarea.dispatchEvent(new Event("input", { bubbles: true }))
    gradioApp().querySelector('#gimai_image_button').click()
}
