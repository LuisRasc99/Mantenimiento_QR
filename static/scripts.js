function regresar() {
    window.history.back(); // Regresar a la página anterior
}

$(document).ready(function() {
    // Inicializa Select2
    $('#SelectMaquinaMantenimiento').select2({
        dropdownParent: $('#nuevoMantenimientoModal'),
        placeholder: 'Selecciona una máquina',
        allowClear: true,
        width: '100%'
    });

    
    $('#PartesMantenimiento').select2({
        dropdownParent: $('#nuevoMantenimientoModal'),
        placeholder: 'Selecciona una parte',
        allowClear: true,
        width: '100%'
    });

    $('#PartesInventario').select2({
        dropdownParent: $('#nuevoInventarioModal'),
        placeholder: 'Selecciona una parte',
        allowClear: true,
        width: '100%'
    });
});


