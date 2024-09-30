
//Handling of scroll animations
const  scrollRevealOption = {
    distance: "50px",
    origin: "bottom",
    duration: 1000,
};
    ScrollReveal().reveal(".content h1", {
...scrollRevealOption,

});
ScrollReveal().reveal(".content p", {
 ...scrollRevealOption,
 delay: 500,
});
ScrollReveal().reveal(".content .btn", {
 ...scrollRevealOption,
 delay: 800,
});
ScrollReveal().reveal(".image__bg", {
    ...scrollRevealOption,
    delay: 1000, 
    scale: 0.5,  
    opacity: 0,  
});
ScrollReveal().reveal(".image img", {
...scrollRevealOption,
delay: 1500,
});
ScrollReveal().reveal(".image .image__content__1 ", {
...scrollRevealOption,
delay: 2000,
});
ScrollReveal().reveal(".image .image__content__2 ", {
...scrollRevealOption,
delay: 2500,
});
ScrollReveal.reveal(".about .content .image", {
...scrollRevealOption,
delay: 1000
});
ScrollReveal.reveal(".about .content h2", {
...scrollRevealOption,
delay: 2000
});
ScrollReveal.reveal(".about .content p", {
...scrollRevealOption,
delay:2000
});
ScrollReveal.reveal(".about .content .btn", {
...scrollRevealOption,
delay: 2500
});

