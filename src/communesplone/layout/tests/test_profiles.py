"""GenericSetup profiles default, uninstall and simplify."""

from communesplone.layout.interfaces import ICommunesploneLayoutLayer
from communesplone.layout.testing import EDITOR
from communesplone.layout.testing import INTEGRATION
from communesplone.layout.testing import SIMPLIFY_INTEGRATION
from communesplone.layout.testing import SITE_ADMIN
from plone.app.testing import login
from plone.app.testing import logout
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.base.interfaces import IBundleRegistry
from plone.base.utils import get_installer
from plone.browserlayer.utils import registered_layers
from plone.registry.interfaces import IRegistry
from Products.CMFCore.Expression import Expression
from Products.CMFPlone.resources.utils import evaluateExpression
from Products.CMFPlone.resources.utils import get_resource
from zope.component import getUtility

import unittest


BUNDLE = "plone.bundles/communesplone-layout-simplify"
SIMPLIFY_EXPRESSION = (
    "python: not portal.portal_membership.isAnonymousUser() and not context.portal_membership.getAuthenticatedMember()"
    ".has_role('Manager') and not 'full-layout' in context.portal_membership.getAuthenticatedMember().getGroups()"
)


class TestDefaultProfile(unittest.TestCase):

    layer = INTEGRATION

    def setUp(self):
        self.portal = self.layer["portal"]
        self.installer = get_installer(self.portal, self.layer["request"])

    def test_install(self):
        self.assertTrue(self.installer.is_product_installed("communesplone.layout"))
        self.assertEqual(
            self.portal.portal_setup.getLastVersionForProfile(
                "communesplone.layout:default"
            ),
            ("4381",),
        )
        self.assertIn(ICommunesploneLayoutLayer, registered_layers())

    def test_uninstall(self):
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.installer.uninstall_product("communesplone.layout")
        self.assertFalse(self.installer.is_product_installed("communesplone.layout"))
        self.assertNotIn(ICommunesploneLayoutLayer, registered_layers())


class TestSimplifyProfile(unittest.TestCase):

    layer = SIMPLIFY_INTEGRATION

    def setUp(self):
        self.portal = self.layer["portal"]
        self.bundle = getUtility(IRegistry).forInterface(IBundleRegistry, prefix=BUNDLE)

    def simplify_css_shown(self):
        """simplify.css is in the page for the current user."""
        return evaluateExpression(
            Expression(self.bundle.expression), self.portal.folder.doc
        )

    def test_install(self):
        self.assertTrue(self.bundle.enabled)
        self.assertEqual(
            self.bundle.csscompilation, "++plone++communesplone.layout/simplify.css"
        )
        self.assertIn(
            b"#plone-contentmenu-actions",
            get_resource(self.portal, self.bundle.csscompilation),
        )
        self.assertEqual(self.bundle.expression, SIMPLIFY_EXPRESSION)
        # shown to the authenticated users outside full-layout, except Managers
        logout()
        self.assertFalse(self.simplify_css_shown())
        login(self.portal, EDITOR)
        self.assertTrue(self.simplify_css_shown())
        login(
            self.portal, SITE_ADMIN
        )  # member of full-layout through the Site Administrators group
        self.assertFalse(self.simplify_css_shown())
        login(self.portal, TEST_USER_NAME)
        self.assertTrue(self.simplify_css_shown())
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.assertFalse(self.simplify_css_shown())
        setRoles(self.portal, TEST_USER_ID, ["Member"])
        self.portal.portal_groups.addPrincipalToGroup(EDITOR, "full-layout")
        login(self.portal, EDITOR)
        self.assertFalse(self.simplify_css_shown())
