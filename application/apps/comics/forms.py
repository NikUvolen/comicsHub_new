from django import forms
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from comics.models import Comics, Images


class AtLeastOneFormSet(BaseInlineFormSet):

    def clean(self):
        super(AtLeastOneFormSet, self).clean()
        non_empty_forms = 0
        for form in self:
            if form.cleaned_data:
                non_empty_forms += 1
        if non_empty_forms - len(self.deleted_forms) < 1:
            raise ValidationError("Please fill at least one form.")


# class AddComicsInlineFormSet(BaseInlineFormSet):
#
class AddComicsForm(forms.ModelForm):

    class Meta:
        model = Comics
        fields = ['title', 'description', 'is_complete', 'preview_image']
        widgets = {
            'title': forms.TextInput(),
            'description': forms.Textarea(),
            'is_complete': forms.CheckboxInput(),
            'preview_image': forms.FileInput()
        }


# class AddComicsImages(forms.Form):
#
#     image = forms.ImageField(required=True)
#
#     def clean_images(self):

