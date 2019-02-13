from django.contrib import admin
from django.contrib.admin import register

from mail.forms import MailboxForm
from mail.models import Domain, Mailbox, TLSPolicy, Alias


@register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'mailboxes', 'aliases', 'active']


# @register(AliasDomain)
# class AliasDomainAdmin(admin.ModelAdmin):
#     list_display = ['name', 'target', 'description', 'active']


@register(Mailbox)
class MailboxAdmin(admin.ModelAdmin):
    form = MailboxForm
    list_display = ['__str__', 'get_aliases']

    def get_aliases(self, obj):
        aliases = Alias.objects.filter(targets__icontains=f"{obj.name}@{obj.domain_id}")
        return [f"{alias.name}@{alias.domain_id}" for alias in aliases]

    get_aliases.short_description = 'Aliases'


@register(Alias)
class AliasAdmin(admin.ModelAdmin):
    list_display = ['name', 'domain', 'targets', 'active']


@register(TLSPolicy)
class TLSPolicyAdmin(admin.ModelAdmin):
    list_display = ['domain', 'policy', 'params']
