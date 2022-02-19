from django import forms
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Comics, Images


class AtLeastOneFormSet(BaseInlineFormSet):

    def clean(self):
        super(AtLeastOneFormSet, self).clean()
        non_empty_forms = 0
        for form in self:
            if form.cleaned_data:
                non_empty_forms += 1
        if non_empty_forms - len(self.deleted_forms) < 1:
            raise ValidationError("Please fill at least one form.")


class AddComicsForm(forms.ModelForm):

    class Meta:
        model = Comics
        fields = ['title', 'description', 'is_complete', 'preview_image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter title'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'is_complete': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'preview_image': forms.FileInput(attrs={'class': 'form-control-file', 'id': 'input-id'})
        }
