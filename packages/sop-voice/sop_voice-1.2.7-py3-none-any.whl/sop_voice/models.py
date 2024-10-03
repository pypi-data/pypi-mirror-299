from django.db import models
from django.db.models import Transform
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from netbox.models import NetBoxModel
from circuits.models import Provider
from dcim.models import Site
from utilities.choices import ChoiceSet

from .validators import VoiceValidator, number_quicksearch



__all__ = (
    'VoiceSda',
    'VoiceDelivery',
    'SiteVoiceInfo',
    'VoiceMaintainer',
    'VoiceMaintainerStatusChoice',
    'VoiceDeliveryStatusChoices',
    'SopBoolChoices',
    'AbsoluteValue',
    'FloorValue',
    'LogValue'
)


class VoiceMaintainerStatusChoice(ChoiceSet):

    CHOICES = (
        ('active', _('Active'), 'green'),
        ('retired', _('Retired'), 'red'),
        ('unknown', _('Unknown'), 'gray'),
    )


class VoiceDeliveryStatusChoices(ChoiceSet):

    CHOICES = (
        ('active', _('Active'), 'green'),
        ('planned', _('Planned'), 'cyan'),
        ('staging', _('Staging'), 'blue'),
        ('retired', _('Retired'), 'red'),
        ('unknown', _('Unknown'), 'gray'),
    )


class SopBoolChoices(ChoiceSet):

    CHOICES = (
        ('unknown', _('Unknown'), 'gray'),
        ('true', _('True'), 'green'),
        ('false', _('False'), 'red'),
    )


class AbsoluteValue(Transform):
    lookup_name = "abs"
    function = "ABS"
    bilateral = True

class FloorValue(Transform):
    lookup_name = "floor"
    function = "FLOOR"
    bilateral = True

class LogValue(Transform):
    lookup_name = "log"
    function = "LOG"
    bilateral = True

models.IntegerField.register_lookup(AbsoluteValue)
models.IntegerField.register_lookup(FloorValue)
models.IntegerField.register_lookup(LogValue)



class VoiceMaintainer(NetBoxModel):
    name = models.CharField(
        verbose_name=_('Maintainer'),
    )
    slug = models.SlugField(
        verbose_name=_('slug'),
        max_length=100,
        unique=True,
        blank=True,
    )
    status = models.CharField(
        max_length=30,
        choices=VoiceMaintainerStatusChoice,
        default="Unknown",
        verbose_name=_('Status')
    )
    description = models.CharField(
        verbose_name=_('description'),
        max_length=200,
        blank=True
    )
    comments = models.TextField(
        verbose_name=_('comments'),
        blank=True
    )

    def __str__(self) -> str:
        return f'{self.name}'

    def get_absolute_url(self) -> str:
        return reverse('plugins:sop_voice:voicemaintainer_detail', args=[self.pk])

    def get_status_color(self) -> str:
        return VoiceDeliveryStatusChoices.colors.get(self.status)

    class Meta(NetBoxModel.Meta):
        verbose_name = _('Voice Maintainer')
        verbose_name_plural = _('Voice Maintainers')
        constraints = (
            models.UniqueConstraint(
                fields=('name',),
                name='%(app_label)s_%(class)s_unique_name',
                violation_error_message=_("Maintainer name must be unique.")
            ),
            models.UniqueConstraint(
                fields=('slug',),
                name='%(app_label)s_%(class)s_unique_slug',
                violation_error_message=_("Maintainer slug must be unique.")
            )
        )

    def clean(self):
        super().clean()
        
        if self.name and VoiceMaintainer.objects.filter(name=self.name).exists():
            raise ValidationError({
                'name': _(f'A "{self.name}" maintainer already exists.')
            })


class SiteVoiceInfo(NetBoxModel):
    site = models.OneToOneField(
        Site,
        on_delete=models.CASCADE,
        verbose_name=_('Site'),
    )
    maintainer = models.ForeignKey(
        VoiceMaintainer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Maintainer'),
    )

    def __str__(self) -> str:
        return f'{self.site} voice maintainer'

    def get_absolute_url(self) -> str:
        return reverse('plugins:sop_voice:sitevoiceinfo_detail', args=[self.pk])

    class Meta(NetBoxModel.Meta):
        verbose_name = _('Information')
        verbose_name_plural = _('Informations')
        constraints = [
            models.UniqueConstraint(
                fields=['site',],
                name='%(app_label)s_%(class)s_unique_site',
                violation_error_message=_("Site must be unique.")
            )
        ]


class VoiceDelivery(NetBoxModel):
    delivery = models.CharField(
        verbose_name=_('Delivery'),
    )
    provider = models.ForeignKey(
        Provider,
        on_delete=models.CASCADE,
        verbose_name=_('Provider'),
    )
    site = models.ForeignKey(
        Site,
        on_delete=models.CASCADE,
        verbose_name=_('Site'),
    )
    channel_count = models.PositiveBigIntegerField(
        verbose_name=_('Channel Count'),
        null=True,
        blank=True,
    )
    status = models.CharField(
        max_length=30,
        choices=VoiceDeliveryStatusChoices,
        verbose_name=_('Status'),
    )
    ndi = models.PositiveBigIntegerField(
        verbose_name=_('NDI'),
        null=True,
        blank=True,
    )
    dto = models.PositiveBigIntegerField(
        verbose_name=_('DTO'),
        null=True,
        blank=True,
    )
    description = models.CharField(
        verbose_name=_('description'),
        max_length=200,
        blank=True
    )
    comments = models.TextField(
        verbose_name=_('comments'),
        blank=True
    )

    def get_absolute_url(self) -> str:
        return reverse('plugins:sop_voice:voicedelivery_detail', args=[self.pk])

    def get_status_color(self) -> str:
        return VoiceDeliveryStatusChoices.colors.get(self.status)

    def __str__(self) -> str:
        delivery:str = self.delivery if self.delivery is not None else 'Unknown delivery'
        provider:str = self.provider if self.provider is not None else 'Unknown provider'

        return f'{delivery} / {provider}'

    def clean(self):
        super().clean()
        if self.delivery and self.site:
            if VoiceDelivery.objects.filter(site=self.site, delivery=self.delivery).exists():
                raise ValidationError({
                    'delivery': _(f'A "{self.delivery}" delivery method already exists for this site.')
                })
        if self.ndi:
            VoiceValidator.check_number('ndi', self.ndi)
            if VoiceDelivery.objects.filter(ndi=self.ndi).exists():
                raise ValidationError({
                    'ndi': _(f'This NDI already exists on another delivery.')
                })


    class Meta(NetBoxModel.Meta):
        verbose_name = _('Voice Delivery')
        verbose_name_plural = _('Voice Deliveries')
        constraints = (
            models.UniqueConstraint(
                fields=('ndi',),
                name='%(app_label)s_%(class)s_unique_ndi',
                violation_error_message=_("NDI must be unique.")
            ),
            models.UniqueConstraint(
                fields=('delivery', 'site'),
                name='%(app_label)s_%(class)s_unique_delivery_method_site',
                violation_error_message=_("Delivery method must be unique in a site.")
            )
        )


class VoiceSda(NetBoxModel):
    delivery = models.ForeignKey(
        VoiceDelivery,
        on_delete=models.SET_NULL,
        verbose_name=_('Delivery'),
        null=True,
        blank=True,
    )
    site = models.ForeignKey(
        Site,
        on_delete=models.CASCADE,
        verbose_name=_('Site'),
        null=False,
        blank=True,
    )
    start = models.PositiveBigIntegerField(
        unique=False,
        verbose_name=_('Start number'),
        null=False,
        blank=True,
    )
    end = models.PositiveBigIntegerField(
        unique=False,
        verbose_name=_('End number'),
        null=False,
        blank=True,
    )

    def __str__(self) -> str:
        return f'"{self.start} >> {self.end}"'

    def get_absolute_url(self) -> str:
        return reverse('plugins:sop_voice:voicesda_detail', args=[self.pk])

    def clean(self):
        super().clean()

        VoiceValidator.check_delivery(self.delivery, self.site)

        VoiceValidator.check_number('start', self.start)
        if self.end is None:
            self.end=self.start
        else :
            VoiceValidator.check_number('end', self.end)
            VoiceValidator.check_start_end(self.start, self.end)  

        '''
        check if self.end or self.start overlaps an existing DID range
        '''
        lnum=len(str(self.start))
        for rng in VoiceSda.objects.all():
            #only compare if numbers are comaprable (have the same length)
            if len(str(rng.start))==lnum:
                # check if number overlap
                if self.start <= rng.end and rng.start <= self.end:
                    raise ValidationError({
                        'start': _(f'This range {self.start} -> {self.end} overlaps range {rng.start} -> {rng.end}.')
                    })

    def save(self, *args, **kwargs):
        if not self.end or self.end == 0:
            self.end = self.start
        super().save(*args, **kwargs)

    class Meta(NetBoxModel.Meta):
        ordering = ('start',)
        verbose_name = _('DID Range')
        verbose_name_plural = _('DIDs')

        constraints = (
            models.UniqueConstraint(
                fields=('start',),
                name='%(app_label)s_%(class)s_unique_start_number',
                violation_error_message=_("Start number must be unique.")
            ),
            models.UniqueConstraint(
                fields=('end',),
                name='%(app_label)s_%(class)s_unique_end_number',
                violation_error_message=_("End number must be unique.")
            ),
            models.CheckConstraint(
                check=models.Q(end__gte=models.F('start')) & \
                    models.Q(start__abs__log__floor=models.F("end")),
                name='%(app_label)s_%(class)s_end_greater_than_start',
                violation_error_message=_("End number must be greater than or equal to start number.")
            )
        )
