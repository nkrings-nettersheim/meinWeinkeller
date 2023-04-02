from django.contrib import admin

from .models import Weinland, Region, Jahrgang, Geschmacksrichtung, Rebsorte, Weinart, Erzeuger, Wein, \
    Qualitaetsstufe, LagerTyp, Lager, Bestand


admin.site.site_header = "Admin Bereich 'Mein Weinkeller'"

admin.site.register(Weinland)
admin.site.register(Region)
admin.site.register(Jahrgang)
admin.site.register(Geschmacksrichtung)
admin.site.register(Rebsorte)
admin.site.register(Weinart)
admin.site.register(Erzeuger)
admin.site.register(Wein)
admin.site.register(Qualitaetsstufe)
admin.site.register(LagerTyp)
admin.site.register(Lager)
admin.site.register(Bestand)
