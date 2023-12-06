function regresar() {
    window.history.back(); // Regresar a la página anterior
}

$(document).ready(function() {

    $('#PartesInventario').select2({
        dropdownParent: $('#nuevoInventarioModal'),
        placeholder: 'Selecciona una parte',
        allowClear: true,
        width: '100%'
    });

    

});

