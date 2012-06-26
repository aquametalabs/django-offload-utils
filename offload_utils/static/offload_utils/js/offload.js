function offload_ajax(element, success_callback, failure_callback, extras) {
    var url = element.attr('data-offload-url');
    var function_name = element.attr('data-offload-function');
    var datatype = element.attr('data-offload-datatype');
    var uid = element.attr('data-offload-uid');
    $.ajax({
        url: url,
        data: {
            function_name: function_name,
            extras: JSON.stringify(extras),
            datatype: datatype,
            uid: uid,
        },
        type:'POST',
        dataType: 'json',
        success: function(data) {
            success_callback(data, $(this));
        },
        error: function(err) {
            failure_callback(err, $(this));
        }
    });
}

function offload_check_status(success_callback, failure_callback) {
    $('[data-offload-uid]').each(function() {
        var uid = $(this).attr('data-offload-uid');
        $.ajax({
            url: offload_check_url,
            data: {
                uid: uid,
            },
            type:'POST',
            dataType: 'json',
            success: function(data) {
                success_callback(data, $(this));
            },
            error: function(err) {
                failure_callback(err, $(this));
            }
        });
    });
    setTimeout(function(){offload_check_status(success_callback, failure_callback)}, 5000);
}
