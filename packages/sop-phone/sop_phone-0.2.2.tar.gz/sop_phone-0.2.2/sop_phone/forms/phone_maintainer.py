from django import forms
from django.utils.translation import gettext_lazy as _

from utilities.forms.fields import CommentField, SlugField, CSVChoiceField
from netbox.forms import NetBoxModelFilterSetForm, NetBoxModelForm, NetBoxModelBulkEditForm, NetBoxModelImportForm

from ..models import *


__all__ = (
    'PhoneMaintainerForm',
    'PhoneMaintainerFilterForm',
    'PhoneMaintainerBulkEditForm',
    'PhoneMaintainerBulkImportForm',
)


class PhoneMaintainerFilterForm(NetBoxModelFilterSetForm):
    model = PhoneMaintainer
    status = forms.ChoiceField(
        choices=PhoneMaintainerStatusChoice,
        required=False,
        label=_('Status'),
    )


class PhoneMaintainerBulkEditForm(NetBoxModelBulkEditForm):
    model = PhoneMaintainer
    status = forms.ChoiceField(
        choices=PhoneMaintainerStatusChoice,
        required=True,
    )

    class Meta:
        fields = ('status', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'add_tags' in self.fields:
            del self.fields['add_tags']
        if 'remove_tags' in self.fields:
            del self.fields['remove_tags']


class PhoneMaintainerForm(NetBoxModelForm):
    name = forms.CharField(label=_('Maintainer'))
    slug = SlugField()
    status = forms.ChoiceField(
        choices=PhoneMaintainerStatusChoice,
        required=True
    )
    comments = CommentField()

    class Meta:
        model = PhoneMaintainer
        fields = ('name', 'slug', 'status', 'description', 'comments')


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'tags' in self.fields:
            del self.fields['tags']


class PhoneMaintainerBulkImportForm(NetBoxModelImportForm):
    status = CSVChoiceField(
        choices=PhoneMaintainerStatusChoice,
        required=True,
    )
    slug = SlugField(required=True)

    class Meta:
        model = PhoneMaintainer
        fields = ['name', 'slug', 'status', 'description',]

    def clean(self):
        super().clean()
