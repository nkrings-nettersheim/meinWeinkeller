import logging

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views import generic
from django.core.exceptions import ObjectDoesNotExist

from .models import Weinkeller, Weinland, Region, Rebsorte, Wein, Erzeuger, Lager, Bestand
from .forms import WeinlandForm, RegionForm, RebsorteForm, WeinForm, ErzeugerForm, LagerForm, BestandForm, \
    WeinkellerForm

logger = logging.getLogger(__name__)


def index(request):
    weinkeller_data = Weinkeller.objects.filter(weinkeller_admin_id=request.user.id)
    if weinkeller_data:
        return redirect('list/weine')
    else:
        return redirect('add/weinkeller')


def impressum(request):
    return render(request, 'lager/impressum.html')


def datenschutz(request):
    return render(request, 'lager/datenschutz.html')


##########################################################################
# Area Weinland create and change
##########################################################################
def add_weinland(request):
    if request.method == "POST":
        mydata = Weinkeller.objects.filter(weinkeller_user_id=request.user.id).values().first()
        request.POST._mutable = True
        request.POST['weinkeller'] = mydata['weinkeller_admin_id']
        form = WeinlandForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.save()
            return redirect('/lager/list/weinland/')
    else:
        form = WeinlandForm()
    return render(request, 'lager/weinland_form.html', {'form': form})


def edit_weinland(request, id=None):
    item = get_object_or_404(Weinland, id=id, weinkeller=request.user.id)
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
        return Weinland.objects.filter(weinkeller=str(self.request.user.id)).order_by('kontinent', 'land')


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
        mydata = Weinkeller.objects.filter(weinkeller_user_id=request.user.id).values().first()
        request.POST._mutable = True
        request.POST['weinkeller'] = mydata['weinkeller_admin_id']
        form = RegionForm(request.POST, user=request.user.id)
        if form.is_valid():
            item = form.save(commit=False)
            item.save()

            return redirect('/lager/region/' + str(item.id) + '/')
    else:
        form = RegionForm(user=request.user.id)
    return render(request, 'lager/region_form.html', {'form': form})


def edit_region(request, id=None):
    item = get_object_or_404(Region, id=id, weinkeller=request.user.id)
    form = RegionForm(request.POST or None, instance=item, user=request.user.id)
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
        return Region.objects.filter(weinkeller=str(self.request.user.id)).order_by('weinland', 'region')


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
        mydata = Weinkeller.objects.filter(weinkeller_user_id=request.user.id).values().first()
        request.POST._mutable = True
        request.POST['weinkeller'] = mydata['weinkeller_admin_id']
        form = RebsorteForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.save()

            return redirect('/lager/rebsorte/' + str(item.id) + '/')
    else:
        form = RebsorteForm()
    return render(request, 'lager/rebsorte_form.html', {'form': form})


def edit_rebsorte(request, id=None):
    item = get_object_or_404(Rebsorte, id=id, weinkeller=request.user.id)
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
        return Rebsorte.objects.filter(weinkeller=str(self.request.user.id)).order_by('rebsorte')


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
        mydata = Weinkeller.objects.filter(weinkeller_user_id=request.user.id).values().first()
        request.POST._mutable = True
        request.POST['weinkeller'] = mydata['weinkeller_admin_id']
        form = WeinForm(request.POST, user=request.user.id)
        if form.is_valid():
            item = form.save(commit=False)
            item.save()

            return redirect('/lager/wein/' + str(item.id) + '/')
    else:
        form = WeinForm(user=request.user.id)
    return render(request, 'lager/wein_form.html', {'form': form})


def edit_wein(request, id=None):
    item = get_object_or_404(Wein, id=id, weinkeller=request.user.id)
    form = WeinForm(request.POST or None, instance=item, user=request.user.id)
    # assert False
    if form.is_valid():
        form.save()
        return redirect('/lager/wein/' + str(item.id) + '/')

    form.id = item.id
    return render(request, 'lager/wein_form.html', {'form': form})


# Liste der Weine
class WeineView(generic.ListView):
    model = Wein
    template_name = 'lager/weine.html'
    context_object_name = 'weine_list'

    def get_queryset(self):
        return Wein.objects.filter(weinkeller=str(self.request.user.id)).order_by('weinland', 'region', 'erzeuger',
                                                                                  'jahrgang', 'name')


# Anzeige einzelne Region
def wein(request, id=id):
    try:
        wein_result = Wein.objects.get(id=id)
        return render(request, 'lager/wein.html', {'wein': wein_result})
    except ObjectDoesNotExist:
        return redirect('/lager/')


##########################################################################
# Area Erzeuger create and change
##########################################################################
def add_erzeuger(request):
    if request.method == "POST":
        mydata = Weinkeller.objects.filter(weinkeller_user_id=request.user.id).values().first()
        request.POST._mutable = True
        request.POST['weinkeller'] = mydata['weinkeller_admin_id']
        form = ErzeugerForm(request.POST, user=request.user.id)
        if form.is_valid():
            item = form.save(commit=False)
            item.save()

            return redirect('/lager/erzeuger/' + str(item.id) + '/')
    else:
        form = ErzeugerForm(user=request.user.id)
    return render(request, 'lager/erzeuger_form.html', {'form': form})


def edit_erzeuger(request, id=None):
    item = get_object_or_404(Erzeuger, id=id, weinkeller=request.user.id)
    form = ErzeugerForm(request.POST or None, instance=item, user=request.user.id)
    # assert False
    if form.is_valid():
        form.save()
        return redirect('/lager/erzeuger/' + str(item.id) + '/')

    form.id = item.id
    return render(request, 'lager/erzeuger_form.html', {'form': form})


# Liste der Weine
class ErzeugersView(generic.ListView):
    model = Erzeuger
    template_name = 'lager/erzeugers.html'
    context_object_name = 'erzeugers_list'

    def get_queryset(self):
        return Erzeuger.objects.filter(weinkeller=str(self.request.user.id)).order_by('land', 'name')


# Anzeige einzelne Region
def erzeuger(request, id=id):
    try:
        erzeuger_result = Erzeuger.objects.get(id=id)
        return render(request, 'lager/erzeuger.html', {'erzeuger': erzeuger_result})
    except ObjectDoesNotExist:
        return redirect('/lager/')


##########################################################################
# Area Lager create and change
##########################################################################
def add_lager(request):
    if request.method == "POST":
        mydata = Weinkeller.objects.filter(weinkeller_user_id=request.user.id).values().first()
        request.POST._mutable = True
        request.POST['weinkeller'] = mydata['weinkeller_admin_id']
        form = LagerForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.save()

            return redirect('/lager/lager/' + str(item.id) + '/')
    else:
        form = LagerForm()
    return render(request, 'lager/lager_form.html', {'form': form})


def edit_lager(request, id=None):
    item = get_object_or_404(Lager, id=id, weinkeller=request.user.id)
    form = LagerForm(request.POST or None, instance=item)
    # assert False
    if form.is_valid():
        form.save()
        return redirect('/lager/lager/' + str(item.id) + '/')

    form.id = item.id
    return render(request, 'lager/lager_form.html', {'form': form})


# Liste der Weine
class LagersView(generic.ListView):
    model = Lager
    template_name = 'lager/lagers.html'
    context_object_name = 'lagers_list'

    def get_queryset(self):
        return Lager.objects.filter(weinkeller=str(self.request.user.id)).order_by('name')


# Anzeige einzelne Region
def lager(request, id=id):
    try:
        lager_result = Lager.objects.get(id=id)
        return render(request, 'lager/lager.html', {'lager': lager_result})
    except ObjectDoesNotExist:
        return redirect('/lager/')


##########################################################################
# Area Bestand create and change
##########################################################################
def add_bestand(request):
    if request.method == "POST":
        mydata = Weinkeller.objects.filter(weinkeller_user_id=request.user.id).values().first()
        request.POST._mutable = True
        request.POST['weinkeller'] = mydata['weinkeller_admin_id']
        form = BestandForm(request.POST, user=request.user.id)
        # assert False
        if form.is_valid():
            item = form.save(commit=False)
            item.save()

            return redirect('/lager/bestand/' + str(item.id) + '/')
    else:
        form = BestandForm(user=request.user.id)
    return render(request, 'lager/bestand_form.html', {'form': form})


def edit_bestand(request, id=None):
    item = get_object_or_404(Bestand, id=id, weinkeller=request.user.id)
    form = BestandForm(request.POST or None, instance=item, user=request.user.id)
    # assert False
    if form.is_valid():
        form.save()
        return redirect('/lager/bestand/' + str(item.id) + '/')

    form.id = item.id
    return render(request, 'lager/bestand_form.html', {'form': form})


# Liste der Weine
class BestandsView(generic.ListView):
    model = Bestand
    template_name = 'lager/bestands.html'
    context_object_name = 'bestands_list'

    def get_queryset(self):
        return Bestand.objects.filter(weinkeller=str(self.request.user.id)).order_by('wein')


# Anzeige einzelne Region
def bestand(request, id=id):
    try:
        bestand_result = Bestand.objects.get(id=id)
        return render(request, 'lager/bestand.html', {'bestand': bestand_result})
    except ObjectDoesNotExist:
        return redirect('/lager/')


##########################################################################
# Receiver Functions
##########################################################################
def add_weinkeller(request):
    if request.method == "POST":
        request.POST._mutable = True
        request.POST['weinkeller_admin_id'] = request.user.id
        request.POST['weinkeller_user_id'] = request.user.id
        form = WeinkellerForm(request.POST)
        # assert False
        if form.is_valid():
            item = form.save(commit=False)
            item.save()

            return redirect('/lager/list/weine/')
    else:
        form = WeinkellerForm()
    return render(request, 'lager/weinkeller_form.html', {'form': form})


##########################################################################
# AJAX Functions
##########################################################################
# AJAX
def ajax_load_regions(request):
    weinland_id = request.GET.get('weinland_id')
    regionen = Region.objects.filter(weinland_id=weinland_id).all().order_by('region')
    return render(request, 'lager/region_dropdown_list_options.html', {'regionen': regionen})
    # return JsonResponse(list(cities.values('id', 'name')), safe=False)
