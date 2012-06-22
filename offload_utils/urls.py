import dselector


parser = dselector.Parser()
url = parser.url

urlpatterns = parser.patterns('offload_utils.views',
    url('offload_utils/start_offload_action', 'start_offload', name='offload_utils_start_offload_action'),
    url('offload_utils/check_status', 'check_status', name='offload_utils_check_status'),
)
