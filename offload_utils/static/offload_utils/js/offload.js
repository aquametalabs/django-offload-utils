function offload_ajax(element, success_callback, failure_callback, extras) {
    var url = element.attr('data-offload-url');
    var function_name = element.attr('data-offload-function');
    var datatype = element.attr('data-offload-datatype');
    $.ajax({
        url: url,
        data: {
            function_name: function_name,
            extras: JSON.stringify(extras),
            datatype: datatype,
        },
        type:'POST',
        dataType: 'json',
        success: function(data) {
            success_callback(data, element);
        },
        error: function(err) {
            failure_callback(err);
        }
    });
}
