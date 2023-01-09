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
// mainContainer.style = `padding-bottom: calc(${navbar.getBoundingClientRect().height}px + 2rem);`;
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
// const aLinks = document.querySelectorAll('a')
// const pageTransition = function(href) {
//     document.querySelector('body').style.opacity = 0

//     if (href != '#') {
//         setTimeout(function() { 
//             window.location.href = href
//         }, 500)
//     }
// }

// aLinks.forEach(a => {
//     href = a.href
//     if (href != '#') {
//         a.addEventListener('click', e => {
//             window.transitionToPage = pageTransition(href)
//         })
//     } 
// });

document.addEventListener('DOMContentLoaded', function(event) {
    document.querySelector('body').style.opacity = 1
})

// Reply form
const replyButtons = document.querySelectorAll('.reply-button')
const replyFormContainer = document.querySelectorAll('.reply-form-container')
console.log(replyButtons);
replyButtons.forEach(button => {
    let questionId = button.classList[1]
    let replyFromContainer = document.
    console.log(button.classList[1]);
    button.addEventListener('click', (e) => {
        e.preventDefault()
    })
});

// Dropdown
const dropdowns = document.querySelectorAll('.dropdown')

dropdowns.forEach(dropdown => {
    const toggle = dropdown.querySelector('.toggle')
    const indication = dropdown.querySelector('.indication')
    const content = dropdown.querySelector('.content')

    toggle.classList.add('interactable')

    toggle.addEventListener('click', (e) => {
        e.preventDefault()
        if (indication.innerHTML == 'View') {
            indication.innerHTML = 'Hide'
        } else {
            indication.innerHTML = 'View'
        }

        if (content.clientHeight) {
            content.style.height = 0;
        } else {
            var wrapper = content.querySelector('.wrapper');
            content.style.height = wrapper.clientHeight + "px";
        }

        content.classList.toggle('visible');
    })
});

// Flip card
const flipCards = document.querySelectorAll('.flip-card')

flipCards.forEach(card => {
    const inner = card.querySelector('.inner')
    card.addEventListener('click', (e) => {
        inner.classList.toggle('rotate');
    })
});

// HTMX
document.body.addEventListener('htmx:configRequest', (event) => {
    event.detail.headers['X-CSRFToken'] = '{{ csrf_token }}';
})