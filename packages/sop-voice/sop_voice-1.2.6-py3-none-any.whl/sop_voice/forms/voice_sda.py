from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from netbox.forms import NetBoxModelFilterSetForm, NetBoxModelBulkEditForm, NetBoxModelForm, NetBoxModelImportForm
from utilities.forms.fields import DynamicModelChoiceField, DynamicModelChoiceField, CSVModelChoiceField
from dcim.models import Site

from ..models import *


__all__ = (
    'VoiceSdaForm',
    'VoiceSdaFilterForm',
    'VoiceSdaBulkEditForm',
    'VoiceSdaBulkImportForm',
)


class VoiceSdaBulkEditForm(NetBoxModelBulkEditForm):
    model = VoiceSda

    site = DynamicModelChoiceField(
        queryset=Site.objects.all()
    )
    delivery = DynamicModelChoiceField(
        queryset=VoiceDelivery.objects.all(),
        help_text=_('Specify how this range is delivered.'),
        query_params={
            'site_id': '$site'
        }
    )

    class Meta:
        fields = ('site', 'delivery', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'add_tags' in self.fields:
            del self.fields['add_tags']
        if 'remove_tags' in self.fields:
            del self.fields['remove_tags']


class VoiceSdaFilterForm(NetBoxModelFilterSetForm):
    model = VoiceSda
    
    site_id = DynamicModelChoiceField(
        queryset=Site.objects.all(),
        required=False,
        label=_('Site')
    )
    maintainer_id = forms.ModelChoiceField(
        queryset=VoiceMaintainer.objects.all(),
        required=False,
        label=_('Maintainer')
    )
    delivery_id = forms.ModelChoiceField(
        queryset=VoiceDelivery.objects.all(),
        required=False,
        label=_('Delivery')
    )
    partial_number = forms.IntegerField(
        label=_('Partial number'),
        required=False
    )
    start = forms.IntegerField(
        label=_('Start number'),
        required=False,
        help_text=_('E164 format'),
    )
    end = forms.IntegerField(
        label=_('End number'),
        required=False,
        help_text=_('E164 format')
    )

    def clean(self):
        super().clean()
        if self.cleaned_data and self.cleaned_data['partial_number']:
            if not isinstance(self.cleaned_data.get('partial_number'), int):
                raise ValidationError({'partial_number': _('Partial number must be a number')})


class VoiceSdaForm(NetBoxModelForm):

    site = DynamicModelChoiceField(
        label=_('Site'),
        queryset=Site.objects.all(),
        required=True,
    )
    start = forms.IntegerField(
        label=_('Start number'),
        required=True,
        help_text=_('E164 format / NUMBER ONLY'),
    )
    end = forms.IntegerField(
        label=_('End number'),
        required=False,
        help_text=_('E164 format - can be left blank if the range is only one number. / NUMBER ONLY'),
    )
    delivery = DynamicModelChoiceField(
        label=_('Delivery'),
        queryset=VoiceDelivery.objects.all(),
        required=False,
        help_text=_('Specify how this range is delivered.'),
        query_params={
            'site_id': '$site'
        }
    )

    class Meta:
        model = VoiceSda
        fields = ('site', 'start', 'end', 'delivery')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'tags' in self.fields:
            del self.fields['tags']

    def clean(self):

        super().clean()


class VoiceSdaBulkImportForm(NetBoxModelImportForm):
    delivery = CSVModelChoiceField(
        queryset=VoiceDelivery.objects.all(),
        to_field_name='id',
        required=False,
    )
    site = CSVModelChoiceField(
        queryset=Site.objects.all(),
        to_field_name='slug',
        required=True,
    )
    start = forms.IntegerField(
        label=_('Start number'),
        help_text='E164 format',
        required=True
    )
    end = forms.IntegerField(
        label=_('End number'),
        help_text='E164 format - can be left blank if the range is only one number.',
        required=False
    )

    class Meta:
        model = VoiceSda
        fields = ['delivery', 'site', 'start', 'end']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'tags' in self.fields:
            del self.fields['tags']

    def clean(self):
        super().clean()
        if not self.cleaned_data.get('end'):
            self.cleaned_data['end'] = self.cleaned_data['start']
