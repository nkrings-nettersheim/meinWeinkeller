import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views import generic
from django.core.exceptions import ObjectDoesNotExist

from .models import Weinland, Region, Rebsorte, Wein
from .forms import WeinlandForm, RegionForm, RebsorteForm, WeinForm

logger = logging.getLogger(__name__)


def index(request):
    return render(request, 'lager/index.html', )


def impressum(request):
    return render(request, 'lager/impressum.html')


def datenschutz(request):
    return render(request, 'lager/datenschutz.html')


##########################################################################
# Area Weinland create and change
##########################################################################
def add_weinland(request):
    if request.method == "POST":
        form = WeinlandForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.save()

            return redirect('/lager/weinland/' + str(item.id) + '/')
    else:
        form = WeinlandForm()
    return render(request, 'lager/weinland_form.html', {'form': form})


def edit_weinland(request, id=None):
    item = get_object_or_404(Weinland, id=id)
    form = WeinlandForm(request.POST or None, instance=item)
    if form.is_valid():
        form.save()
        return redirect('/lager/weinland/' + str(item.id) + '/')
    form.id = item.id
    return render(request, 'lager/weinland_form.html', {'form': form})


# Liste der Weinländer
class WeinlandsView(generic.ListView):
    model = Weinland
    template_name = 'lager/weinlands.html'
    context_object_name = 'weinlands_list'

    def get_queryset(self):
        return Weinland.objects.all().order_by('kontinent', 'land')


# Anzeige einzelnes Weinland
def weinland(request, id=id):
    try:
        weinland_result = Weinland.objects.get(id=id)
        return render(request, 'lager/weinland.html', {'weinland': weinland_result})
    except ObjectDoesNotExist:
        return redirect('/lager/')


##########################################################################
# Area Region create and change
##########################################################################
def add_region(request):
    if request.method == "POST":
        form = RegionForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.save()

            return redirect('/lager/region/' + str(item.id) + '/')
    else:
        form = RegionForm()
    return render(request, 'lager/region_form.html', {'form': form})


def edit_region(request, id=None):
    item = get_object_or_404(Region, id=id)
    form = RegionForm(request.POST or None, instance=item)
    if form.is_valid():
        form.save()
        return redirect('/lager/region/' + str(item.id) + '/')
    form.id = item.id
    return render(request, 'lager/region_form.html', {'form': form})


# Liste der Region
class RegionView(generic.ListView):
    model = Region
    template_name = 'lager/regionen.html'
    context_object_name = 'regionen_list'

    def get_queryset(self):
        return Region.objects.all().order_by('weinland', 'region')


# Anzeige einzelne Region
def region(request, id=id):
    try:
        region_result = Region.objects.get(id=id)
        return render(request, 'lager/region.html', {'region': region_result})
    except ObjectDoesNotExist:
        return redirect('/lager/')


##########################################################################
# Area Rebsorte create and change
##########################################################################
def add_rebsorte(request):
    if request.method == "POST":
        form = RebsorteForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.save()

            return redirect('/lager/rebsorte/' + str(item.id) + '/')
    else:
        form = RebsorteForm()
    return render(request, 'lager/rebsorte_form.html', {'form': form})


def edit_rebsorte(request, id=None):
    item = get_object_or_404(Rebsorte, id=id)
    form = RebsorteForm(request.POST or None, instance=item)
    if form.is_valid():
        form.save()
        return redirect('/lager/rebsorte/' + str(item.id) + '/')
    form.id = item.id
    return render(request, 'lager/rebsorte_form.html', {'form': form})


# Liste der Rebsorten
class RebsortenView(generic.ListView):
    model = Rebsorte
    template_name = 'lager/rebsorten.html'
    context_object_name = 'rebsorten_list'

    def get_queryset(self):
        return Rebsorte.objects.all().order_by('rebsorte')


# Anzeige einzelne Region
def rebsorte(request, id=id):
    try:
        rebsorte_result = Rebsorte.objects.get(id=id)
        return render(request, 'lager/rebsorte.html', {'rebsorte': rebsorte_result})
    except ObjectDoesNotExist:
        return redirect('/lager/')


##########################################################################
# Area Wein create and change
##########################################################################
def add_wein(request):
    if request.method == "POST":
        form = WeinForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.save()

            return redirect('/lager/wein/' + str(item.id) + '/')
    else:
        form = WeinForm()
    return render(request, 'lager/wein_form.html', {'form': form})


def edit_wein(request, id=None):
    item = get_object_or_404(Wein, id=id)
    form = WeinForm(request.POST or None, instance=item)
    #assert False
    if form.is_valid():
        form.save()
        return redirect('/lager/wein/' + str(item.id) + '/')
    else:
        print("Fehler")
    form.id = item.id
    return render(request, 'lager/wein_form.html', {'form': form})


# Liste der Weine
class WeineView(generic.ListView):
    model = Wein
    template_name = 'lager/weine.html'
    context_object_name = 'weine_list'

    def get_queryset(self):
        return Wein.objects.all().order_by('weinland', 'region', 'erzeuger', 'jahrgang', 'name')


# Anzeige einzelne Region
def wein(request, id=id):
    try:
        wein_result = Wein.objects.get(id=id)
        return render(request, 'lager/wein.html', {'wein': wein_result})
    except ObjectDoesNotExist:
        return redirect('/lager/')


# AJAX
def ajax_load_regions(request):
    weinland_id = request.GET.get('weinland_id')
    regionen = Region.objects.filter(weinland_id=weinland_id).all().order_by('region')
    return render(request, 'lager/region_dropdown_list_options.html', {'regionen': regionen})
    # return JsonResponse(list(cities.values('id', 'name')), safe=False)
