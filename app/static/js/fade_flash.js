document.addEventListener("DOMContentLoaded", () => {
    setTimeout(() => {
        document.querySelectorAll('.alert.server-flash').forEach(el => {
            el.classList.remove('show'); // dispara animación fade-out
            // esperar la transición de Bootstrap y luego remover del DOM
            el.addEventListener('transitionend', () => el.remove());
        });
    }, 3000);
});