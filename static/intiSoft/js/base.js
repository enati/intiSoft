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
        method: 'get',
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
        method: 'get',
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
        method: 'get',
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
        method: 'get',
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


    $("#ofertatec_formtable select").on('change keyup', function (e) {
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
                    $('#ofertatecform_table').load('#ofertatecform_table');
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
                    $("#id_fecha_solicitado").text(data['fecha_solicitado']);
                    $("#id_fecha_realizado").text(data['fecha_realizado']);
                    $("#id_fecha_aceptado").text(data['fecha_aceptado']);
                    $("#id_fecha_instrumento").text(data['fecha_instrumento']);
                    $("#id_usuario").text(data['usuario']);
                    $("#id_mail").text(data['mail']);
                    $("#id_rubro").text(data['rubro']);
                    $("#id_presupuesto__area").text(data['area']);
                    $("#id_presupuesto__usuario__nombre").text(data['usuario']);

                    var n = $('#id_adm-ot_linea-content_type-object_id-TOTAL_FORMS').val()
                    for (i=0; i<n; i++) {
                        $('#ofertatec_formtable tr.inline:first a.delete-row').click()
                    }
                    for (i=0; i<data['ofertatec'].length; i++) {
                        $('#ofertatec_formtable .add-row').click();
                        $('#ofertatec_formtable tr:last>td>select').val(data['ofertatec'][i].ofertatec);
                        $('#ofertatec_formtable tr:last>td>input')[0].value = data['ofertatec'][i].codigo;
                        // El [1] es detalle, no lo completo
                        $('#ofertatec_formtable tr:last>td>input')[2].value = data['ofertatec'][i].tipo_servicio;
                        $('#ofertatec_formtable tr:last>td>input')[3].value = data['ofertatec'][i].cantidad;
                        $('#ofertatec_formtable tr:last>td>input')[4].value = data['ofertatec'][i].cant_horas;
                        $('#ofertatec_formtable tr:last>td>input')[5].value = data['ofertatec'][i].precio;
                        $('#ofertatec_formtable tr:last>td>input')[6].value = data['ofertatec'][i].precio_total;
                    }
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

    $("[id^=id_ofertatec][id$=cant_horas], [id^=id_ofertatec][id$=cantidad], [id^=id_ofertatec][id$=precio]")
        .on('change', function (e) {
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

    $("[id^=id_adm-ot][id$=cantidad], [id^=id_adm-ot][id$=cant_horas], [id^=id_adm-ot][id$=precio]")
            .on('change', function (e) {
                var cant_horas_id = $(this).attr('id'),
                    formset_number = cant_horas_id.split("-")[4],
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

    $("[id^=id_adm-ot][id$=cant_horas]").on('change', function (e) {
        cant_horas_id = $(this).attr('id')
        formset_number = cant_horas_id.split("-")[4];
        cantidad = parseFloat($("[id$="+formset_number+"-cantidad"+"]").val());
        cant_horas = parseFloat($("[id$="+formset_number+"-cant_horas"+"]").val());
        precio = parseFloat($("[id$="+formset_number+"-precio"+"]").val());
        precio_total = $("[id$="+formset_number+"-precio_total"+"]");
        if (isNaN(cant_horas)) {
            precio_total.val(precio);
        }
        else {
            precio_total.val(cantidad*cant_horas*precio);
        }
    });

    $("[id^=id_adm-factura][id$=numero]").on('change', function (e) {
        importe = $('#id_importe_neto').val();
        field_id = $(this).attr('id')
        importe_id = field_id.split("numero")[0] + 'importe'
        $('#'+importe_id).val(importe);

    });

    $("#btnImporteNeto").on('click', function(e) {
        var otLinePrice_list = $("[id^=id_adm-ot][id$=precio_total]"),
            total = 0,
            importe_bruto = $("[id$=id_importe_bruto]"),
            importe_neto = $("[id$=id_importe_neto]"),
            descuento_val = parseFloat($("[id$=id_descuento]").val());
        for (var i=0; i<otLinePrice_list.length; i++) {
            if (otLinePrice_list[i].closest('tr').style.display != 'none') {
                total += parseFloat(otLinePrice_list[i].value);
            }
        }
        importe_bruto.val(total);
        importe_neto.val(total - descuento_val);
    });

    $("#id_codigo").on('change keyup', function (e) {
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

    $("#id_asistencia").click(function() {
        var id = $("#viewWord").data('id');
        document.getElementById("id_calibracion").checked = false;
        document.getElementById("id_in_situ").checked = false;
        document.getElementById("id_lia").checked = false;
        //postForm();
    });

    $("#id_calibracion").click(function() {
        var id = $("#viewWord").data('id');
        document.getElementById("id_asistencia").checked = false;
        document.getElementById("id_in_situ").checked = false;
        document.getElementById("id_lia").checked = false;
        //postForm();
    });

    $("#id_in_situ").click(function() {

        document.getElementById("id_asistencia").checked = false;
        document.getElementById("id_calibracion").checked = false;
        document.getElementById("id_lia").checked = false;
        //postForm();
    });

    $("#id_lia").click(function() {
        var id = $("#viewWord").data('id');
        document.getElementById("id_asistencia").checked = false;
        document.getElementById("id_calibracion").checked = false;
        document.getElementById("id_in_situ").checked = false;
        //postForm();
    });

    $("#viewWord").click(function(e) {
        var id = $(this).data('id')
        asist = document.getElementById("id_asistencia");
        calib = document.getElementById("id_calibracion");
        in_situ = document.getElementById("id_in_situ");
        lia = document.getElementById("id_lia");

        if (!asist.checked &
            !calib.checked &
            !in_situ.checked &
            !lia.checked)
        {
            $('#myErrorModal .modal-body h4').text("No hay ninguna plantilla seleccionada.");
            $('#myErrorModal').modal('show');
            return false
        }
    });

    //$('#viewWord').click(function(event) {
         //   var id = $(this).data('id')
         //   $.ajax({
         //   url: '/adm/presup/viewWord/',
         //   method: 'get',
         //   data: {'presup_id': id},
         //   success: function(){ location.href = '/adm/presup/viewWord/' }
         //});
            //trlink=true;
            //return false;
        //});


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
        if (model=='OT' || model=='OT-ML')
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
            modal.find('.modal-body p').text("Tenga en cuenta que esto dará lugar a una nueva revisión.")
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
    })

    $('.dropdown').on({
        "hide.bs.dropdown": function () {
            if (!close) {
                close = true;
                return false;
                }
            },
    });

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

    submitAll = function(){
        //Crea un formulario con todas las opciones seleccionadas
        //de cada dropbox
        var f = document.createElement("form");
        f.setAttribute('method',"get");
        f.setAttribute('action', "");

        var checkbox_list = document.getElementsByClassName("cb");

        for (var i=0; i<checkbox_list.length; i++) {
            if (checkbox_list[i].checked) {
                var n = document.createElement("input");
                n.setAttribute('type',"hidden");
                n.setAttribute('name',checkbox_list[i].name);
                n.setAttribute('value',checkbox_list[i].value);
                n.checked = true;
                f.appendChild(n);
            }
        }
        document.body.appendChild(f);
        f.submit();
    };

    $("#change_pass").on({"click": function (e) {
            document.getElementById("id_old_password").removeAttribute("disabled");
            document.getElementById("id_new_password").removeAttribute("disabled");
            document.getElementById("id_cnew_password").removeAttribute("disabled");
            return false;
        }
    });

});
