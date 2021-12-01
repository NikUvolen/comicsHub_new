document.addEventListener('DOMContentLoaded', () => {
    const deleteButton = document.querySelector("#delete");
    const deletePanel = document.querySelector("#delete_panel");
    const closeButton = document.querySelector("#close_button");

    deleteButton.addEventListener('click', () => {
        deletePanel.style.display = 'block';
    })

    closeButton.addEventListener('click', () => {
        deletePanel.style.display = 'none';
    })
})