function flashMessage(message, alertClass = "alert-info") {
    const container = document.getElementById("flash-messages")

    const div = document.createElement("div")
    div.className = `alert ${alertClass} fade show`
    div.setAttribute("role", "alert")
    div.textContent = message

    container.appendChild(div)

    // eliminar automáticamente después de 3s
    setTimeout(() => {
        div.classList.remove("show")
        setTimeout(() => div.remove(), 150)
    }, 3000)
}