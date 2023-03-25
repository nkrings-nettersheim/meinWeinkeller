from django.urls import path
from . import views

app_name = 'lager'

urlpatterns = [
    path('', views.index, name='index'),
    path('impressum/', views.impressum, name='impressum'),
    path('datenschutz/', views.datenschutz, name='datenschutz'),

    path('add/weinland/', views.add_weinland, name='add_weinland'),
    path('edit/weinland/<id>/', views.edit_weinland, name='edit_weinland'),
    path('list/weinland/', views.WeinlandsView.as_view(), name='list_weinlands'),
    path('weinland/<id>/', views.weinland, name='weinland'),

    path('add/region/', views.add_region, name='add_region'),
    path('edit/region/<id>/', views.edit_region, name='edit_region'),
    path('list/regionen/', views.RegionView.as_view(), name='list_regionen'),
    path('region/<id>/', views.region, name='region'),

    path('add/rebsorte/', views.add_rebsorte, name='add_rebsorte'),
    path('edit/rebsorte/<id>/', views.edit_rebsorte, name='edit_rebsorte'),
    path('list/rebsorten/', views.RebsortenView.as_view(), name='list_rebsorten'),
    path('rebsorte/<id>/', views.rebsorte, name='rebsorte'),

    path('add/wein/', views.add_wein, name='add_wein'),
    path('edit/wein/<id>/', views.edit_wein, name='edit_wein'),
    path('list/weine/', views.WeineView.as_view(), name='list_weine'),
    path('wein/<id>/', views.wein, name='wein'),

    path('ajax/load-regionen/', views.ajax_load_regions, name='ajax_load_regions'),  # AJAX
]