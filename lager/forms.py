from django import forms
import datetime
# from datetime import datetime, today, timedelta

from .models import Weinland, Region, Rebsorte, Wein, Jahrgang, Erzeuger, Geschmacksrichtung, Weinart, \
    LagerTyp, Lager, Bestand, Weinkeller


class WeinlandForm(forms.ModelForm):
    land = forms.CharField(required=True,
                           max_length=50,
                           widget=forms.TextInput(
                               attrs={
                                   'class': 'form-control',
                                   'autofocus': 'autofocus',
                                   'placeholder': 'Land eingeben ...'
                               }
                           )
                           )

    KONTINENTE = (
        ('Afrika', 'Afrika'),
        ('Asien', 'Asien'),
        ('Australien', 'Australien'),
        ('Europa', 'Europa'),
        ('Nord-Amerika', 'Nord-Amerika'),
        ('Süd-Amerika', 'Süd-Amerika'),
        ('Ozeanien', 'Ozeanien')
    )
    kontinent = forms.ChoiceField(
        required=True,
        choices=KONTINENTE,
        label="",
        initial=4,
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            }
        )
    )

    bemerkung = forms.CharField(required=False,
                                widget=forms.Textarea(
                                    attrs={
                                        'class': 'form-control',
                                        'placeholder': 'Bemerkungen ...'
                                    }
                                )
                                )

    class Meta:
        model = Weinland
        fields = ['land',
                  'kontinent',
                  'weinkeller',
                  'bemerkung'
                  ]


class RegionForm(forms.ModelForm):
    region = forms.CharField(required=True,
                             max_length=50,
                             widget=forms.TextInput(
                                 attrs={
                                     'class': 'form-control',
                                     'autofocus': 'autofocus',
                                     'placeholder': 'Region eingeben ...'
                                 }
                             )
                             )

    class Meta:
        model = Region
        fields = [
            'region',
            'weinland',
            'weinkeller'
        ]

    def __init__(self, *args, **kwargs):
        user_id = kwargs.pop('user')
        super(RegionForm, self).__init__(*args, **kwargs)
        self.fields['weinland'] = forms.ModelChoiceField(
            queryset=Weinland.objects.filter(weinkeller=user_id).order_by('land'), required=False,
            widget=forms.Select(
                attrs={
                    'class': 'form-control',
                }
            ),
            empty_label='Wähle das Land aus ...'
        )


class RebsorteForm(forms.ModelForm):
    rebsorte = forms.CharField(
        required=True,
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'autofocus': 'autofocus',
                'placeholder': 'Rebsorte eingeben ...'
            }
        )
    )

    rebsorte_alias = forms.CharField(
        required=False,
        max_length=250,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'autofocus': 'autofocus',
                'placeholder': 'mögliche Alias-Namen eingeben ...'
            }
        )
    )

    class Meta:
        model = Rebsorte
        fields = [
            'rebsorte',
            'rebsorte_alias',
            'weinkeller'
        ]


class WeinForm(forms.ModelForm):
    name = forms.CharField(required=True,
                           max_length=50,
                           widget=forms.TextInput(
                               attrs={
                                   'class': 'form-control',
                                   'autofocus': 'autofocus',
                                   'placeholder': 'Name des Weins eingeben ...'
                               }
                           )
                           )

    weinart = forms.ModelChoiceField(queryset=Weinart.objects.all().order_by('weinart'),
                                     widget=forms.Select(
                                         attrs={
                                             'class': 'form-control',
                                         }
                                     ),
                                     empty_label='Wähle die Weinart aus'
                                     )

    geschmacksrichtung = forms.ModelChoiceField(
        queryset=Geschmacksrichtung.objects.all().order_by('geschmacksrichtung'),
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        ),
        empty_label='Wähle die Geschmacksrichtung aus'
    )

    date = datetime.date.today()
    start_year = date - datetime.timedelta(days=18250)
    current_year = date.strftime("%Y")
    start_year = start_year.strftime("%Y")

    jahrgang = forms.ModelChoiceField(
        queryset=Jahrgang.objects.filter(jahrgang_num__range=(start_year, current_year)).order_by('-jahrgang'),
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        ),
        empty_label='Wähle den Jahrgang aus'
    )

    bemerkung = forms.CharField(required=False,
                                widget=forms.Textarea(
                                    attrs={
                                        'class': 'form-control',
                                        'placeholder': 'Bemerkungen ...'
                                    }
                                )
                                )

    class Meta:
        model = Wein
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        user_id = kwargs.pop('user')
        super(WeinForm, self).__init__(*args, **kwargs)
        self.fields['weinland'] = forms.ModelChoiceField(
            queryset=Weinland.objects.filter(weinkeller=user_id).order_by('land'), required=False,
            widget=forms.Select(
                attrs={
                    'class': 'form-control',
                }
            ),
            empty_label='Wähle das Land aus ...'
        )

        self.fields['rebsorte'] = forms.ModelChoiceField(
            queryset=Rebsorte.objects.filter(weinkeller=user_id).order_by('rebsorte'), required=False,
            widget=forms.Select(
                attrs={
                    'class': 'form-control',
                }
            ),
            empty_label='Wähle die Rebsorte aus ...'
        )

        self.fields['region'] = forms.ModelChoiceField(
            queryset=Region.objects.filter(weinkeller=user_id).order_by('region'), required=False,
            widget=forms.Select(
                attrs={
                    'class': 'form-control',
                }
            ),
            empty_label='Wähle die Region aus ...'
        )

        self.fields['erzeuger'] = forms.ModelChoiceField(
            queryset=Erzeuger.objects.filter(weinkeller=user_id).order_by('name'), required=False,
            widget=forms.Select(
                attrs={
                    'class': 'form-control',
                }
            ),
            empty_label='Wähle den Erzeuger aus ...'
        )

        if 'weinland' in self.data:
            try:
                weinland_id = int(self.data.get('weinland'))
                # self.fields['region'].queryset = Region.objects.filter(weinland_id=weinland_id, weinkeller=user_id).order_by('region')
                self.fields['region'] = forms.ModelChoiceField(
                    queryset=Region.objects.filter(weinland_id=weinland_id, weinkeller=user_id).order_by('region'),
                    required=False,
                    widget=forms.Select(
                        attrs={
                            'class': 'form-control',
                        }
                    )
                )
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Weinland queryset
        elif self.instance.pk:
            self.fields['region'].queryset = self.instance.weinland.region_set.order_by('region')


class ErzeugerForm(forms.ModelForm):
    name = forms.CharField(required=True,
                           max_length=50,
                           widget=forms.TextInput(
                               attrs={
                                   'class': 'form-control',
                                   'autofocus': 'autofocus',
                                   'placeholder': 'Name des Erzeugers eingeben ...'
                               }
                           )
                           )

    inhaber = forms.CharField(required=False,
                              max_length=50,
                              widget=forms.TextInput(
                                  attrs={
                                      'class': 'form-control',
                                      'autofocus': 'autofocus',
                                      'placeholder': 'Name des Inhabers eingeben ...'
                                  }
                              )
                              )

    strasse = forms.CharField(required=False,
                              max_length=50,
                              widget=forms.TextInput(
                                  attrs={
                                      'class': 'form-control',
                                      'autofocus': 'autofocus',
                                      'placeholder': 'Strasse/Hausnummer eingeben ...'
                                  }
                              )
                              )

    plz = forms.CharField(required=False,
                          max_length=10,
                          widget=forms.TextInput(
                              attrs={
                                  'class': 'form-control',
                                  'autofocus': 'autofocus',
                                  'placeholder': 'PLZ eingeben ...'
                              }
                          )
                          )

    ort = forms.CharField(required=False,
                          max_length=50,
                          widget=forms.TextInput(
                              attrs={
                                  'class': 'form-control',
                                  'autofocus': 'autofocus',
                                  'placeholder': 'Ort eingeben ...'
                              }
                          )
                          )

    telefon = forms.CharField(required=False,
                              max_length=50,
                              widget=forms.TextInput(
                                  attrs={
                                      'class': 'form-control',
                                      'autofocus': 'autofocus',
                                      'placeholder': 'Telefon eingeben ...'
                                  }
                              )
                              )

    email = forms.EmailField(required=False,
                             max_length=254,
                             widget=forms.EmailInput(
                                 attrs={
                                     'class': 'form-control',
                                     'placeholder': 'E-Mail Adresse eingeben ...'
                                 }
                             )
                             )

    ansprechpartner = forms.CharField(required=False,
                                      max_length=50,
                                      widget=forms.TextInput(
                                          attrs={
                                              'class': 'form-control',
                                              'autofocus': 'autofocus',
                                              'placeholder': 'Ansprechpartner eingeben ...'
                                          }
                                      )
                                      )

    asp_telefon = forms.CharField(required=False,
                                  max_length=20,
                                  widget=forms.TextInput(
                                      attrs={
                                          'class': 'form-control',
                                          'autofocus': 'autofocus',
                                          'placeholder': 'Telefon des Ansprechpartners eingeben ...'
                                      }
                                  )
                                  )

    asp_email = forms.EmailField(required=False,
                                 max_length=254,
                                 widget=forms.EmailInput(
                                     attrs={
                                         'class': 'form-control',
                                         'placeholder': 'E-Mail Adresse des Ansprechpartners eingeben ...'
                                     }
                                 )
                                 )

    website = forms.URLField(required=False,
                             max_length=254,
                             widget=forms.URLInput(
                                 attrs={
                                     'class': 'form-control',
                                     'placeholder': 'Website eingeben ...'
                                 }
                             )
                             )

    class Meta:
        model = Erzeuger
        fields = [
            'name',
            'inhaber',
            'strasse',
            'plz',
            'ort',
            'land',
            'telefon',
            'email',
            'ansprechpartner',
            'asp_telefon',
            'asp_email',
            'website',
            'weinkeller'
        ]

    def __init__(self, *args, **kwargs):
        user_id = kwargs.pop('user')
        super(ErzeugerForm, self).__init__(*args, **kwargs)
        self.fields['land'] = forms.ModelChoiceField(
            queryset=Weinland.objects.filter(weinkeller=user_id), required=False,
            widget=forms.Select(
                attrs={
                    'class': 'form-control',
                }
            ),
            empty_label='Wähle das Land aus ...'
        )


class LagerForm(forms.ModelForm):
    name = forms.CharField(required=True,
                           max_length=100,
                           widget=forms.TextInput(
                               attrs={
                                   'class': 'form-control',
                                   'autofocus': 'autofocus',
                                   'placeholder': 'Vergebe einen sprechenden Namen ...'
                               }
                           )
                           )

    typ = forms.ModelChoiceField(queryset=LagerTyp.objects.all().order_by('typ'),
                                 widget=forms.Select(
                                     attrs={
                                         'class': 'form-control',
                                     }
                                 ),
                                 empty_label='Wähle den Regaltyp aus'
                                 )

    cols = forms.IntegerField(widget=forms.NumberInput(
        attrs={
            'class': 'form-control',
        }
    ))

    rows = forms.IntegerField(widget=forms.NumberInput(
        attrs={
            'class': 'form-control',
        }
    ))

    max_kapa = forms.IntegerField(widget=forms.NumberInput(
        attrs={
            'class': 'form-control',
        }
    ))

    links_rechts = forms.NullBooleanField(required=False, initial='',
                                          widget=forms.NullBooleanSelect(
                                              attrs={
                                                  'class': 'form-control',
                                              }
                                          ))

    oben_unten = forms.NullBooleanField(required=False, initial='',
                                        widget=forms.NullBooleanSelect(
                                            attrs={
                                                'class': 'form-control',
                                            }
                                        ))

    vorne_hinten = forms.NullBooleanField(required=False, initial='',
                                          widget=forms.NullBooleanSelect(
                                              attrs={
                                                  'class': 'form-control',
                                              }
                                          ))

    class Meta:
        model = Lager
        fields = '__all__'


class BestandForm(forms.ModelForm):
    col_value = forms.IntegerField(
        initial=1,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            }
        ))

    row_value = forms.IntegerField(
        initial=1,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            }
        ))

    rechts = forms.NullBooleanField(
        required=False,
        initial='',
        widget=forms.NullBooleanSelect(
            attrs={
                'class': 'form-control',
            }
        ))

    links = forms.NullBooleanField(
        required=False,
        initial='',
        widget=forms.NullBooleanSelect(
            attrs={
                'class': 'form-control',
            }
        ))

    oben = forms.NullBooleanField(
        required=False,
        initial='',
        widget=forms.NullBooleanSelect(
            attrs={
                'class': 'form-control',
            }
        ))

    unten = forms.NullBooleanField(
        required=False,
        initial='',
        widget=forms.NullBooleanSelect(
            attrs={
                'class': 'form-control',
            }
        ))

    hinten = forms.NullBooleanField(
        required=False,
        initial='',
        widget=forms.NullBooleanSelect(
            attrs={
                'class': 'form-control',
            }
        ))

    vorne = forms.NullBooleanField(
        required=False,
        initial='',
        widget=forms.NullBooleanSelect(
            attrs={
                'class': 'form-control',
            }
        ))

    menge = forms.IntegerField(
        initial=1,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            }
        ))

    class Meta:
        model = Bestand
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        user_id = kwargs.pop('user')
        super(BestandForm, self).__init__(*args, **kwargs)
        self.fields['wein'] = forms.ModelChoiceField(
            queryset=Wein.objects.filter(weinkeller=user_id).order_by('name'), required=True,
            widget=forms.Select(
                attrs={
                    'class': 'form-control',
                }
            ),
            empty_label='Wähle den Wein aus ...'
        )

        self.fields['lager'] = forms.ModelChoiceField(
            queryset=Lager.objects.filter(weinkeller=user_id).order_by('name'), required=True,
            widget=forms.Select(
                attrs={
                    'class': 'form-control',
                }
            ),
            empty_label='Wähle den Lagerort aus ...'
        )


class WeinkellerForm(forms.ModelForm):
    weinkeller = forms.CharField(required=True,
                                 max_length=100,
                                 widget=forms.TextInput(
                                     attrs={
                                         'class': 'form-control',
                                         'autofocus': 'autofocus',
                                         'placeholder': 'Wähle einen schönen Namen für deinen Weinkeller ...'
                                     }
                                 )
                                 )

    class Meta:
        model = Weinkeller
        fields = [
            'weinkeller',
            'weinkeller_admin_id',
            'weinkeller_user_id',
        ]
