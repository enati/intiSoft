var close = true;
var trlink = true;
var domain = '';

if (window.location.href.toLocaleString().indexOf('intiSoft') != -1)
    domain = '/intiSoft';
else
    domain = '';

function seleccionar_todo(f_name){
   for (i=0;i<f_name.elements.length;i++)
      if(f_name.elements[i].type == "checkbox")
         f_name.elements[i].checked=1
   close = false;
}

function deseleccionar_todo(f_name){
   for (i=0;i<f_name.elements.length;i++)
      if(f_name.elements[i].type == "checkbox")
         f_name.elements[i].checked=0
   close = false;
}

function revisionarTurno() {
    $.ajax({
        url: 'revision/',
        method: 'post',
        data: {},
        success: function(data){
                    if (data.ok) {
                        location.href = '?edit=1&revision=1';
                    }
                    else if (data.err) {
                        alert("ERROR!");
                        location.reload();
                    }
                },
        error  : function( json ) {
                    alert("ERROR!");
                    location.reload();
            }
     });
}

function rollBackTurno() {
    $.ajax({
        url: 'rollback/',
        method: 'post',
        data: {},
        success: function(data){
                    if (data.ok) {
                        location.href = data.redirect;
                    }
                    else if (data.err) {
                        alert("ERROR!");
                        location.href = data.redirect;
                    }
                },
        error  : function( json ) {
                    alert("ERROR!");
                    location.reload();
            }
     });
}

function revisionarPresupuesto() {
    $.ajax({
        url: 'revision/',
        method: 'post',
        data: {},
        success: function(data){
                    if (data.ok) {
                        location.href = '?edit=1&revision=1';
                    }
                    else if (data.err) {
                        alert("ERROR!");
                        location.reload();
                    }
                },
        error  : function( json ) {
                    alert("ERROR!");
                    location.reload();
            }
     });
}

function rollBackPresupuesto() {
    $.ajax({
        url: 'rollback/',
        method: 'post',
        data: {},
        success: function(data){
                    if (data.ok) {
                        location.href = data.redirect;
                    }
                    else if (data.err) {
                        alert("ERROR!");
                        location.href = data.redirect;
                    }
                },
        error  : function( json ) {
                    alert("ERROR!");
                    location.reload();
            }
     });
}

$.fn.wrapInTag = function(opts) {

  var tag = opts.tag || 'strong'
    , words = opts.words || []
    , regex = RegExp(words.join('|'), 'gi') // case insensitive
    , replacement = '<'+ tag +'>$&</'+ tag +'>';
  return this.html(function() {
      if (words != "") {
        return $(this).text().replace(regex, replacement);
      }
  });
};

//function cancelarFactura(event) {
//    btn = $(event.target);
//    form_prefix = btn.data('f_prefix') + '-' + btn.data('f_id');
//    alert(form_prefix);
//    field_estado = $('#id_' + form_prefix + '-estado');
//    field_estado.val('cancelada');

//    fields = $("input[id^=id_" + form_prefix + "], select[id^=id_" + form_prefix + "]")
//                    .not("[id$=-id]\
//                         ,[id$=-estado]\
//                         ,[id$=-MIN_NUM_FORMS]\
//                         ,[id$=-MAX_NUM_FORMS]\
//                         ,[id$=-INITIAL_FORMS]\
//                         ,[id$=-TOTAL_FORMS]\
//                         ,[id$=-DELETE]");
    //btn.prop("disabled", true);
//    for (i=0; i<fields.length; i++) {
//        $(fields[i]).prop("readonly", true);

//    }
//}

$(document).ready(function() {

    $('#calendarBtn').daterangepicker();

    var url = decodeURIComponent(window.location),
        matches = url.match(/[\?|\&]search=([^\&]+)/),
        getParams = matches ? matches[1].split(",") : [],
        getParamsDate = [];
    for (var i = 0; i < getParams.length; i++) {
        $('#searchField').tagsinput('add', getParams[i]);
        // Si es la fecha con formato dd/mm/yyyy-dd/mm/yyyy la separo en 2 palabras para la negrita
        //match = getParams[i].match(/\d{2}\/\d{2}\/\d{4}-\d{2}\/\d{2}\/\d{4}/);
        //getParamsDate = match ? match[0].split("-") : [];
        //if (getParamsDate.length > 0) {
            //getParams.splice(i, 1);
        //}
    }
    $('#otTable tbody td:not(:first):not(:has(button)),\
       #presupuestoTable tbody td:not(:first):not(:has(button)),\
       #rutTable tbody td:not(:first):not(:has(button)),\
       #sotTable tbody td:not(:first):not(:has(button)),\
       #siTable tbody td:not(:first):not(:has(button)),\
       #ofertatecTable tbody td:not(:has(button)),\
       #usuarioTable tbody td:not(:has(button)),\
       #pdtTable tbody td:not(:has(button)),\
       #turnoTable tbody td:not(:has(button))').wrapInTag({words: getParams});

    // Reseteo las fechas cuando hago una nueva revision
    if (window.location.href.indexOf('revision') != -1) {
        $('#id_fecha_realizado').val('');
        $('#id_fecha_aceptado').val('');
    };
    //$(".chosen-select").chosen();
    $.datepicker._gotoToday = function(id) {
        var target = $(id);
        var inst = this._getInst(target[0]);
        if (this._get(inst, 'gotoCurrent') && inst.currentDay) {
                inst.selectedDay = inst.currentDay;
                inst.drawMonth = inst.selectedMonth = inst.currentMonth;
                inst.drawYear = inst.selectedYear = inst.currentYear;
        }
        else {
                var date = new Date();
                inst.selectedDay = date.getDate();
                inst.drawMonth = inst.selectedMonth = date.getMonth();
                inst.drawYear = inst.selectedYear = date.getFullYear();
                // the below two lines are new
                this._setDateDatepicker(target, date);
                this._selectDate(id, this._getDateDatepicker(target));
        }
        this._notifyChange(inst);
        this._adjustDate(target);
    };

    $.datepicker.regional['es'] = {
        closeText: 'Borrar',
        prevText: '<Ant',
        nextText: 'Sig>',
        currentText: 'Hoy',
        monthNames: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'],
        monthNamesShort: ['Ene','Feb','Mar','Abr', 'May','Jun','Jul','Ago','Sep', 'Oct','Nov','Dic'],
        dayNames: ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado'],
        dayNamesShort: ['Dom','Lun','Mar','Mié','Juv','Vie','Sáb'],
        dayNamesMin: ['Do','Lu','Ma','Mi','Ju','Vi','Sá'],
        weekHeader: 'Sm',
        dateFormat: 'dd/mm/yy',
        firstDay: 1,
        isRTL: false,
        showMonthAfterYear: false,
        yearSuffix: ''
    };

    $.datepicker.setDefaults($.datepicker.regional['es']);

     $(".datepicker").datepicker({ showButtonPanel:true,
                                   beforeShow: function( input ) {
                                       setTimeout(function() {
                                	              var clearButton = $(input )
                                	              .datepicker( "widget" )
                            		              .find( ".ui-datepicker-close" );
                            	                       clearButton.unbind("click").bind("click",function() {
            	                                                            $.datepicker._clearDate( input );});
                            		          }, 1 );
                	               },
                                 });

    $('#smbButton').click(function(event) {
        var button = $(event.relatedTarget)
        if (button.data('name') == 'Actualizar') {
            $('#ofertatec_table').load(' #ofertatec_table');
            $('#title').load(' #title');
            $('#total').load(' #total')
        }
    });


    $("#ofertatec_formtable_turno select").on('change keyup', function (e) {
        var ot_id = $(this).val()
        if ( ot_id != "" ) {
            var select = $(this).get(0);
            splitted_id = select.id.split("-");
            splitted_id[splitted_id.length-1] = 'codigo';
            codigo_id = '#'.concat(splitted_id.join("-"));
            codigo = $(codigo_id);
            splitted_id[splitted_id.length-1] = 'precio';
            precio_id = '#'.concat(splitted_id.join("-"));
            precio = $(precio_id);
            splitted_id[splitted_id.length-1] = 'detalle';
            detalle_id = '#'.concat(splitted_id.join("-"));
            detalle = $(detalle_id);
            splitted_id[splitted_id.length-1] = 'tipo_servicio';
            tipo_servicio_id = '#'.concat(splitted_id.join("-"));
            tipo_servicio = $(tipo_servicio_id);
            splitted_id[splitted_id.length-1] = 'precio_total';
            precio_total_id = '#'.concat(splitted_id.join("-"));
            precio_total= $(precio_total_id);
            $.ajax({
                url: domain + '/lab/turnos/get_price/',
                method: 'get',
                data: {'ot_id': ot_id},
                success: function(data){
                    codigo.val(data['codigo']);
                    precio.val(data['precio']);
                    detalle.val(data['detalle']);
                    tipo_servicio.val(data['tipo_servicio']);
                    precio_total.val(data['precio_total']);
                    //$('#ofertatecform_table').load('#ofertatecform_table');
                }
             });
        }
    });

    $("#ofertatec_formtable select").on('change keyup', function (e) {
        var ot_id = $(this).val()
        if ( ot_id != "" ) {
            var select = $(this).get(0);
            splitted_id = select.id.split("-");
            splitted_id[splitted_id.length-1] = 'codigo';
            codigo_id = '#'.concat(splitted_id.join("-"));
            codigo = $(codigo_id);
            splitted_id[splitted_id.length-1] = 'cantidad';
            cantidad_id = '#'.concat(splitted_id.join("-"));
            cantidad = $(cantidad_id);
            splitted_id[splitted_id.length-1] = 'precio';
            precio_id = '#'.concat(splitted_id.join("-"));
            precio = $(precio_id);
            splitted_id[splitted_id.length-1] = 'detalle';
            detalle_id = '#'.concat(splitted_id.join("-"));
            detalle = $(detalle_id);
            splitted_id[splitted_id.length-1] = 'tipo_servicio';
            tipo_servicio_id = '#'.concat(splitted_id.join("-"));
            tipo_servicio = $(tipo_servicio_id);
            splitted_id[splitted_id.length-1] = 'precio_total';
            precio_total_id = '#'.concat(splitted_id.join("-"));
            precio_total= $(precio_total_id);
            $.ajax({
                url: domain + '/lab/turnos/get_price/',
                method: 'get',
                data: {'ot_id': ot_id},
                success: function(data){
                    codigo.val(data['codigo']);
                    cantidad.val(1);
                    cantidad.trigger("input");// Para actualizar el importe bruto/neto
                    precio.val(data['precio']);
                    precio.trigger("input"); // Para actualizar el importe bruto/neto
                    detalle.val(data['detalle']);
                    tipo_servicio.val(data['tipo_servicio']);
                    precio_total.val(data['precio_total']);
                    //$('#ofertatecform_table').load('#ofertatecform_table');
                }
             });
        }
    });

    $("#id_presupuesto").on('change keyup', function (e) {
        var presup_id = $(this).val()
        if (presup_id != "") {
            $.ajax({
                url: domain + '/lab/turnos/get_presup/',
                method: 'get',
                data: {'presup_id': presup_id},
                success: function(data){
                    $('#id_pdt option:contains(' + data['pdt'] + ')').prop('selected', true);
                    $("#id_fecha_solicitado").text(data['fecha_solicitado']);
                    $("#id_fecha_realizado").text(data['fecha_realizado']);
                    $("#id_fecha_aceptado").text(data['fecha_aceptado']);
                    $("#id_fecha_instrumento").text(data['fecha_instrumento']);
                    $("#id_usuario").text(data['usuario']);
                    $("#id_mail").text(data['mail']);
                    $("#id_rubro").text(data['rubro']);
                    $("#id_presupuesto__nro_presea").text(data['nro_presea']);
                    $("#id_presupuesto__area").text(data['area']);
                    $("select#id_solicitante").val(data['solicitante']);
                    $("#id_fecha_prevista").val(data['fecha_turno']);
                    $("#id_presupuesto__usuario__nombre").text(data['usuario']);
                    $('#id_deudor option:contains(' + data['usuario'] + ')').prop('selected', true);
                    $('select#id_centro_costos').val(data['centro_costos']);
                    $('select#id_area_tematica').val(data['area_tematica']);
                    $('select#id_horizonte').val(data['horizonte']);

                    // Borro todas las lineas de oferta tecnologica actuales
                    $('#ofertatec_formtable a.delete-row').click()
                    $('#ofertatec_formtable').trigger('row-deleted');
                    if (data['ofertatec'].length > 0) {
                        // Traigo las lineas de oferta tecnologica del presupuesto
                        for (i=0; i<data['ofertatec'].length; i++) {
                            $('#ofertatec_formtable .add-row').click();
                            $('#ofertatec_formtable tr:last>td>select').val(data['ofertatec'][i].ofertatec);
                            $('#ofertatec_formtable tr:last>td>input[id$=\'ofertatec_old\']').val(data['ofertatec'][i].ofertatec_old);
                            $('#ofertatec_formtable tr:last>td>input[id$=\'ofertatec_old_helper\']').val(data['ofertatec'][i].ofertatec_old_helper);
                            $('#ofertatec_formtable tr:last>td>input[id$=\'codigo\']').val(data['ofertatec'][i].codigo);
                            $('#ofertatec_formtable tr:last>td>input[id$=\'detalle\']').val(data['ofertatec'][i].detalle);
                            $('#ofertatec_formtable tr:last>td>input[id$=\'tipo_servicio\']').val(data['ofertatec'][i].tipo_servicio);
                            $('#ofertatec_formtable tr:last>td>input[id$=\'cantidad\']').val(data['ofertatec'][i].cantidad);
                            $('#ofertatec_formtable tr:last>td>input[id$=\'cant_horas\']').val(data['ofertatec'][i].cant_horas);
                            $('#ofertatec_formtable tr:last>td>input[id$=\'precio\']').val(data['ofertatec'][i].precio);
                            $('#ofertatec_formtable tr:last>td>input[id$=\'precio_total\']').val(data['ofertatec'][i].precio_total);
                            $('#ofertatec_formtable tr:last>td>textarea').val(data['ofertatec'][i].observaciones);
                            $('#ofertatec_formtable').trigger('row-added');
                        }
                    };
                },
            });
        }
    });

    $("#id_si").on('change keyup', function (e) {
        var si_id = $(this).val()
        if (si_id != "") {
            $.ajax({
                url: domain + '/lab/turnos/get_si/',
                method: 'get',
                data: {'si_id': si_id},
                success: function(data){
                    $("#id_si__solicitante").text(data['solicitante']);
                    $("#id_si__fecha_realizado").text(data['fecha_realizado']);
                    $("#id_si__fecha_prevista").text(data['fecha_prevista']);
                },
            });
        }
    });

    $("#id_usuario").on('change keyup', function (e) {
        var user_id = $(this).val()
        if (user_id != "") {
            $.ajax({
                url: domain + '/adm/presup/get_user/',
                method: 'get',
                data: {'user_id': user_id},
                success: function(data){
                    $("#id_nro_usuario").text(data['nro_usuario']);
                    $("#id_cuit").text(data['cuit']);
                    $("#id_rubro").text(data['rubro']);
                    $("#id_mail").text(data['mail']);
                },
            });
        }
    });

    function recalculateTotal() {
        //Recalculo el importe neto y el bruto
        var otLinePrice_list = $("[id^=id_adm-ot][id$=precio_total]"),
            total = 0,
            importe_bruto = $("[id$=id_importe_bruto]"),
            importe_neto = $("[id$=id_importe_neto]"),
            descuento_val = parseFloat($("[id$=id_descuento]").val());

        for (var i=0; i<otLinePrice_list.length; i++) {
            if (otLinePrice_list[i].closest('tr').style.display != 'none') {
                var line_total = parseFloat(otLinePrice_list[i].value);
                if (!isNaN(line_total))
                    total += line_total;
            }
        }
        importe_bruto.val(total);
        if (!isNaN(descuento_val))
            importe_neto.val(total - descuento_val);
        else
            importe_neto.val(total);
    }

    $("#ofertatec_formtable").on('row-deleted', function(e) {
        recalculateTotal();
    });

    $("#ofertatec_formtable").on('row-added', function(e) {
        recalculateTotal();
    });

    $("#id_descuento").on('input', function() {
        recalculateTotal();
    });

     $("[id^=id_ofertatec][id$=cant_horas]," +
       "[id^=id_ofertatec][id$=cantidad]," +
       "[id^=id_ofertatec][id$=precio]")
        .on('input', function (e) {
            var cant_horas_id = $(this).attr('id'),
                formset_number = cant_horas_id.split("-")[1],
                cantidad = parseFloat($("[id$="+formset_number+"-cantidad"+"]").val()),
                cant_horas = parseFloat($("[id$="+formset_number+"-cant_horas"+"]").val()),
                precio = parseFloat($("[id$="+formset_number+"-precio"+"]").val()),
                precio_total = $("[id$="+formset_number+"-precio_total"+"]"),
                acc = precio;

                if (!isNaN(cant_horas)) {
                    acc *= cant_horas;
                }
                if (!isNaN(cantidad)) {
                    acc *= cantidad;
                }
                precio_total.val(acc);
    });

    $("[id^=id_adm-ot][id$=cantidad]," +
      "[id^=id_adm-ot][id$=cant_horas]," +
      "[id^=id_adm-ot][id$=precio]")
            .on('input', function (e) {
                // Recalculo los campos cantidad, cantidad_horas, precio y precio_total.
                var input_id = $(this).attr('id'),
                    formset_number = input_id.split("-")[4],
                    cantidad = parseFloat($("[id$="+formset_number+"-cantidad"+"]").val()),
                    cant_horas = parseFloat($("[id$="+formset_number+"-cant_horas"+"]").val()),
                    precio = parseFloat($("[id$="+formset_number+"-precio"+"]").val()),
                    precio_total = $("[id$="+formset_number+"-precio_total"+"]"),
                    acc = precio;

                if (!isNaN(cant_horas)) {
                    acc *= cant_horas;
                }
                if (!isNaN(cantidad)) {
                    acc *= cantidad;
                }
                precio_total.val(acc);

                // Recalculo los campos importe neto e importe bruto
                recalculateTotal();

    });

    $("[id^=id_adm-factura][id$=numero]").on('change', function (e) {
        importe = $('#id_importe_neto').val();
        field_id = $(this).attr('id')
        importe_id = field_id.split("numero")[0] + 'importe'
        $('#'+importe_id).val(importe);

    });

    $("select#id_codigo").on('change keyup', function (e) {
        var presup_id = $(this).val()
        if (presup_id != "") {
            $.ajax({
                url: domain + '/lab/turnos/get_presup/',
                method: 'get',
                data: {'presup_id': presup_id},
                success: function(data){
                    $("#id_fecha_solicitado").text(data['fecha_solicitado']);
                    $("#id_fecha_realizado").text(data['fecha_realizado']);
                    $("#id_fecha_aceptado").text(data['fecha_aceptado']);
                    $("#id_fecha_instrumento").text(data['fecha_instrumento']);
                    $("#id_usuario").text(data['usuario']);
                    $("#id_mail").text(data['mail']);
                    $("#id_rubro").text(data['rubro']);
                },
            });
        }
    });

    //postForm = function() {
    //    var form = $("#presupForm");
    //    var id = $("#viewWord").data('id');
    //    $.ajax({
    //        url: domain + '/adm/presup/update/' + id + '/',
    //        method: 'post',
    //        data: form.serialize(),
    //    });
    //};


    //$("#viewWord").click(function(e) {
    //    postForm();
    //});

    $('#viewWord').click(function(event) {
        var id = $(this).data('id')
        var template = $("#id_tipo").val();
        $.ajax({
            url: domain + '/adm/presup/viewWord/'+id+'/'+template,
            method: 'get',
            success: function(){ location.href = domain + '/adm/presup/viewWord/'+id+'/'+template },
            error: function(data){alert('ERROR')}
        });
        trlink=true;
        return false;
    });


    $('#myForm').on('submit', function() {
        $.ajax({
            url     : $(this).attr('action'),
            type    : $(this).attr('method'),
            dataType: 'json',
            data    : $(this).serialize(),
            success : function( json ) {
                        if (json.ok) {
                            $('#myModal').modal('hide');
                            if (json.redirect) {
                                location.href = json.redirect
                            }
                            else {
                                window.location = window.location.href.split("?")[0];
                                window.location.reload();
                            }
                        }
                        else {
                            $('#myModal').modal('hide');
                            $('#myErrorModal .modal-body h4').text(json.msg);
                            $('#myErrorModal').modal('show');
                        }
            },
            error   : function( json ) {
                     alert("ERROR!");
                     $('#myModal').modal('hide');
            }
        });
        return false;
    });

    $('#modal').on('hide.bs.modal', function (event) {
         // Si no lo destruyo queda cacheado
         $(this).data('bs.modal', null);
         trlink=true;
    });

    $('#myModal').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget)
        var action = button.data('action')
        var model = button.data('model')
        var id = button.data('id')
        var f = document.getElementById('myForm')
        var submitButton = document.getElementById('submitButton')
        var inputField = document.getElementById('inputField')
        var modal = $(this)
        modal.find('.modal-title').text(action +' '+ model)
        var art = ' el ';
        var artP = 'Los ';
        //if ((model=='OT') || (model=='factura'))
        if (model=='OT' || model=='OT-ML' || model=='SOT' || model=='RUT' || model=='ofertatec')
            art = ' la ';
            artP = 'Las ';
        if (action.localeCompare('Finalizar')==0) {
            if (model=='OT') {
                var msg = "Las OT deben ser finalizadas solo en caso que ya hayan sido pagadas.\
                    Tenga en cuenta que una vez finalizada ya no podrá modificarse."
            }
            else
                var msg = artP+model+"s deben ser finalizados solo en caso que ya se hayan realizado.\
                    Tenga en cuenta que una vez finalizado ya no podrá modificarse."
            modal.find('.modal-body h4').text("¿Está seguro que quiere finalizar"+art+model+"?")
            modal.find('.modal-body p').text(msg)
        }
        if (action.localeCompare('Cancelar')==0 || action.localeCompare('CancelarF')==0) {
            modal.find('.modal-body h4').text("¿Está seguro que quiere cancelar"+art+model+"?")
            modal.find('.modal-body p').text("")
        }
        if (action.localeCompare('Eliminar')==0) {
            modal.find('.modal-body h4').text("¿Está seguro que quiere eliminar"+art+model+"?")
            modal.find('.modal-body p').text("")
        }
        if (action.localeCompare('Actualizar')==0) {
            modal.find('.modal-body h4').text("¿Está seguro que quiere actualizar los precios?")
            modal.find('.modal-body p').text("Tenga en cuenta que, en caso de que el presupuesto ya haya sido enviado,\
                                               esto dará lugar a una nueva revisión.")
        }
        if (action.localeCompare('Restaurar')==0) {
            modal.find('.modal-body h4').text("¿Está seguro que quiere restaurar"+art+model+"?")
            modal.find('.modal-body p').text("")
        }
        //En OTs agrego opcion para finalizar solo OT u OT y presupuesto
        if (model=='OT' && action=='Finalizar') {
            $(submitButton).text('Finalizar OT');
            submitButton.name = 'Finalizar1';
            submitButton.value = id;
            $(submitButton).attr('onclick', "$('#inputField').attr('name', 'Finalizar1').attr('value', " + id + ")");
            $('#submitButton2').remove();
            var btn = $("<button id='submitButton2' type='submit' class='btn btn-primary' name='name' value='value'></button>");
            $("#myForm").append(btn);
            submitButton2 = document.getElementById('submitButton2');
            $(submitButton2).text('Finalizar OT y Presupuesto');
            submitButton2.name = 'Finalizar1';
            submitButton2.value = id;
            $(submitButton2).attr('onclick', "$('#inputField').attr('name', 'Finalizar2').attr('value', " + id + ")");
        }
        //En SOTs agrego opcion para finalizar solo SOT u SOT y presupuesto
        else if (model=='SOT' && action=='Finalizar') {
            $(submitButton).text('Finalizar SOT');
            submitButton.name = 'Finalizar1';
            submitButton.value = id;
            $(submitButton).attr('onclick', "$('#inputField').attr('name', 'Finalizar1').attr('value', " + id + ")");
            $('#submitButton2').remove();
            var btn = $("<button id='submitButton2' type='submit' class='btn btn-primary' name='name' value='value'></button>");
            $("#myForm").append(btn);
            submitButton2 = document.getElementById('submitButton2');
            $(submitButton2).text('Finalizar SOT y Presupuesto');
            submitButton2.name = 'Finalizar1';
            submitButton2.value = id;
            $(submitButton2).attr('onclick', "$('#inputField').attr('name', 'Finalizar2').attr('value', " + id + ")");
        }
        //En RUTs agrego opcion para finalizar solo RUT u RUT y presupuesto
        else if (model=='RUT' && action=='Finalizar') {
            $(submitButton).text('Finalizar RUT');
            submitButton.name = 'Finalizar1';
            submitButton.value = id;
            $(submitButton).attr('onclick', "$('#inputField').attr('name', 'Finalizar1').attr('value', " + id + ")");
            $('#submitButton2').remove();
            var btn = $("<button id='submitButton2' type='submit' class='btn btn-primary' name='name' value='value'></button>");
            $("#myForm").append(btn);
            submitButton2 = document.getElementById('submitButton2');
            $(submitButton2).text('Finalizar RUT y Presupuesto');
            submitButton2.name = 'Finalizar1';
            submitButton2.value = id;
            $(submitButton2).attr('onclick', "$('#inputField').attr('name', 'Finalizar2').attr('value', " + id + ")");
        }
        else {
            $(submitButton).text('Aceptar');
            $(submitButton).removeAttr('onclick');
            $('#submitButton2').remove();
            submitButton.name = action
            submitButton.value = id

            inputField.name = action
            inputField.value = id
        }

        trlink=true;
    });

    $('#textBoxModal').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget)
        var action = button.data('action')
        var model = button.data('model')
        var id = button.data('id')
        var f = document.getElementById('textBoxForm')
        var submitButton = document.getElementById('submitBtn')
        var inputField = document.getElementById('inputField2')
        var modal = $(this)
        modal.find('.modal-title').text(action +' '+ model)

        submitButton.name = action
        submitButton.value = id

        inputField.name = action
        inputField.value = id

        trlink=true;
    });

    $('#textBoxModal').on('hide.bs.modal', function (event) {
         // Si no lo destruyo queda cacheado
         $(this).data('bs.modal', null);
         trlink=true;
    });

    $('textarea[name=observations]').bind('input propertychange', function() {
        if($.trim($('[name=observations]').val()) == '' ||
           ($.trim($('[name=observations]').val())).indexOf('Registro automático') >= 0){
            $("#submitBtn").prop('disabled', true);
        } else {
            $("#submitBtn").prop('disabled', false);
        }
    });

    $('#textBoxModalForm').on('submit', function() {
        $.ajax({
            url     : $(this).attr('action'),
            type    : $(this).attr('method'),
            dataType: 'json',
            data    : $(this).serialize(),
            success : function( json ) {
                        if (json.ok) {
                            $('#textBoxModal').modal('hide');
                            window.location = window.location.href.split("?")[0];
                            window.location.reload();
                        }
                        else {
                            $('#textBoxModal').modal('hide');
                            $('#myErrorModal .modal-body h4').text(json.msg);
                            $('#myErrorModal').modal('show');
                        }
            },
            error   : function( json ) {
                     alert("ERROR!");
                     $('#textBoxModal').modal('hide');
            }
        });
        return false;
    });

    $('.dropdown').on({
        "hide.bs.dropdown": function () {
            if (!close) {
                close = true;
                return false;
                }
            },
    });

/*
    $('.cbSearch').on({"change keyup": function(e) {
        var fieldName = $(this).attr('id').split("-")[0];
        var key = this.value.toUpperCase();
        $.each($(".cb[name=" + fieldName + "]"), function(index, input) {
            if (input.value.toUpperCase().indexOf(key) != 0) {

               input.closest('label').hidden = true;
            }
            else {
                input.closest('label').hidden = false;
            }
        });
    }
    });
*/

    $("#change_pass").on({"click": function (e) {
            document.getElementById("id_old_password").removeAttribute("disabled");
            document.getElementById("id_new_password").removeAttribute("disabled");
            document.getElementById("id_cnew_password").removeAttribute("disabled");
            return false;
        }
    });

    $('#id_descuento_fijo').change(function() {
        if(this.checked) {
            // Calculo el 10% del bruto
            importe_bruto = parseFloat($('#id_importe_bruto').val());
            $('#id_descuento').val(importe_bruto/10);
            $('#id_descuento').attr('readonly', true);
        }
        else {
            $('#id_descuento').attr('readonly', false);
            $("[id$=id_descuento]").val(0);
        }
        $("[id$=id_descuento]").trigger("input");
    });

    $('.modal.draggable>.modal-dialog').draggable({
        cursor: 'move',
        handle: '.modal-header'
    });
    $('.modal.draggable>.modal-dialog>.modal-content>.modal-header').css('cursor', 'move');

});
