document.addEventListener('DOMContentLoaded', () => {

    const header = document.querySelector('.header');
    const body = document.querySelector('body');
    
    const handleHeaderScroll = () => {
        if (window.scrollY > 50) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    };
    window.addEventListener('scroll', handleHeaderScroll);
    handleHeaderScroll();

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });
    document.querySelectorAll('.animate-on-scroll').forEach(el => observer.observe(el));

    const elementsToAnimateOnLoad = document.querySelectorAll('.animate-on-load');
    setTimeout(() => {
        elementsToAnimateOnLoad.forEach(element => {
            element.classList.add('visible');
        });
    }, 200);

    const burger = document.querySelector('.burger-menu');
    const nav = document.querySelector('.nav');

    burger.addEventListener('click', () => {
        burger.classList.toggle('is-active');
        nav.classList.toggle('is-active');
        body.classList.toggle('no-scroll');
    });
});