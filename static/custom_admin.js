(function($){
    $(document).ready(function(){
        function toggleFieldsBasedOnTipoUsuario(){
            var tipoUsuarioValue = $('#id_tipo_usuario').val();
            var isStaffField = $('#id_is_staff');
            var isActiveField = $('#id_is_active');
            var isSuperuserField = $('#id_is_superuser');

            // Desactiva is_staff e is_active por defecto
            isStaffField.prop('checked', false);
            isStaffField.prop('disabled', true);
            isActiveField.prop('checked', false);
            isActiveField.prop('disabled', true);

            // Activa is_staff e is_active si el tipo_usuario es 'superusuario'
            if (tipoUsuarioValue === 'superusuario') {
                isStaffField.prop('checked', true);
                isStaffField.prop('disabled', false);
                isActiveField.prop('checked', true);
                isActiveField.prop('disabled', false);
            }

            // Activa is_staff e is_active si el tipo_usuario es 'tecnico'
            if (tipoUsuarioValue === 'tecnico') {
                isStaffField.prop('checked', true);
                isStaffField.prop('disabled', false);
                isActiveField.prop('checked', true);
                isActiveField.prop('disabled', false);
            }
        }

        // Llamada inicial al cargar la página
        toggleFieldsBasedOnTipoUsuario();

        // Configuración de evento para cambiar los campos cuando cambie el tipo_usuario
        $('#id_tipo_usuario').change(function(){
            toggleFieldsBasedOnTipoUsuario();
        });
    });
})(django.jQuery);
