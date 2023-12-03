function regresar() {
    window.history.back(); // Regresar a la página anterior
}

function obtenerTotalPiezas(partesId) {
    $.ajax({
        url: `/obtener_total_piezas/${partesId}/`,
        type: 'GET',
        success: function(data) {
            $('#id_piezas_salida').attr('max', data.total_piezas);
            $('#total_piezas_disponibles').text(`Disponibles: ${data.total_piezas}`);
        },
        error: function(jqXHR, textStatus, errorThrown) {
            console.log('Error al obtener total_piezas:');
            console.log(`Status: ${textStatus}`);
            console.log(`Error: ${errorThrown}`);
            console.log(jqXHR.responseText);  // Muestra la respuesta del servidor
        }
    });
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
    }).on('change', function() {
        var partesId = $(this).val();
        if (partesId) {
            obtenerTotalPiezas(partesId);
        }
    });

    $('#PartesInventario').select2({
        dropdownParent: $('#nuevoInventarioModal'),
        placeholder: 'Selecciona una parte',
        allowClear: true,
        width: '100%'
    });

    
});


