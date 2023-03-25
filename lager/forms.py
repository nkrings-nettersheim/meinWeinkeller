from django import forms

from .models import Weinland, Region, Rebsorte, Wein, Jahrgang


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

    weinland = forms.ModelChoiceField(queryset=Weinland.objects.all().order_by('land'))

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

    jahrgang = forms.ModelChoiceField(queryset=Jahrgang.objects.all().order_by('-jahrgang'))

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


