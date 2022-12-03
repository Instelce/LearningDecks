let inputs = document.querySelectorAll('input')
let textareas = document.querySelectorAll('textarea')

inputs.forEach(input => {
    input.placeholder = " "
});

textareas.forEach(textarea => {
    textarea.placeholder = " "
});

let navbar = document.querySelector('.navbar')
let sidebar = document.querySelector('.sidebar')

// sidebar = navbar.offsetHeight