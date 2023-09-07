import datetime
import logging
import io

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import ProtectedError
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from django.views.generic.edit import DeleteView
from django.views.generic import ListView
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import PageBreak
from weasyprint import HTML, CSS
from django.template.loader import render_to_string
from django.conf import settings
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm


from .models import Weinkeller, Weinland, Region, Rebsorte, Wein, Erzeuger, Lager, Bestand
from .forms import WeinlandForm, RegionForm, RebsorteForm, WeinForm, ErzeugerForm, LagerForm, BestandForm, \
    WeinkellerForm
from .forms import WFWeinWeinlandForm, WFWeinRebsorteForm, WFWeinErzeugerForm, WFWeinBasisForm, WFWeinZusatzForm

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
@login_required
def add_weinland(request):
    f = request.GET['f']
    if request.method == "POST":
        mydata = Weinkeller.objects.filter(weinkeller_user_id=request.user.id).values().first()
        request.POST._mutable = True
        request.POST['weinkeller'] = mydata['weinkeller_admin_id']
        form = WeinlandForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.save()
            request.session['weinland_id'] = item.id
            if request.POST['parameter'] == "wf":
                return redirect('/lager/wf/wein/weinland/')
            else:
                return redirect('/lager/list/weinland/')
    else:
        form = WeinlandForm()
    return render(request, 'lager/weinland_form.html', {'form': form, 'parameter': f})

@login_required
def edit_weinland(request, id=None):
    item = get_object_or_404(Weinland, id=id, weinkeller=request.user.id)
    form = WeinlandForm(request.POST or None, instance=item)
    if form.is_valid():
        form.save()
        return redirect('/lager/weinland/' + str(item.id) + '/')
    form.id = item.id
    return render(request, 'lager/weinland_form.html', {'form': form})


# Liste der Weinländer
class WeinlandsView(LoginRequiredMixin, ListView):
    model = Weinland
    template_name = 'lager/weinlands.html'
    #context_object_name = 'weinlands_list'

    def get_queryset(self):
        return Weinland.objects.filter(weinkeller=str(self.request.user.id)).order_by('kontinent', 'land')


class DeleteWeinlandItem(LoginRequiredMixin, DeleteView):
    model = Weinland
    template_name = 'lager/weinland_confirm_delete.html'

    # success_url = "/lager/list/weinland/"

    def form_valid(self, form):
        success_url = "/lager/list/weinland/"
        self.object = self.get_object()
        try:
            self.object.delete()
            return HttpResponseRedirect(success_url)
        except ProtectedError:
            self.object = self.get_object()
            context = self.get_context_data(
                object=self.object,
                error="Der Datensatz kann nicht gelöscht werden, da es noch Verknüpfungen zu anderen Datensätzen gibt"
            )
            return self.render_to_response(context)


# Anzeige einzelnes Weinland
@login_required
def weinland(request, id=id):
    try:
        weinland_result = Weinland.objects.get(id=id)
        return render(request, 'lager/weinland.html', {'weinland': weinland_result})
    except ObjectDoesNotExist:
        return redirect('/lager/')


##########################################################################
# Area Region create and change
##########################################################################
@login_required
def add_region(request):
    f = request.GET['f']
    if request.method == "POST":
        mydata = Weinkeller.objects.filter(weinkeller_user_id=request.user.id).values().first()
        request.POST._mutable = True
        request.POST['weinkeller'] = mydata['weinkeller_admin_id']
        form = RegionForm(request.POST, user=request.user.id)
        if form.is_valid():
            item = form.save(commit=False)
            item.save()
            request.session['region_id'] = item.id
            if request.POST['parameter'] == "wf":
                return redirect('/lager/wf/wein/rebsorte/')
            else:
                return redirect('/lager/region/' + str(item.id) + '/')
    else:
        if 'weinland_id' in request.session:
            form = RegionForm(user=request.user.id, initial={'weinland': request.session['weinland_id']})
        else:
            form = RegionForm(user=request.user.id)
    return render(request, 'lager/region_form.html', {'form': form, 'parameter': f})


@login_required
def edit_region(request, id=None):
    item = get_object_or_404(Region, id=id, weinkeller=request.user.id)
    form = RegionForm(request.POST or None, instance=item, user=request.user.id)
    if form.is_valid():
        form.save()
        return redirect('/lager/region/' + str(item.id) + '/')
    form.id = item.id
    return render(request, 'lager/region_form.html', {'form': form})


# Liste der Region
class RegionView(LoginRequiredMixin, ListView):
    model = Region
    template_name = 'lager/regionen.html'
    context_object_name = 'regionen_list'

    def get_queryset(self):
        return Region.objects.filter(weinkeller=str(self.request.user.id)).order_by('weinland', 'region')


# Delete Region
class DeleteRegionItem(LoginRequiredMixin, DeleteView):
    model = Region
    template_name = 'lager/region_confirm_delete.html'

    def form_valid(self, form):
        success_url = "/lager/list/regionen/"
        self.object = self.get_object()
        try:
            self.object.delete()
            return HttpResponseRedirect(success_url)
        except ProtectedError:
            self.object = self.get_object()
            context = self.get_context_data(
                object=self.object,
                error="Der Datensatz kann nicht gelöscht werden, da es noch Verknüpfungen zu anderen Datensätzen gibt"
            )
            return self.render_to_response(context)


# Anzeige einzelne Region
@login_required
def region(request, id=id):
    try:
        region_result = Region.objects.get(id=id)
        return render(request, 'lager/region.html', {'region': region_result})
    except ObjectDoesNotExist:
        return redirect('/lager/')


##########################################################################
# Area Rebsorte create and change
##########################################################################
@login_required
def add_rebsorte(request):
    f = request.GET['f']
    if request.method == "POST":
        mydata = Weinkeller.objects.filter(weinkeller_user_id=request.user.id).values().first()
        request.POST._mutable = True
        request.POST['weinkeller'] = mydata['weinkeller_admin_id']
        form = RebsorteForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.save()
            request.session['rebsorte_id'] = item.id
            if request.POST['parameter'] == "wf":
                return redirect('/lager/wf/wein/rebsorte/')
            else:
                return redirect('/lager/rebsorte/' + str(item.id) + '/')
    else:
        form = RebsorteForm()
    return render(request, 'lager/rebsorte_form.html', {'form': form, 'parameter': f})


# Edit Rebsorte
@login_required
def edit_rebsorte(request, id=None):
    item = get_object_or_404(Rebsorte, id=id, weinkeller=request.user.id)
    form = RebsorteForm(request.POST or None, instance=item)
    if form.is_valid():
        form.save()
        return redirect('/lager/rebsorte/' + str(item.id) + '/')
    form.id = item.id
    return render(request, 'lager/rebsorte_form.html', {'form': form})


# Liste der Rebsorten
class RebsortenView(LoginRequiredMixin, ListView):
    model = Rebsorte
    template_name = 'lager/rebsorten.html'
    context_object_name = 'rebsorten_list'

    def get_queryset(self):
        return Rebsorte.objects.filter(weinkeller=str(self.request.user.id)).order_by('rebsorte')


# Delete Rebsorte
class DeleteRebsorteItem(LoginRequiredMixin, DeleteView):
    model = Rebsorte
    template_name = 'lager/rebsorte_confirm_delete.html'

    def form_valid(self, form):
        success_url = "/lager/list/rebsorten/"
        self.object = self.get_object()
        try:
            self.object.delete()
            return HttpResponseRedirect(success_url)
        except ProtectedError:
            self.object = self.get_object()
            context = self.get_context_data(
                object=self.object,
                error="Der Datensatz kann nicht gelöscht werden, da es noch Verknüpfungen zu anderen Datensätzen gibt"
            )
            return self.render_to_response(context)


# Anzeige einzelne Region
@login_required
def rebsorte(request, id=id):
    try:
        rebsorte_result = Rebsorte.objects.get(id=id)
        return render(request, 'lager/rebsorte.html', {'rebsorte': rebsorte_result})
    except ObjectDoesNotExist:
        return redirect('/lager/')


##########################################################################
# Area Wein create and change
##########################################################################
@login_required
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
            print("not valid")
    else:
        form = WeinForm(user=request.user.id)
    return render(request, 'lager/wein_form.html', {'form': form})


@login_required
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
class WeineView(LoginRequiredMixin, ListView):
    model = Wein
    template_name = 'lager/weine.html'
    context_object_name = 'weine_list'

    def get_queryset(self):
        return Wein.objects.filter(weinkeller=str(self.request.user.id)).order_by('weinland', 'region', 'erzeuger',
                                                                                  'jahrgang', 'name')


# Delete Wein
class DeleteWeinItem(LoginRequiredMixin, DeleteView):
    model = Wein
    template_name = 'lager/wein_confirm_delete.html'

    def form_valid(self, form):
        success_url = "/lager/list/weine/"
        self.object = self.get_object()
        try:
            self.object.delete()
            return HttpResponseRedirect(success_url)
        except ProtectedError:
            self.object = self.get_object()
            context = self.get_context_data(
                object=self.object,
                error="Der Datensatz kann nicht gelöscht werden, da es noch Verknüpfungen zu anderen Datensätzen gibt"
            )
            return self.render_to_response(context)


# Anzeige einzelne Region
@login_required
def wein(request, id=id):
    try:
        wein_result = Wein.objects.get(id=id)
        bestand_result = Bestand.objects.filter(wein=wein_result.id)
        return render(request, 'lager/wein.html', {'wein': wein_result, 'bestands': bestand_result})
    except ObjectDoesNotExist:
        return redirect('/lager/')


##########################################################################
# Area Erzeuger create and change
##########################################################################
@login_required
def add_erzeuger(request):
    f = request.GET['f']
    if request.method == "POST":
        mydata = Weinkeller.objects.filter(weinkeller_user_id=request.user.id).values().first()
        request.POST._mutable = True
        request.POST['weinkeller'] = mydata['weinkeller_admin_id']
        form = ErzeugerForm(request.POST, user=request.user.id)
        if form.is_valid():
            item = form.save(commit=False)
            item.save()
            request.session['erzeuger_id'] = item.id
            if request.POST['parameter'] == "wf":
                return redirect('/lager/wf/wein/erzeuger')
            else:
                return redirect('/lager/erzeuger/' + str(item.id) + '/')
    else:
        form = ErzeugerForm(user=request.user.id)
    return render(request, 'lager/erzeuger_form.html', {'form': form, 'parameter': f})


@login_required
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
class ErzeugersView(LoginRequiredMixin, ListView):
    model = Erzeuger
    template_name = 'lager/erzeugers.html'
    context_object_name = 'erzeugers_list'

    def get_queryset(self):
        return Erzeuger.objects.filter(weinkeller=str(self.request.user.id)).order_by('land', 'name')


# Delete Erzeuger
class DeleteErzeugerItem(LoginRequiredMixin, DeleteView):
    model = Erzeuger
    template_name = 'lager/erzeuger_confirm_delete.html'

    def form_valid(self, form):
        success_url = "/lager/list/erzeuger/"
        self.object = self.get_object()
        try:
            self.object.delete()
            return HttpResponseRedirect(success_url)
        except ProtectedError:
            self.object = self.get_object()
            context = self.get_context_data(
                object=self.object,
                error="Der Datensatz kann nicht gelöscht werden, da es noch Verknüpfungen zu anderen Datensätzen gibt"
            )
            return self.render_to_response(context)


# Anzeige einzelne Region
@login_required
def erzeuger(request, id=id):
    try:
        erzeuger_result = Erzeuger.objects.get(id=id)
        return render(request, 'lager/erzeuger.html', {'erzeuger': erzeuger_result})
    except ObjectDoesNotExist:
        return redirect('/lager/')


##########################################################################
# Area Lager create and change
##########################################################################
# Lager anlegen
@login_required
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

# Lager editieren
@login_required
def edit_lager(request, id=None):
    item = get_object_or_404(Lager, id=id, weinkeller=request.user.id)
    form = LagerForm(request.POST or None, instance=item)
    # assert False
    if form.is_valid():
        form.save()
        return redirect('/lager/lager/' + str(item.id) + '/')

    form.id = item.id
    return render(request, 'lager/lager_form.html', {'form': form})


# Liste der Lager
class LagersView(LoginRequiredMixin, ListView):
    model = Lager
    template_name = 'lager/lagers.html'
    context_object_name = 'lagers_list'

    def get_queryset(self):
        return Lager.objects.filter(weinkeller=str(self.request.user.id)).order_by('name')


# Delete Lager
class DeleteLagerItem(LoginRequiredMixin, DeleteView):
    model = Lager
    template_name = 'lager/lager_confirm_delete.html'

    def form_valid(self, form):
        success_url = "/lager/list/lager/"
        self.object = self.get_object()
        try:
            self.object.delete()
            return HttpResponseRedirect(success_url)
        except ProtectedError:
            self.object = self.get_object()
            context = self.get_context_data(
                object=self.object,
                error="Der Datensatz kann nicht gelöscht werden, da es noch Verknüpfungen zu anderen Datensätzen gibt"
            )
            return self.render_to_response(context)


# Anzeige einzelne Region
@login_required
def lager(request, id=id):
    try:
        lager_result = Lager.objects.get(id=id)
        return render(request, 'lager/lager.html', {'lager': lager_result})
    except ObjectDoesNotExist:
        return redirect('/lager/')


##########################################################################
# Area Bestand create and change
##########################################################################
# Bestand anlegen
@login_required
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


# Bestand editieren
@login_required
def edit_bestand(request, id=None):
    item = get_object_or_404(Bestand, id=id, weinkeller=request.user.id)
    form = BestandForm(request.POST or None, instance=item, user=request.user.id)
    # assert False
    if form.is_valid():
        form.save()
        return redirect('/lager/bestand/' + str(item.id) + '/')

    form.id = item.id
    return render(request, 'lager/bestand_form.html', {'form': form})

# Bestand drucken
@login_required
def print_bestand(request):
    item = Bestand.objects.filter(weinkeller=str(request.user.id)).order_by('lager', 'col_value', 'row_value')
    weinkeller = Weinkeller.objects.get(weinkeller_admin_id=str(request.user.id))

    fachmenge = {}
    lager = item[0].lager_id
    spalte = item[0].col_value
    reihe = item[0].row_value
    fachmenge2 = 0

    for x in item:
        #print("Lager: " + str(x.lager_id) + " Spalte: " + str(x.col_value) + "; Reihe: " + str(x.row_value) + " Menge: " + str(x.menge))
        if lager == x.lager_id:
            if spalte == x.col_value:
                if reihe == x.row_value:
                    fachmenge2 = fachmenge2 + x.menge
                    fachmenge[f"{x.lager_id}_{x.col_value}_{x.row_value}"] = fachmenge2
                else:
                    fachmenge2 = 0
                    fachmenge2 = fachmenge2 + x.menge
                    fachmenge[f"{x.lager_id}_{x.col_value}_{x.row_value}"] = fachmenge2
                    reihe = x.row_value
            else:
                fachmenge2 = 0
                fachmenge2 = fachmenge2 + x.menge
                fachmenge[f"{x.lager_id}_{x.col_value}_{x.row_value}"] = fachmenge2
                reihe = x.row_value
                spalte = x.col_value
        else:
            fachmenge2 = 0
            fachmenge2 = fachmenge2 + x.menge
            fachmenge[f"{x.lager_id}_{x.col_value}_{x.row_value}"] = fachmenge2
            reihe = x.row_value
            spalte = x.col_value
            lager = x.lager_id

        #print("Spalte: " + str(spalte))

        #print(x.menge)
        #print("Wert: " + str(fachmenge[f"{x.lager}_{x.col_value}_{x.row_value}"]))

    print(fachmenge)


    html_file = 'pdf_templates/report_bestand.html'
    css_file = '/lager/css/report_bestand.css'

    filename = "report_bestand.pdf"

    html_string = render_to_string(html_file, {'bestand': item, 'weinkeller': weinkeller, 'fachmenge': fachmenge})

    html = HTML(string=html_string, base_url=request.build_absolute_uri())
    logger.debug(f"User-ID: {request.user.id}; show_therapy_report CSS_File: {settings.STATIC_ROOT}{css_file}")
    pdf = html.write_pdf(stylesheets=[CSS(settings.STATIC_ROOT + css_file)])
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=' + filename

    return response

# Bestand drucken mit Reportlab
@login_required
def print_bestand2(request):
    # Daten ermitteln
    bestand = Bestand.objects.filter(weinkeller=str(request.user.id)).order_by('lager', 'col_value', 'row_value')
    weinkeller = Weinkeller.objects.get(weinkeller_admin_id=str(request.user.id))

    # Erstellen Sie einen dateiähnlichen Puffer, um PDF-Daten zu empfangen.
    buffer = io.BytesIO()

    # Erstellen Sie das PDF-Objekt, indem Sie den Puffer als "Datei" verwenden.
    p = canvas.Canvas(buffer, pagesize=A4)
    # Holen der Seitenabmessung
    breite, hoehe = A4

    p.drawString(1 * cm, 1 * cm, 'Der Text steht links unten')
    p.setFont('Helvetica-Bold', 18)
    p.drawCentredString(breite / 2, hoehe - (1 * cm), weinkeller.weinkeller)

    p.setFont('Helvetica-Bold', 14)
    p.drawCentredString(breite / 2, hoehe - (1.8 * cm), "Bestand am: " + str(datetime.date.today().strftime('%d.%m.%Y')))

    p.line(0.5 * cm, hoehe - (2.3 * cm), 20 * cm, hoehe - (2.3 * cm))  # Zeichne die Linie

    y = 750  # Starthöhe, kann angepasst werden
    max_y = 50  # Maximale Höhe auf der Seite
    p.setFont('Helvetica', 10)
    abstand = 0
    lager_nr = 0
    spalte_nr = -1
    reihe_nr = -1
    sum_menge = 0
    sum_gesamt = 0
    sum_fach = 0

    for item in bestand:
        if lager_nr == item.lager_id:
            if spalte_nr == item.col_value:
                if reihe_nr == item.row_value:
                    p.drawString(0.5 * cm, (hoehe - ((3 + abstand) * cm)),  str(item.wein))
                    p.drawString(16 * cm, (hoehe - ((3 + abstand) * cm)),  str(item.col_value))
                    p.drawString(17 * cm, (hoehe - ((3 + abstand) * cm)),  str(item.row_value))
                    p.drawRightString(19.5 * cm, (hoehe - ((3 + abstand) * cm)),  str(item.menge))
                    sum_menge = sum_menge + item.menge
                    sum_gesamt = sum_gesamt + item.menge
                    sum_fach = sum_fach + item.menge
                    abstand = abstand + 0.5
                else:
                    if reihe_nr > -1:
                        p.line(13 * cm, hoehe - ((2.63 + abstand) * cm), 20 * cm, hoehe - ((2.63 + abstand) * cm))
                        p.drawString(13 * cm, (hoehe - ((3 + abstand) * cm)), 'Bestand im Fach:')
                        p.drawRightString(19.5 * cm, (hoehe - ((3 + abstand) * cm)), str(sum_fach))
                        sum_fach = 0
                        abstand = abstand + 0.5
                    p.drawString(0.5 * cm, (hoehe - ((3 + abstand) * cm)), str(item.wein))
                    p.drawString(16 * cm, (hoehe - ((3 + abstand) * cm)), str(item.col_value))
                    p.drawString(17 * cm, (hoehe - ((3 + abstand) * cm)), str(item.row_value))
                    p.drawRightString(19.5 * cm, (hoehe - ((3 + abstand) * cm)), str(item.menge))
                    sum_menge = sum_menge + item.menge
                    sum_gesamt = sum_gesamt + item.menge
                    sum_fach = sum_fach + item.menge
                    abstand = abstand + 0.5
                    reihe_nr = item.row_value
            else:
                if spalte_nr > -1:
                    p.line(13 * cm, hoehe - ((2.63 + abstand) * cm), 20 * cm, hoehe - ((2.63 + abstand) * cm))
                    p.drawString(13 * cm, (hoehe - ((3 + abstand) * cm)), 'Bestand im Fach:')
                    p.drawRightString(19.5 * cm, (hoehe - ((3 + abstand) * cm)), str(sum_fach))
                    sum_fach = 0
                    abstand = abstand + 0.5
                p.drawString(0.5 * cm, (hoehe - ((3 + abstand) * cm)), str(item.wein))
                p.drawString(16 * cm, (hoehe - ((3 + abstand) * cm)), str(item.col_value))
                p.drawString(17 * cm, (hoehe - ((3 + abstand) * cm)), str(item.row_value))
                p.drawRightString(19.5 * cm, (hoehe - ((3 + abstand) * cm)), str(item.menge))
                sum_menge = sum_menge + item.menge
                sum_gesamt = sum_gesamt + item.menge
                sum_fach = sum_fach + item.menge
                abstand = abstand + 0.5
                spalte_nr = item.col_value
                reihe_nr = -1
        else:
            if lager_nr > 0:
                p.line(13 * cm, hoehe - ((2.63 + abstand) * cm), 20 * cm, hoehe - ((2.63 + abstand) * cm))
                p.drawString(13 * cm, (hoehe - ((3 + abstand) * cm)), 'Bestand im Fach:')
                p.drawRightString(19.5 * cm, (hoehe - ((3 + abstand) * cm)), str(sum_fach))
                abstand = abstand + 1.0
                p.line(13 * cm, hoehe - ((2.63 + abstand) * cm), 20 * cm, hoehe - ((2.63 + abstand) * cm))
                p.drawString(13 * cm, (hoehe - ((3 + abstand) * cm)), 'Bestand in Spalte:')
                p.drawRightString(19.5 * cm, (hoehe - ((3 + abstand) * cm)), str(sum_menge))
                sum_menge = 0
                sum_fach = 0
                abstand = abstand + 1.0

            # Hintergrundfarbe für das Rechteck
            background_color = colors.lightgrey

            # Zeichne ein Rechteck als Hintergrund
            p.setFillColor(background_color)
            p.rect(0.5 * cm, (hoehe - ((3 + abstand + 0.15) * cm)), 19.5 * cm, 18, fill=True)

            p.setFillColor(colors.black)  # Textfarbe
            p.setFont('Helvetica', 13)
            p.drawString(0.7 * cm, (hoehe - ((3 + abstand) * cm)),  str(item.lager))
            p.setFont('Helvetica', 10)
            p.drawString(15.55 * cm, (hoehe - ((3 + abstand) * cm)),  'Spalte')
            p.drawString(16.7 * cm, (hoehe - ((3 + abstand) * cm)),  'Reihe')
            p.drawString(18.7 * cm, (hoehe - ((3 + abstand) * cm)),  'Menge')
            lager_nr = item.lager_id
            abstand = abstand + 0.5
            p.setFont('Helvetica', 9)
            p.drawString(0.5 * cm, (hoehe - ((3 + abstand) * cm)),  str(item.wein))
            p.drawString(16 * cm, (hoehe - ((3 + abstand) * cm)),  str(item.col_value))
            p.drawString(17 * cm, (hoehe - ((3 + abstand) * cm)),  str(item.row_value))
            p.drawRightString(19.5 * cm, (hoehe - ((3 + abstand) * cm)),  str(item.menge))
            sum_menge = sum_menge + item.menge
            sum_gesamt = sum_gesamt + item.menge
            sum_fach = sum_fach + item.menge
            reihe_nr = item.row_value
            spalte_nr = item.col_value
            abstand = abstand + 0.5

    p.line(13 * cm, hoehe - ((2.63 + abstand) * cm), 20 * cm, hoehe - ((2.63 + abstand) * cm))
    p.drawString(13 * cm, (hoehe - ((3 + abstand) * cm)), 'Bestand im Fach:')
    p.drawRightString(19.5 * cm, (hoehe - ((3 + abstand) * cm)), str(sum_fach))
    abstand = abstand + 1.0
    p.line(13 * cm, hoehe - ((2.63 + abstand) * cm), 20 * cm, hoehe - ((2.63 + abstand) * cm))
    p.drawString(13 * cm, (hoehe - ((3 + abstand) * cm)), 'Bestand in Spalte:')
    p.drawRightString(19.5 * cm, (hoehe - ((3 + abstand) * cm)), str(sum_menge))
    abstand = abstand + 1.0
    p.line(13 * cm, hoehe - ((2.63 + abstand) * cm), 20 * cm, hoehe - ((2.63 + abstand) * cm))
    p.drawString(13 * cm, (hoehe - ((3 + abstand) * cm)), 'Gesamter Weinbestand:')
    p.drawRightString(19.5 * cm, (hoehe - ((3 + abstand) * cm)), str(sum_gesamt))


    # Schließen Sie das PDF-Objekt sauber, und wir sind fertig.
    p.showPage()
    p.save()

    # FileResponse setzt den Content-Disposition-Header so, dass Browser
    # präsentiert die Option zum Speichern der Datei.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=False, filename='hello.pdf')


# Liste der Weine
class BestandsView(LoginRequiredMixin, ListView):
    model = Bestand
    template_name = 'lager/bestands.html'
    context_object_name = 'bestands_list'

    def get_queryset(self):
        # return Bestand.objects.filter(weinkeller=str(self.request.user.id), menge__gt=0).order_by('wein')
        return Bestand.objects.filter(weinkeller=str(self.request.user.id)).order_by('wein')


# Delete Wein
class DeleteBestandItem(LoginRequiredMixin, DeleteView):
    model = Bestand
    template_name = 'lager/bestand_confirm_delete.html'

    def form_valid(self, form):
        success_url = "/lager/list/bestand/"
        self.object = self.get_object()
        try:
            self.object.delete()
            return HttpResponseRedirect(success_url)
        except ProtectedError:
            self.object = self.get_object()
            context = self.get_context_data(
                object=self.object,
                error="Der Datensatz kann nicht gelöscht werden, da es noch Verknüpfungen zu anderen Datensätzen gibt"
            )
            return self.render_to_response(context)


# Anzeige einzelne Region
@login_required
def bestand(request, id=id):
    try:
        bestand_result = Bestand.objects.get(id=id)
        return render(request, 'lager/bestand.html', {'bestand': bestand_result})
    except ObjectDoesNotExist:
        return redirect('/lager/')


##########################################################################
# Area Weinkeller create and change
##########################################################################
@login_required
def add_weinkeller(request):
    weinkeller_count = Weinkeller.objects.filter(weinkeller_admin_id=request.user.id).count()
    if weinkeller_count >= 1:
        return redirect('/lager/list/weine/')

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


# Weinkeller editieren
@login_required
def edit_weinkeller(request, id=None):
    item = get_object_or_404(Weinkeller, id=id, weinkeller_user_id=request.user.id)
    form = WeinkellerForm(request.POST or None, instance=item)
    # assert False
    if form.is_valid():
        form.save()
        return redirect('/lager/weinkeller/' + str(item.id) + '/')

    form.id = item.id
    return render(request, 'lager/weinkeller_form.html', {'form': form})


# Liste der Weinkeller
class WeinkellersView(LoginRequiredMixin, ListView):
    model = Weinkeller
    template_name = 'lager/weinkellers.html'
    context_object_name = 'weinkellers_list'

    def get_queryset(self):
        return Weinkeller.objects.filter(weinkeller_user_id=str(self.request.user.id))


# Anzeige einzelner Weinkeller
@login_required
def weinkeller(request, id=id):
    try:
        weinkeller_result = Weinkeller.objects.get(id=id)
        return render(request, 'lager/weinkeller.html', {'weinkeller': weinkeller_result})
    except ObjectDoesNotExist:
        return redirect('/lager/')


##########################################################################
# Wein erfassen Workflow
##########################################################################
@login_required
def wf_wein_initial(request):
    if 'weinland_id' in request.session:
        del request.session['weinland_id']
    if 'region_id' in request.session:
        del request.session['region_id']
    if 'lage' in request.session:
        del request.session['lage']
    if 'rebsorte_id' in request.session:
        del request.session['rebsorte_id']
    if 'cuvee_rebsorten' in request.session:
        del request.session['cuvee_rebsorten']
    if 'name' in request.session:
        del request.session['name']
    if 'weinart_id' in request.session:
        del request.session['weinart_id']
    if 'jahrgang_id' in request.session:
        del request.session['jahrgang_id']
    if 'geschmacksrichtung_id' in request.session:
        del request.session['geschmacksrichtung_id']
    if 'erzeuger_id' in request.session:
        del request.session['erzeuger_id']
    if 'bemerkung' in request.session:
        del request.session['bemerkung']
    if 'apnr' in request.session:
        del request.session['apnr']
    if 'flaschengroesse' in request.session:
        del request.session['flaschengroesse']
    if 'alkoholgehalt' in request.session:
        del request.session['alkoholgehalt']
    if 'vegan' in request.session:
        del request.session['vegan']
    if 'restzucker' in request.session:
        del request.session['restzucker']
    if 'literpreis' in request.session:
        del request.session['literpreis']
    if 'preis' in request.session:
        del request.session['preis']
    if 'bestellnummer' in request.session:
        del request.session['bestellnummer']
    if 'trinkbar_ab' in request.session:
        del request.session['trinkbar_ab']
    if 'restsaeure' in request.session:
        del request.session['restsaeure']

    return redirect('/lager/wf/wein/weinland/')


@login_required
def wf_wein_weinland(request):
    if request.method == "POST":
        request.session['weinland_id'] = request.POST['weinland']
        request.session['region_id'] = request.POST['region']
        request.session['lage'] = request.POST['lage']
        # print(request.session['weinland_id'] + "; " + request.session['region_id'] + "; " + request.session['lage'])
        return redirect('/lager/wf/wein/rebsorte/')

    if 'weinland_id' in request.session and 'region_id' in request.session and 'lage' in request.session:
        print("v1")
        form = WFWeinWeinlandForm(user_id=request.user.id, initial={
            'weinland': request.session['weinland_id'],
            'region': request.session['region_id'],
            'lage': request.session['lage']
        })
    elif 'weinland_id' in request.session and 'region_id' in request.session:
        print("v2")
        form = WFWeinWeinlandForm(user_id=request.user.id, initial={
            'weinland': request.session['weinland_id'],
            'region': request.session['region_id']
        })
    elif 'weinland_id' in request.session and 'lage' in request.session:
        form = WFWeinWeinlandForm(user_id=request.user.id, initial={
            'weinland': request.session['weinland_id'],
            'lage': request.session['lage']
        })
    elif 'weinland_id' in request.session:
        form = WFWeinWeinlandForm(user_id=request.user.id, initial={
            'weinland': request.session['weinland_id']
        })
    else:
        form = WFWeinWeinlandForm(user_id=request.user.id)

    return render(request, 'lager/wf_wein_weinland_form.html', {'form': form})


@login_required
def wf_wein_rebsorte(request):
    if request.method == "POST":
        request.session['rebsorte_id'] = request.POST['rebsorte']
        request.session['cuvee_rebsorten'] = request.POST['cuvee_rebsorten']
        return redirect('/lager/wf/wein/erzeuger/')

    if 'rebsorte_id' in request.session and 'cuvee_rebsorten' in request.session:
        form = WFWeinRebsorteForm(user_id=request.user.id, initial={
            'rebsorte': request.session['rebsorte_id'],
            'cuvee_rebsorten': request.session['cuvee_rebsorten']
        })
    elif 'rebsorte_id' in request.session:
        form = WFWeinRebsorteForm(user_id=request.user.id, initial={
            'rebsorte': request.session['rebsorte_id'],
        })
    else:
        form = WFWeinRebsorteForm(user_id=request.user.id)

    return render(request, 'lager/wf_wein_rebsorte_form.html', {'form': form})


@login_required
def wf_wein_erzeuger(request):
    if request.method == "POST":
        request.session['erzeuger_id'] = request.POST['erzeuger']
        return redirect('/lager/wf/wein/weinbasis/')

    if 'erzeuger_id' in request.session:
        form = WFWeinErzeugerForm(user_id=request.user.id, initial={
            'erzeuger': request.session['erzeuger_id']
        })
    else:
        form = WFWeinErzeugerForm(user_id=request.user.id)

    return render(request, 'lager/wf_wein_erzeuger_form.html', {'form': form})


@login_required
def wf_wein_basis(request):
    if request.method == "POST":
        request.session['name'] = request.POST['name']
        request.session['weinart_id'] = request.POST['weinart']
        request.session['jahrgang_id'] = request.POST['jahrgang']
        request.session['geschmacksrichtung_id'] = request.POST['geschmacksrichtung']
        request.session['bemerkung'] = request.POST['bemerkung']
        request.session['literpreis'] = request.POST['literpreis']
        request.session['preis'] = request.POST['preis']
        request.session['bestellnummer'] = request.POST['bestellnummer']
        request.session['trinkbar_ab'] = request.POST['trinkbar_ab']

        return redirect('/lager/wf/wein/weinzusatz/')

    if 'name' in request.session:
        form = WFWeinBasisForm(initial={
            'name': request.session['name'],
            'weinart': request.session['weinart_id'],
            'jahrgang': request.session['jahrgang_id'],
            'geschmacksrichtung': request.session['geschmacksrichtung_id'],
            'bemerkung': request.session['bemerkung'],
            'literpreis': request.session['literpreis'],
            'preis': request.session['preis'],
            'bestellnummer': request.session['bestellnummer'],
            'trinkbar_ab': request.session['trinkbar_ab']
        })
    else:
        form = WFWeinBasisForm()

    return render(request, 'lager/wf_wein_basis_form.html', {'form': form})


@login_required
def wf_wein_zusatz(request):
    if request.method == "POST":
        mydata = Weinkeller.objects.filter(weinkeller_user_id=request.user.id).values().first()
        form = WFWeinZusatzForm(request.POST)
        if form.is_valid():
            if request.POST['vegan'] == 'false':
                vegan_value = False
            elif request.POST['vegan'] == 'true':
                vegan_value = True
            else:
                vegan_value = True
            #assert False
            wein2save = Wein(
                name=request.session['name'],
                region_id=request.session['region_id'],
                weinland_id=request.session['weinland_id'],
                rebsorte_id=request.session['rebsorte_id'],
                cuvee_rebsorten=request.session['cuvee_rebsorten'],
                weinart_id=request.session['weinart_id'],
                jahrgang_id=request.session['jahrgang_id'],
                geschmacksrichtung_id=request.session['geschmacksrichtung_id'],
                erzeuger_id=request.session['erzeuger_id'],
                bemerkung=request.session['bemerkung'],
                weinkeller=mydata['weinkeller_admin_id'],
                apnr=request.POST['apnr'],
                flaschengroesse=request.POST['flaschengroesse'],
                alkoholgehalt=request.POST['alkoholgehalt'],
                vegan=vegan_value,
                restzucker=request.POST['restzucker'],
                literpreis=request.session['literpreis'],
                preis=request.session['preis'],
                bestellnummer=request.session['bestellnummer'],
                trinkbar_ab=request.session['trinkbar_ab'],
                lage=request.session['lage'],
                restsaeure=request.POST['restsaeure']
                )
            wein2save.save()

            return redirect('/lager/list/weine/')
        else:
            print('NotValid')

    form = WFWeinZusatzForm()

    return render(request, 'lager/wf_wein_zusatz_form.html', {'form': form})


##########################################################################
# AJAX Functions
##########################################################################
# AJAX
@login_required
def ajax_load_regions(request):
    weinland_id = request.GET.get('weinland_id')
    regionen = Region.objects.filter(weinland_id=weinland_id).all().order_by('region')
    return render(request, 'lager/region_dropdown_list_options.html', {'regionen': regionen})
    # return JsonResponse(list(cities.values('id', 'name')), safe=False)


@login_required
def ajax_load_lagers(request):
    lager_id = request.GET.get('lager_id')
    lager_parameter = Lager.objects.filter(id=lager_id).values().first()
    return render(request, 'lager/lager_parameter.html', {'lager_parameter': lager_parameter})
