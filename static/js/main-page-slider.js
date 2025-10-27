document.addEventListener('DOMContentLoaded', () => {

    const swiper = new Swiper('.main-gallery-slider', {
        loop: true,
        
        autoplay: {
            delay: 2500,
            disableOnInteraction: false,
        },

        speed: 800,
        
        effect: 'coverflow',
        grabCursor: true,
        centeredSlides: true,
        slidesPerView: 'auto',
        coverflowEffect: {
            rotate: 50,
            stretch: 0,
            depth: 100,
            modifier: 1,
            slideShadows: true,
        },

        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev',
        },
    });

    // Fancybox.bind("[data-fancybox='main-gallery']", {
    // });

});