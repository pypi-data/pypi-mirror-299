from netbox.search import SearchIndex, register_search

from .models import *


@register_search
class VoiceSdaSearchIndex(SearchIndex):
    model = VoiceSda
    fields = (
        ('start', 100),
        ('end', 100),
    )


@register_search
class VoiceDeliverySearchIndex(SearchIndex):
    model = VoiceDelivery
    fields = (
        ('delivery', 100),
        ('provider', 100),
        ('site', 500),
    )


@register_search
class VoiceMaintainerSearchIndex(SearchIndex):
    model = VoiceMaintainer
    fields = (
        ('name', 100),
        ('slug', 100),
        ('description', 500),
        ('comments', 1000),
        ('status', 1000),
    )
