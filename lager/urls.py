from django.urls import path
from . import views
from .views import index, WeinlandsView

app_name = 'lager'

urlpatterns = [
    path('', index, name='index'),
    path('impressum/', views.impressum, name='impressum'),
    path('datenschutz/', views.datenschutz, name='datenschutz'),

    path('add/weinland/', views.add_weinland, name='add_weinland'),
    path('edit/weinland/<id>/', views.edit_weinland, name='edit_weinland'),
    path('list/weinland/', WeinlandsView.as_view(), name='list_weinlands'),
    path('delete/weinland/<pk>/', views.DeleteWeinlandItem.as_view(), name='delete_weinland_item'),
    path('weinland/<id>/', views.weinland, name='weinland'),

    path('add/region/', views.add_region, name='add_region'),
    path('edit/region/<id>/', views.edit_region, name='edit_region'),
    path('list/regionen/', views.RegionView.as_view(), name='list_regionen'),
    path('delete/region/<pk>/', views.DeleteRegionItem.as_view(), name='delete_region_item'),
    path('region/<id>/', views.region, name='region'),

    path('add/rebsorte/', views.add_rebsorte, name='add_rebsorte'),
    path('edit/rebsorte/<id>/', views.edit_rebsorte, name='edit_rebsorte'),
    path('list/rebsorten/', views.RebsortenView.as_view(), name='list_rebsorten'),
    path('delete/rebsorte/<pk>/', views.DeleteRebsorteItem.as_view(), name='delete_rebsorte_item'),
    path('rebsorte/<id>/', views.rebsorte, name='rebsorte'),

    path('add/wein/', views.add_wein, name='add_wein'),
    path('edit/wein/<id>/', views.edit_wein, name='edit_wein'),
    path('list/weine/', views.WeineView.as_view(), name='list_weine'),
    path('delete/wein/<pk>/', views.DeleteWeinItem.as_view(), name='delete_wein_item'),
    path('wein/<id>/', views.wein, name='wein'),

    path('add/erzeuger/', views.add_erzeuger, name='add_erzeuger'),
    path('edit/erzeuger/<id>/', views.edit_erzeuger, name='edit_erzeuger'),
    path('list/erzeuger/', views.ErzeugersView.as_view(), name='list_erzeugers'),
    path('delete/erzeuger/<pk>/', views.DeleteErzeugerItem.as_view(), name='delete_erzeuger_item'),
    path('erzeuger/<id>/', views.erzeuger, name='erzeuger'),

    path('add/lager/', views.add_lager, name='add_lager'),
    path('edit/lager/<id>/', views.edit_lager, name='edit_lager'),
    path('list/lager/', views.LagersView.as_view(), name='list_lagers'),
    path('delete/lager/<pk>/', views.DeleteLagerItem.as_view(), name='delete_lager_item'),
    path('lager/<id>/', views.lager, name='lager'),

    path('add/bestand/', views.add_bestand, name='add_bestand'),
    path('edit/bestand/<id>/', views.edit_bestand, name='edit_bestand'),
    path('list/bestand/', views.BestandsView.as_view(), name='list_bestands'),
    path('delete/bestand/<pk>/', views.DeleteBestandItem.as_view(), name='delete_bestand_item'),
    path('bestand/<id>/', views.bestand, name='bestand'),
    path('report/bestand', views.print_bestand, name='print_bestand'),
    path('report/bestand2', views.print_bestand2, name='print_bestand2'),

    path('add/weinkeller/', views.add_weinkeller, name='add_weinkeller'),
    path('edit/weinkeller/<id>/', views.edit_weinkeller, name='edit_weinkeller'),
    path('list/weinkeller/', views.WeinkellersView.as_view(), name='list_weinkellers'),
    path('weinkeller/<id>/', views.weinkeller, name='weinkeller'),

    path('wf/wein/initial/', views.wf_wein_initial, name='wf_wein_initial'),
    path('wf/wein/weinland/', views.wf_wein_weinland, name='wf_wein_weinland'),
    path('wf/wein/rebsorte/', views.wf_wein_rebsorte, name='wf_wein_rebsorte'),
    path('wf/wein/erzeuger/', views.wf_wein_erzeuger, name='wf_wein_erzeuger'),
    path('wf/wein/weinbasis/', views.wf_wein_basis, name='wf_wein_basis'),
    path('wf/wein/weinzusatz/', views.wf_wein_zusatz, name='wf_wein_zusatz'),

    path('ajax/load-regionen/', views.ajax_load_regions, name='ajax_load_regions'),  # AJAX
    path('ajax/load-lagers/', views.ajax_load_lagers, name='ajax_load_lagers'),  # AJAX
]