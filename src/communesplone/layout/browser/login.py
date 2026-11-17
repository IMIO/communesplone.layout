from Products.CMFPlone.browser.login import login
from Products.CMFPlone.browser.login.login import LoginForm as BaseLoginForm
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.PluggableAuthService.interfaces.plugins import IAuthenticationPlugin

import os


class LoginForm(BaseLoginForm):
    """Plone's login form, or a maintenance message when source_users is deactivated."""

    index = ViewPageTemplateFile(
        "templates/login.pt", _prefix=os.path.dirname(login.__file__)
    )
    maintenance = ViewPageTemplateFile("maintenance.pt")

    def render(self):
        plugins = self.context.acl_users.plugins.listPlugins(IAuthenticationPlugin)
        if "source_users" not in [plugin_id for plugin_id, plugin in plugins]:
            return self.maintenance()
        return super().render()
