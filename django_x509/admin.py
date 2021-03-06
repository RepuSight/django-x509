from django.contrib import admin
from django.contrib.admin import ModelAdmin as BaseAdmin
from django.contrib.admin.templatetags.admin_static import static
from django.core.urlresolvers import reverse
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _

from .models import Ca, Cert


class AbstractAdmin(BaseAdmin):
    """
    ModelAdmin for TimeStampedEditableModel
    """
    list_display = ['name',
                    'key_length',
                    'digest',
                    'created',
                    'modified']
    search_fields = ('name', 'serial_number', 'common_name')
    actions_on_bottom = True
    save_on_top = True
    # custom attribute
    readonly_edit = ('key_length',
                     'digest',
                     'validity_start',
                     'validity_end',
                     'country_code',
                     'state',
                     'city',
                     'organization',
                     'email',
                     'common_name',
                     'serial_number',
                     'certificate',
                     'private_key')

    class Media:
        css = {'all': (static('django-x509/css/admin.css'),)}

    def __init__(self, *args, **kwargs):
        self.readonly_fields += ('created', 'modified')
        super(AbstractAdmin, self).__init__(*args, **kwargs)

    def get_readonly_fields(self, request, obj=None):
        # edit
        if obj:
            return self.readonly_edit + self.readonly_fields
        # add
        else:
            return self.readonly_fields

    def get_fields(self, request, obj=None):
        fields = super(AbstractAdmin, self).get_fields(request, obj)
        # edit
        if obj and 'extensions' in fields:
            fields.remove('extensions')
        return fields


class CaAdmin(AbstractAdmin):
    list_filter = ('key_length', 'digest', 'created',)


class CertAdmin(AbstractAdmin):
    list_filter = ('ca', 'revoked', 'key_length', 'digest', 'created',)
    list_select_related = ('ca',)
    readonly_fields = ('revoked', 'revoked_at',)
    fields = ['name',
              'ca',
              'notes',
              'revoked',
              'revoked_at',
              'key_length',
              'digest',
              'validity_start',
              'validity_end',
              'country_code',
              'state',
              'city',
              'organization',
              'email',
              'common_name',
              'extensions',
              'serial_number',
              'certificate',
              'private_key',
              'created',
              'modified']
    actions = ['revoke_action']

    def ca_url(self, obj):
        url = reverse('admin:django_x509_ca_change', args=[obj.ca.id])
        return format_html("<a href='{url}'>{text}</a>",
                           url=url,
                           text=obj.ca.name)
    ca_url.short_description = 'CA'

    def revoke_action(self, request, queryset):
        rows = 0
        for cert in queryset:
            cert.revoke()
            rows += 1
        if rows == 1:
            bit = '1 certificate was'
        else:
            bit = '{0} certificates were'.format(rows)
        message = '{0} revoked.'.format(bit)
        self.message_user(request, _(message))

    revoke_action.short_description = _('Revoke selected certificates')


CertAdmin.list_display = AbstractAdmin.list_display[:]
CertAdmin.list_display.insert(1, 'ca_url')
CertAdmin.list_display.insert(4, 'serial_number')
CertAdmin.list_display.insert(5, 'revoked')
CertAdmin.readonly_edit = AbstractAdmin.readonly_edit[:]
CertAdmin.readonly_edit += ('ca',)

admin.site.register(Ca, CaAdmin)
admin.site.register(Cert, CertAdmin)
