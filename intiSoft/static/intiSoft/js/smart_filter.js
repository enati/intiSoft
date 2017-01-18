function smart_filter() {
    var area = $("#id_ejecutor").val(),
        url = "OT_" + area;
    $.getJSON(url, function(ofertatec) {
        var options = '<option value="">---------</option>';
        for (var i = 0; i < ofertatec.length; i++) {
            options += '<option value="' + ofertatec[i].pk + '">' + ofertatec[i].fields['codigo'] + ' - ' + ofertatec[i].fields['subrubro'] + ' - ' + ofertatec[i].fields['detalle'] + '</option>';
        }
        $("select[id$=ofertatec]").each(function() {
            var last_selection = $(this).val();
            $(this).html(options);
            $(this).val(parseInt(last_selection));
        });
    });
};

$(document).ready(function() {

    if ($("select#id_ejecutor") !== "") {
        smart_filter();
    };

    // Filtro para la oferta tecnologica segun UT Ejecutora (en SI)
    $("select#id_ejecutor").change(function() {
        smart_filter();
    });
});