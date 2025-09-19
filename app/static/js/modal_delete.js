document.addEventListener("DOMContentLoaded", function () {
    const deleteModal = document.getElementById("confirmDeleteModal");
    const modalBody = document.getElementById("confirmDeleteBody");
    const modalLink = document.getElementById("confirmDeleteLink");

    deleteModal.addEventListener("show.bs.modal", function (event) {
        // Botón que disparó el modal
        const button = event.relatedTarget;

        // Obtener atributos data-*
        const message = button.getAttribute("data-message");
        const url = button.getAttribute("data-url");

        // Insertar valores en el modal
        modalBody.innerHTML = message;
        modalLink.setAttribute("href", url);
    });
});