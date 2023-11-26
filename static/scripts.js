function regresar() {
    window.history.back(); // Regresar a la página anterior
}

$(document).ready(function() {
    // Inicializa Select2
    $('#maquinaSelect').select2({
        dropdownParent: $('#nuevoMantenimientoModal'),
        placeholder: 'Selecciona una máquina',
        allowClear: true,
        width: '100%'
    });
    $('#partes').select2({
        dropdownParent: $('#nuevoMantenimientoModal'),
        placeholder: 'Selecciona una parte',
        allowClear: true,
        width: '100%'
    });
});