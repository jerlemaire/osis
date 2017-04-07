from django import forms

from internship.models.internship import Internship


class InternshipOfferImportForm(forms.Form):
    file = forms.FileField()
    internship = forms.ModelChoiceField(queryset=Internship.objects.all())

    def __init__(self, *args, **kwargs):
        super(forms.Form, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
            })

