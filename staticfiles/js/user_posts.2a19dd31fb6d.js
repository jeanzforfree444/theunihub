document.addEventListener("DOMContentLoaded", function () {
    new Swiper(".articles-swiper", {
        slidesPerView: 3,
        spaceBetween: 20,
        navigation: {
            nextEl: ".articles-next",
            prevEl: ".articles-prev",
        },
        breakpoints: {
            1024: { slidesPerView: 3 },
            768: { slidesPerView: 2 },
            480: { slidesPerView: 1 },
        },
        centeredSlides: false,
        grabCursor: true,
        loop: false,
    });

    new Swiper(".threads-swiper", {
        slidesPerView: 3,
        spaceBetween: 20,
        navigation: {
            nextEl: ".threads-next",
            prevEl: ".threads-prev",
        },
        breakpoints: {
            1024: { slidesPerView: 3 },
            768: { slidesPerView: 2 },
            480: { slidesPerView: 1 },
        },
        centeredSlides: false,
        grabCursor: true,
        loop: false,
    });
});