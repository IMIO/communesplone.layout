# -*- coding: utf-8 -*-
"""GenericSetup profiles default and simplify."""
from Acquisition import aq_base
from communesplone.layout.testing import EDITOR
from communesplone.layout.testing import INTEGRATION
from communesplone.layout.testing import SIMPLIFY_INTEGRATION
from communesplone.layout.testing import SITE_ADMIN
from plone.app.testing import login
from plone.app.testing import logout
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME

import unittest


SKIN_OBJECTS = ('checkActivatedPlugins', 'login_form', 'sendto_form', 'validate_sendto')
SIMPLIFY_EXPRESSION = (
    "python: not portal.portal_membership.isAnonymousUser() and not context.portal_membership.getAuthenticatedMember()"
    ".has_role('Manager') and not 'full-layout' in context.portal_membership.getAuthenticatedMember().getGroups()")


class ProfileTestCase(unittest.TestCase):

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.skins = self.portal.portal_skins

    def skin_paths(self):
        return [self.skins.getSkinPath(name).split(',') for name in self.skins.getSkinSelections()]

    def skin_object(self, name):
        """Object found by the skin lookup of a new request."""
        self.portal.clearCurrentSkin()
        self.portal.setupCurrentSkin(self.request)
        return aq_base(getattr(self.portal, name))


class TestDefaultProfile(ProfileTestCase):

    layer = INTEGRATION

    def test_install(self):
        self.assertEqual(self.portal.portal_setup.getLastVersionForProfile('communesplone.layout:default'), ('4381', ))
        self.assertEqual(self.skins.communesplone_layout.getDirPath(), 'communesplone.layout:skins/communesplone_layout')
        self.assertEqual(len(self.skin_paths()), 2)  # Plone Default, Sunburst Theme
        for path in self.skin_paths():
            self.assertEqual(path[:2], ['custom', 'communesplone_layout'])
        for name in SKIN_OBJECTS:
            self.assertIs(self.skin_object(name), aq_base(self.skins.communesplone_layout[name]))

    def test_uninstall(self):
        qi = self.portal.portal_quickinstaller
        self.assertTrue(qi.isProductInstalled('communesplone.layout'))
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        qi.uninstallProducts(['communesplone.layout'])
        self.assertFalse(qi.isProductInstalled('communesplone.layout'))
        self.assertNotIn('communesplone_layout', self.skins.objectIds())
        # the layer name stays in the skin paths (harmless: a missing layer is skipped)
        for path in self.skin_paths():
            self.assertEqual(path[:2], ['custom', 'communesplone_layout'])
        self.assertIs(self.skin_object('login_form'), aq_base(self.skins.plone_login.login_form))
        self.assertIs(self.skin_object('sendto_form'), aq_base(self.skins.plone_forms.sendto_form))
        self.assertFalse(hasattr(self.portal, 'checkActivatedPlugins'))


class TestSimplifyProfile(ProfileTestCase):

    layer = SIMPLIFY_INTEGRATION

    def simplify_css_shown(self):
        """simplify.css is in the page for the current user."""
        css = self.portal.portal_css
        return css.evaluate(css.getResource('simplify.css'), self.portal.folder.doc)

    def test_install(self):
        self.assertEqual(self.skins.communesplone_layout_simplify.getDirPath(),
                         'communesplone.layout:skins/communesplone_layout_simplify')
        for path in self.skin_paths():
            self.assertEqual(path[:3], ['custom', 'communesplone_layout_simplify', 'communesplone_layout'])
        css = self.portal.portal_css
        ids = list(css.getResourceIds())
        self.assertEqual(ids[ids.index('simplify.css') + 1], 'ploneCustom.css')
        resource = css.getResource('simplify.css')
        self.assertTrue(resource.getEnabled())
        self.assertEqual(resource.getMedia(), 'all')
        self.assertEqual(resource.getExpression(), SIMPLIFY_EXPRESSION)
        self.assertIn('#plone-contentmenu-actions', str(self.skin_object('simplify.css')))
        # shown to the authenticated users outside full-layout, except Managers
        logout()
        self.assertFalse(self.simplify_css_shown())
        login(self.portal, EDITOR)
        self.assertTrue(self.simplify_css_shown())
        login(self.portal, SITE_ADMIN)  # member of full-layout through the Site Administrators group
        self.assertFalse(self.simplify_css_shown())
        login(self.portal, TEST_USER_NAME)
        self.assertTrue(self.simplify_css_shown())
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.assertFalse(self.simplify_css_shown())
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        self.portal.portal_groups.addPrincipalToGroup(EDITOR, 'full-layout')
        login(self.portal, EDITOR)
        self.assertFalse(self.simplify_css_shown())
