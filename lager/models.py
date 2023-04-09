from django.db import models


class Weinkeller(models.Model):
    weinkeller = models.CharField(max_length=100, blank=False)
    weinkeller_admin_id = models.IntegerField(default=0)
    weinkeller_user_id = models.IntegerField(default=0)

    def __str__(self):
        return self.weinkeller


class Weinland(models.Model):
    kontinent = models.CharField(max_length=50, blank=False)
    land = models.CharField(max_length=50, blank=False)
    weinkeller = models.IntegerField(default=0)
    bemerkung = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return self.land

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['land', 'weinkeller'], name='unique land_weinkeller'),
        ]


class Region(models.Model):
    region = models.CharField(max_length=50, blank=False)
    weinland = models.ForeignKey(Weinland, on_delete=models.CASCADE)
    weinkeller = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return self.region

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['region', 'weinkeller'], name='unique region_weinkeller'),
        ]


class Jahrgang(models.Model):
    jahrgang = models.CharField(max_length=4, blank=False, unique=True)
    jahrgang_num = models.IntegerField(default=2000, blank=True)
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
    rebsorte = models.CharField(max_length=50, blank=False)
    rebsorte_alias = models.CharField(max_length=250, blank=False, default='')
    weinkeller = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return self.rebsorte

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['rebsorte', 'weinkeller'], name='unique rebsorte_weinkeller'),
        ]


class Weinart(models.Model):
    weinart = models.CharField(max_length=20, blank=False, unique=True)
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
    name = models.CharField(max_length=50, blank=False)
    inhaber = models.CharField(max_length=50, blank=True, default='')
    strasse = models.CharField(max_length=50, blank=True, default='')
    plz = models.CharField(max_length=10, blank=True, default='')
    ort = models.CharField(max_length=50, blank=True, default='')
    land = models.ForeignKey(Weinland, default=1, on_delete=models.PROTECT, blank=True, null=True)
    telefon = models.CharField(max_length=20, blank=True, default='')
    email = models.EmailField(max_length=254, blank=True)
    ansprechpartner = models.CharField(max_length=50, blank=True, default='')
    asp_telefon = models.CharField(max_length=20, blank=True, default='')
    asp_email = models.EmailField(max_length=254, blank=True)
    weinkeller = models.IntegerField(default=0)
    website = models.URLField(default='', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'weinkeller'], name='unique name_erzeuger_weinkeller'),
        ]


class Wein(models.Model):
    name = models.CharField(max_length=100, blank=False)
    weinland = models.ForeignKey(Weinland, on_delete=models.PROTECT, blank=True, null=True)
    region = models.ForeignKey(Region, on_delete=models.PROTECT, blank=True, null=True)
    rebsorte = models.ForeignKey(Rebsorte, on_delete=models.PROTECT, blank=True, null=True)
    weinart = models.ForeignKey(Weinart, on_delete=models.PROTECT, blank=True, null=True)
    jahrgang = models.ForeignKey(Jahrgang, on_delete=models.PROTECT, blank=True, null=True)
    geschmacksrichtung = models.ForeignKey(Geschmacksrichtung, on_delete=models.PROTECT, blank=True, null=True)
    erzeuger = models.ForeignKey(Erzeuger, on_delete=models.PROTECT, blank=True, null=True)
    bemerkung = models.TextField()
    weinkeller = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'jahrgang', 'weinkeller'], name='unique name_wein_weinkeller'),
        ]


class LagerTyp(models.Model):
    typ = models.CharField(max_length=20, blank=False, unique=True)

    def __str__(self):
        return self.typ


class Lager(models.Model):
    name = models.CharField(max_length=100, blank=False)
    typ = models.ForeignKey(LagerTyp, on_delete=models.PROTECT, blank=True, null=True)
    cols = models.IntegerField(default=1)
    rows = models.IntegerField(default=1)
    max_kapa = models.IntegerField(default=1)
    links_rechts = models.BooleanField(default=False, null=True)
    oben_unten = models.BooleanField(default=False, null=True)
    vorne_hinten = models.BooleanField(default=False, null=True)
    weinkeller = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'weinkeller'], name='unique name_lager_weinkeller'),
        ]


class Bestand(models.Model):
    wein = models.ForeignKey(Wein, on_delete=models.PROTECT, blank=True, null=True)
    lager = models.ForeignKey(Lager, on_delete=models.PROTECT, blank=True, null=True)
    row_value = models.IntegerField(default=1)
    col_value = models.IntegerField(default=1)
    links = models.BooleanField(default=False, null=True)
    rechts = models.BooleanField(default=False, null=True)
    oben = models.BooleanField(default=False, null=True)
    unten = models.BooleanField(default=False, null=True)
    vorne = models.BooleanField(default=False, null=True)
    hinten = models.BooleanField(default=False, null=True)
    menge = models.IntegerField(default=0)
    weinkeller = models.IntegerField(default=0)

    def __str__(self):
        return self.wein




