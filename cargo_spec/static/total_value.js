$(document).on("change", ".value", function() {
    var sum = 0;
    $(".value").each(function(){
        sum += +$(this).val();
    });
    $("#id_total_value").val(sum);
});