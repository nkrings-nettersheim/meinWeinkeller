from django.db import models


class Weinland(models.Model):
    kontinent = models.CharField(max_length=50, blank=False)
    land = models.CharField(max_length=50, blank=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return self.land


class Region(models.Model):
    region = models.CharField(max_length=50, blank=False, unique=True)
    weinland = models.ForeignKey(Weinland, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return self.region


class Jahrgang(models.Model):
    jahrgang = models.CharField(max_length=4, blank=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return self.jahrgang


class Geschmacksrichtung(models.Model):
    geschmacksrichtung = models.CharField(max_length=20, blank=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return self.geschmacksrichtung


class Rebsorte(models.Model):
    rebsorte = models.CharField(max_length=50, blank=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return self.rebsorte


class Weinart(models.Model):
    weinart = models.CharField(max_length=10, blank=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return self.weinart


class Qualitaetsstufe(models.Model):
    qualitaetsstufe = models.CharField(max_length=50, blank=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return self.qualitaetsstufe


class Erzeuger(models.Model):
    name = models.CharField(max_length=50, blank=False, unique=True)
    inhaber = models.CharField(max_length=50, blank=True, default='')
    strasse = models.CharField(max_length=50, blank=True, default='')
    plz = models.CharField(max_length=10, blank=True, default='')
    ort = models.CharField(max_length=50, blank=True, default='')
    land = models.CharField(max_length=50, blank=True, default='')
    telefon = models.CharField(max_length=20, blank=True, default='')
    email = models.EmailField(max_length=254, blank=True)
    ansprechpartner = models.CharField(max_length=50, blank=True, default='')
    asp_telefon = models.CharField(max_length=20, blank=True, default='')
    asp_email = models.EmailField(max_length=254, blank=True)

    def __str__(self):
        return self.name


class Wein(models.Model):
    name = models.CharField(max_length=100, blank=False, unique=True)
    weinland = models.ForeignKey(Weinland, on_delete=models.PROTECT, blank=True, null=True)
    region = models.ForeignKey(Region, on_delete=models.PROTECT, blank=True, null=True)
    rebsorte = models.ForeignKey(Rebsorte, on_delete=models.PROTECT, blank=True, null=True)
    weinart = models.ForeignKey(Weinart, on_delete=models.PROTECT, blank=True, null=True)
    jahrgang = models.ForeignKey(Jahrgang, on_delete=models.PROTECT, blank=True, null=True)
    geschmacksrichtung = models.ForeignKey(Geschmacksrichtung, on_delete=models.PROTECT, blank=True, null=True)
    erzeuger = models.ForeignKey(Erzeuger, on_delete=models.PROTECT, blank=True, null=True)
    bemerkung = models.TextField()

    def __str__(self):
        return self.name




