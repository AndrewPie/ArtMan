var total_value = function() {
        var sum = 0;
        $(".value").each(function(){
            sum += +$(this).val();
        });
        $("#id_total_value").val(sum);
    };

$(document).on('change', total_value);
$(document).on('click', '#save_spec', total_value);

// TODO: nie działa wywołanie funkcji w przypadku kliknięcia 'usuń'
// $(document).on('click', '.delete-row', total_value);