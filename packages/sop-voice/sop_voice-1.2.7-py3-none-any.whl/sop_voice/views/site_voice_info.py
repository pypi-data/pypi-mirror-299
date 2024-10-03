from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404

from netbox.views import generic
from dcim.models import Site

from ..utils import count_all_sda_list
from ..forms.site_voice_info import *
from ..models import SiteVoiceInfo, VoiceSda


__all__ = (
    'SiteVoiceInfoEditView',
    'SiteVoiceInfoDeleteView',
    'SiteVoiceInfoDetailView'
)


class SiteVoiceInfoDetailView(generic.ObjectView):
    queryset = SiteVoiceInfo.objects.all()
    
    def get_extra_context(self, request, instance) -> dict:
        context:dict = {}
        
        sda_list = VoiceSda.objects.filter(site=get_object_or_404(Site, pk=instance.site.id))
        temp: tuple[int, int] = count_all_sda_list(sda_list).__int__()
        context['num_sda'] = temp[0]
        context['num_range'] = temp[1]
        return context


class SiteVoiceInfoEditView(generic.ObjectEditView):
    queryset = SiteVoiceInfo.objects.all()
    form = SiteVoiceInfoForm

    def get_return_url(self, request, obj=None):
        try:
            return '/dcim/sites/' + str(obj.site.pk) + '/voice/'
        except:
            return '/dcim/sites/'


class SiteVoiceInfoDeleteView(generic.ObjectDeleteView):
    queryset = SiteVoiceInfo.objects.all()

    def get_return_url(self, request, obj=None) -> str:
        try:
            if obj is None:
                raise Exception
            return f'/dcim/sites/{obj.site.pk}/voice'
        except:
            return '/dcim/sites/'
