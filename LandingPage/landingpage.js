
document.addEventListener("DOMContentLoaded", function () {
    // Initialize ScrollReveal
    const sr = ScrollReveal({
      distance: '50px',
      duration: 1000,
      easing: 'ease-in-out',
      opacity: 0,
    });
  
    // Function to reveal the content of the active slide
    function revealActiveSlide() {
      const activeSlide = document.querySelector('.carousel-item.active');
  
      // Reveal the image first
      sr.reveal(activeSlide.querySelector('img'), {
        origin: 'bottom',
        delay: 200,
        beforeReveal: function (el) {
          el.style.opacity = 1;
        }
      });
  
      // Then the text (carousel-caption)
      sr.reveal(activeSlide.querySelector('.carousel-caption h1'), {
        origin: 'left',
        delay: 400,
      });
  
      sr.reveal(activeSlide.querySelector('.carousel-caption p'), {
        origin: 'right',
        delay: 600,
      });
  
      // Finally, reveal the button
      sr.reveal(activeSlide.querySelector('.carousel-caption .btn'), {
        origin: 'bottom',
        delay: 800,
      });
    }
  
    // Reveal the first active slide when the page loads
    revealActiveSlide();
  
    // Listen for carousel slide events to trigger ScrollReveal for the next slide
    const myCarousel = document.getElementById('myCarousel');
    myCarousel.addEventListener('slide.bs.carousel', function () {
      revealActiveSlide();
    });
  });

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






  

  
