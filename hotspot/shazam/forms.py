from django import forms

class WifoForm(forms.Form):
    FormControlArtiste = forms.CharField(label="Votre Artiste", max_length=100)
    FormControlTitre = forms.CharField(label="Votre Titre", max_length=100)