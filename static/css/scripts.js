function regresar() {
    window.history.back(); // Regresar a la página anterior
}

// Función para mostrar/ocultar la barra lateral en dispositivos móviles
function toggleSidebar() {
    const sidebar = document.querySelector('.sidebar');
    sidebar.classList.toggle('active');
}

// Función para mostrar/ocultar las opciones del menú de usuario
function toggleUserMenu() {
    const userOptionsMenu = document.querySelector('.user-options-menu');
    userOptionsMenu.classList.toggle('active');
}

// Evento para mostrar/ocultar la barra lateral al hacer clic en el botón de tres rayitas
document.getElementById('toggle-button').addEventListener('click', toggleSidebar);

// Evento para mostrar/ocultar las opciones del menú de usuario al hacer clic en el icono de usuario
document.getElementById('user-options').addEventListener('click', toggleUserMenu);




