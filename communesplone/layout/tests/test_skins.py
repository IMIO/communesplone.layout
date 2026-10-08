# -*- coding: utf-8 -*-
"""Skin layer communesplone_layout: login form and send-to form."""
from communesplone.layout.testing import HAS_CAPTCHA
from communesplone.layout.testing import INTEGRATION
from plone.app.testing import login
from plone.app.testing import logout
from plone.app.testing import TEST_USER_NAME
from Products.PluggableAuthService.interfaces.plugins import IAuthenticationPlugin

import unittest


CAPTCHA_ERROR = "Please provide the message here above correctly, case sensitive."
CAPTCHA_COOKIE = "captchasessionid"  # collective.captcha.browser.captcha.COOKIE_ID


class SkinsTestCase(unittest.TestCase):

    layer = INTEGRATION

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        self.doc = self.portal.folder.doc

    def deactivate_source_users(self):
        self.portal.acl_users.plugins.deactivatePlugin(
            IAuthenticationPlugin, "source_users"
        )


class TestCheckActivatedPlugins(SkinsTestCase):

    def test_checkActivatedPlugins(self):
        logout()  # called by the login form of anonymous users
        plugins = self.portal.restrictedTraverse("checkActivatedPlugins")()
        self.assertIn("source_users", plugins)
        self.deactivate_source_users()
        plugins = self.portal.restrictedTraverse("checkActivatedPlugins")()
        self.assertNotIn("source_users", plugins)
        self.assertIn("session", plugins)


class TestLoginForm(SkinsTestCase):

    def test_login_form(self):
        logout()
        html = self.portal.restrictedTraverse("login_form")()
        self.assertIn('id="login_form" action="http://nohost/plone/login_form"', html)
        self.assertIn('id="__ac_password"', html)
        self.assertIn('id="login-forgotten-password"', html)
        self.assertNotIn("no_plugin", html)
        # maintenance: a message instead of the login form
        self.deactivate_source_users()
        html = self.portal.restrictedTraverse("login_form")()
        self.assertIn('<p id="no_plugin" style="font-weight:bold;">', html)
        self.assertIn(
            "The connection to the site is temporary suspended for maintenance operations.",
            html,
        )
        self.assertIn('<a href="contact-info">Contact the site administrator</a>', html)
        self.assertNotIn('id="login_form"', html)
        self.assertNotIn("__ac_password", html)
        self.assertNotIn("login-forgotten-password", html)


@unittest.skipUnless(HAS_CAPTCHA, "collective.captcha is not installed")
class TestSendtoForm(SkinsTestCase):

    def test_sendto_form(self):
        login(self.portal, TEST_USER_NAME)
        html = self.doc.restrictedTraverse("sendto_form")()
        self.assertIn('<label for="captcha">Captcha</label>', html)
        self.assertIn('<input type="text" name="captcha" />', html)
        self.assertIn(
            '<img src="http://nohost/plone/folder/doc/@@captcha/image" />', html
        )
        self.assertNotIn(CAPTCHA_ERROR, html)
        # a wrong captcha shows the form again with the error
        self.request.form.update(
            {
                "form.submitted": "1",
                "send_to_address": "to@example.com",
                "send_from_address": "from@example.com",
                "captcha": "WRONG",
            }
        )
        html = self.doc.restrictedTraverse("sendto_form")()
        self.assertIn("<div>{}</div>".format(CAPTCHA_ERROR), html)
        self.assertIn('<input type="text" name="captcha" />', html)


@unittest.skipUnless(HAS_CAPTCHA, "collective.captcha is not installed")
class TestValidateSendto(SkinsTestCase):

    def validate(self, captcha):
        """Runs validate_sendto as the form controller does on submit."""
        controller = self.portal.portal_form_controller
        form = {
            "send_to_address": "to@example.com",
            "send_from_address": "from@example.com",
            "captcha": captcha,
            "controller_state": None,
        }
        for key, value in form.items():
            self.request.set(
                key, value
            )  # request.get() caches the form values in request.other
        state = controller.getState(self.doc.sendto_form, is_validator=0)
        return controller.validate(state, self.request, ["validate_sendto"])

    def test_validate_sendto(self):
        login(self.portal, TEST_USER_NAME)
        self.request.cookies[CAPTCHA_COOKIE] = (
            "session-id"  # set when the captcha image is shown
        )
        word = self.doc.restrictedTraverse("@@captcha")._generate()  # text of the image
        state = self.validate("WRONG")
        self.assertEqual(state.getStatus(), "failure")
        self.assertEqual(state.getErrors(), {"captcha": CAPTCHA_ERROR})
        state = self.validate(word.lower())  # case insensitive, despite the message
        self.assertEqual(state.getStatus(), "success")
        self.assertEqual(state.getErrors(), {})
