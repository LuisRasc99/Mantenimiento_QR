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

    $('#PartesMantenimiento').on('change', function() {
        var parteSeleccionada = $(this).val();
        if (parteSeleccionada) {
            var obtenerInventarioUrl = $(this).data('obtener-inventario-url').replace('0', parteSeleccionada);

            $.ajax({
                url: obtenerInventarioUrl,
                type: 'GET',
                success: function(data) {
                    $('#inventario_disponible').val(data.total_piezas);
                },
                error: function() {
                    console.error('Error al obtener el inventario disponible');
                }
            });
        } else {
            $('#inventario_disponible').val('');
        }
    });

    $('#PartesMantenimiento').on('change', function() {
        var parteSeleccionada = $(this).val();
        
        if (parteSeleccionada) {
            var obtenerInventarioUrl = $(this).data('obtener-inventario-url');
    
            // Verificar si la URL está presente
            if (!obtenerInventarioUrl) {
                console.error('Error: La URL para obtener el inventario no está definida.');
                return;
            }
    
            // Reemplazar el marcador de posición en la URL
            obtenerInventarioUrl = obtenerInventarioUrl.replace('0', parteSeleccionada);
    
            $.ajax({
                url: obtenerInventarioUrl,
                type: 'GET',
                success: function(data) {
                    $('#inventario_disponible').val(data.total_piezas);
                },
                error: function() {
                    console.error('Error al obtener el inventario disponible');
                }
            });
        } else {
            $('#inventario_disponible').val('');
        }
    });
    
    

});

