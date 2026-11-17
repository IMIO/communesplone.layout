"""@@login and @@login_form: maintenance message when source_users is deactivated."""

from communesplone.layout.browser.login import LoginForm
from communesplone.layout.interfaces import ICommunesploneLayoutLayer
from communesplone.layout.testing import INTEGRATION
from plone.app.testing import logout
from Products.PluggableAuthService.interfaces.plugins import IAuthenticationPlugin
from zope.interface import noLongerProvides

import unittest


class TestLoginForm(unittest.TestCase):

    layer = INTEGRATION

    def setUp(self):
        self.portal = self.layer["portal"]
        logout()

    def test_render(self):
        for name in ("@@login", "@@login_form"):
            view = self.portal.restrictedTraverse(name)
            self.assertIsInstance(view, LoginForm)
            html = view()
            self.assertIn('id="__ac_password"', html)
            self.assertIn('href="http://nohost/plone/@@login-help"', html)
            self.assertNotIn("no_plugin", html)
        # maintenance: a message instead of the login form
        self.portal.acl_users.plugins.deactivatePlugin(
            IAuthenticationPlugin, "source_users"
        )
        for name in ("@@login", "@@login_form"):
            html = self.portal.restrictedTraverse(name)()
            self.assertIn('<p id="no_plugin" style="font-weight:bold;">', html)
            self.assertIn(
                "The connection to the site is temporary suspended for maintenance operations.",
                html,
            )
            self.assertIn(
                '<a href="contact-info">Contact the site administrator</a>', html
            )
            self.assertNotIn("__ac_password", html)
            self.assertNotIn("@@login-help", html)
        # Plone's login form without the browser layer (package not installed)
        noLongerProvides(self.layer["request"], ICommunesploneLayoutLayer)
        self.assertNotIsInstance(self.portal.restrictedTraverse("@@login"), LoginForm)
