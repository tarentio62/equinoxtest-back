from django.conf.urls import patterns, url

urlpatterns = patterns(
    'api.views',
    url(r'^tests/$', 'test_list', name='test_list'),
    url(r'^extension/$', 'extension_test_creation', name='extension_test_creation'),
    url(r'^tests/(?P<pk>[0-9]+)$', 'test_detail', name='test_detail'),
)


