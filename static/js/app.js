var total_value = function() {
        var sum = 0;
        $('.value').not($('tr:hidden').find('.value')).each(function(){
            sum += +$(this).val();
        });
        $("#id_total_value").val(sum);
    };

$(document).on('change', '.value', total_value);
$(document).on('click', '#save_spec', total_value);
$(document).on('click', '#accept_spec', total_value);

// FIXME: nie działa wywołanie funkcji w przypadku kliknięcia 'usuń'
// $('a.delete-row').live('click', total_value);
// $(document).on('click', 'a.delete-row', total_value);


// NOTE: Ukrywa przycisk "Usuń" z pierwszego rzędu
$(window).on('load', function () {
    $("#div_id_cargos_content-0-DELETE").parent().parent().hide();
});