from django import forms

from .models import Weinland, Region, Rebsorte, Wein, Jahrgang, Erzeuger, Geschmacksrichtung, Weinart


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
        ('Süd-Amerika', 'Süd-Amerika')
    )
    kontinent = forms.ChoiceField(choices=KONTINENTE, label="", initial=4, widget=forms.Select(
        attrs={
            'class': 'form-control'
        }
    ))

    class Meta:
        model = Weinland
        fields = ['land',
                  'kontinent'
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

    weinland = forms.ModelChoiceField(queryset=Weinland.objects.all().order_by('land'),
                                      widget=forms.Select(
                                          attrs={
                                              'class': 'form-control',
                                          }
                                      ),
                                      empty_label='Wähle das Weinland aus')

    class Meta:
        model = Region
        fields = [
            'region',
            'weinland'
        ]


class RebsorteForm(forms.ModelForm):
    rebsorte = forms.CharField(required=True,
                               max_length=50,
                               widget=forms.TextInput(
                                   attrs={
                                       'class': 'form-control',
                                       'autofocus': 'autofocus',
                                       'placeholder': 'Rebsorte eingeben ...'
                                   }
                               )
                               )

    class Meta:
        model = Rebsorte
        fields = [
            'rebsorte'
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

    weinland = forms.ModelChoiceField(queryset=Weinland.objects.all().order_by('kontinent', 'land'),
                                      widget=forms.Select(
                                          attrs={
                                              'class': 'form-control',
                                          }
                                      ),
                                      empty_label='Wähle das Herkunftsland aus'
                                      )

    region = forms.ModelChoiceField(queryset=Region.objects.all().order_by('region'),
                                    widget=forms.Select(
                                        attrs={
                                            'class': 'form-control',
                                        }
                                    ),
                                    empty_label='Wähle die Region aus'
                                    )

    rebsorte = forms.ModelChoiceField(queryset=Rebsorte.objects.all().order_by('rebsorte'),
                                      widget=forms.Select(
                                          attrs={
                                              'class': 'form-control',
                                          }
                                      ),
                                      empty_label='Wähle die Reborte aus'
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

    erzeuger = forms.ModelChoiceField(queryset=Erzeuger.objects.all().order_by('name'),
                                      widget=forms.Select(
                                          attrs={
                                              'class': 'form-control',
                                          }
                                      ),
                                      empty_label='Wer ist der Erzeuger?'
                                      )

    jahrgang = forms.ModelChoiceField(queryset=Jahrgang.objects.all().order_by('-jahrgang'),
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
            super().__init__(*args, **kwargs)
            self.fields['region'].queryset = Region.objects.none()

            if 'weinland' in self.data:
                try:
                    weinland_id = int(self.data.get('weinland'))
                    self.fields['region'].queryset = Region.objects.filter(weinland_id=weinland_id).order_by('region')
                except (ValueError, TypeError):
                    pass  # invalid input from the client; ignore and fallback to empty City queryset
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

    land = forms.CharField(required=False,
                           max_length=50,
                           widget=forms.TextInput(
                               attrs={
                                   'class': 'form-control',
                                   'autofocus': 'autofocus',
                                   'placeholder': 'Land eingeben ...'
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

    class Meta:
        model = Erzeuger
        fields = '__all__'

