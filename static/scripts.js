function regresar() {
    window.history.back(); // Regresar a la página anterior
}

$(document).ready(function() {

    $('#PartesInventario_Entrada').select2({
        dropdownParent: $('#nuevoEntradaModal'),
        placeholder: 'Selecciona una parte',
        allowClear: true,
        width: '100%'
    });

    $('#PartesMantenimiento').select2({
        dropdownParent: $('#nuevoMantenimientoModal'),
        placeholder: 'Selecciona una parte',
        allowClear: true,
        width: '100%'
    });

    $('#maquinas').select2({
        dropdownParent: $('#nuevoMantenimientoModal'),
        placeholder: 'Selecciona una maquina',
        allowClear: true,
        width: '100%'
    });

    

});

