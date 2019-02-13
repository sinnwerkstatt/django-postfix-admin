from django.views.generic import TemplateView

from mail.mixins import AdminRequiredMixin
from mail.utils import Database


class Index(AdminRequiredMixin, TemplateView):
    template_name = 'mail/index.html'

    def get_context_data(self, **kwargs):
        ctx = super(Index, self).get_context_data(**kwargs)
        db = Database()
        ctx['dovecot'] = db.dovecot_sql_conf()
        ctx['postfix'] = db.postfix_sql_conf()
        ctx['driver'] = db.driver
        return ctx
