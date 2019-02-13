from django.contrib import admin
from django.contrib.admin import register

from mail.forms import MailboxForm
from mail.models import Domain, Mailbox, TLSPolicy, Alias, AliasDomain


@register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'mailboxes', 'aliases', 'active']


# @register(AliasDomain)
# class AliasDomainAdmin(admin.ModelAdmin):
#     list_display = ['name', 'target', 'description', 'active']


@register(Mailbox)
class MailboxAdmin(admin.ModelAdmin):
    form = MailboxForm


@register(Alias)
class AliasAdmin(admin.ModelAdmin):
    list_display = ['name', 'domain', 'target', 'active']


@register(TLSPolicy)
class TLSPolicyAdmin(admin.ModelAdmin):
    list_display = ['domain', 'policy', 'params']
