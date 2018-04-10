Para insertar la tabla en un template:

{% if object %}
    $.ajax({
        url: '/recent_activity/',                        //Url donde se incluyeron las url del modulo
        method: 'get',
        data: {
                'content_type_id': 10,           //Content_type del modelo,
                'object_id': {{ object.id }}    //Id del objeto que se quiere ver
        },
        success:
            function(data) {
                $('#recent_activity_table').html(data);
            }
    });
{% endif %}

<div class="row">
    <div id="recent_activity_table" class="col-md-offset-1 col-md-10">
    </div>
</div>