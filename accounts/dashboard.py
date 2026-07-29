from django.utils.translation import gettext_lazy as _
from grappelli.dashboard import Dashboard, modules


class CustomIndexDashboard(Dashboard):
    def init_with_context(self, context):
        self.children.append(modules.AppList(
            title=_('Applications'),
            models=('accounts.*', 'animals.*', 'feeding.*', 'dashboard.*'),
        ))
        self.children.append(modules.RecentActions(
            title=_('Recent Actions'),
            limit=10,
        ))
