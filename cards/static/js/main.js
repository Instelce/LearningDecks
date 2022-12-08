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
let mainContainer = document.querySelector('.main-container')

sidebar.style = `top: ${navbar.getBoundingClientRect().height}px;`;
sidebar.style = `padding-bottom: calc(${navbar.getBoundingClientRect().height}px + 2rem);`;
mainContainer.style = `padding-bottom: calc(${navbar.getBoundingClientRect().height}px + 2rem);`;
console.log(navbar.getBoundingClientRect().height + 'px');

// Trailer
const trailer = document.querySelector('.trailer');

const animateTrailer = (e, interacting) => {
    const x = e.clientX - trailer.offsetWidth / 2;
    const y = e.clientY - trailer.offsetHeight / 2;

    const keyframes = {
        transform: `translate(${x}px, ${y}px) scale(${interacting ? 4 : 1})`,
        opacity: `${interacting ? 0.2 : 1}`
    }

    trailer.animate(keyframes, {
        duration: 100,
        fill: "forwards"
    })
}

window.onmousemove = e => {
    const interactable = e.target.closest('.interactable'),
          interacting = interactable !== null;
    animateTrailer(e, interacting);
}

// Interactable elements
const interactableElements = document.querySelectorAll('.link, .button, .field-container')

interactableElements.forEach(element => {
    element.classList.add('interactable')
});

// Page transition
const aLinks = document.querySelectorAll('a')
const pageTransition = function(href) {
    document.querySelector('body').style.opacity = 0

    if (href != '#') {
        setTimeout(function() { 
            window.location.href = href
        }, 500)
    }
}

aLinks.forEach(a => {
    href = a.href
    if (href != '#') {
        a.addEventListener('click', e => {
            window.transitionToPage = pageTransition(href)
        })
    } 
});

document.addEventListener('DOMContentLoaded', function(event) {
    document.querySelector('body').style.opacity = 1
})