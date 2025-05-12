from django import forms
from .models import ObjetDefectueux

class ObjetDefectueuxForm(forms.ModelForm):
    class Meta:
        model = ObjetDefectueux
        fields = ['nom_produit', 'status', 'description', 'image_url']