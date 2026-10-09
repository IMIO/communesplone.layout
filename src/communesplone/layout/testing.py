# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import login
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.testing import zope
from Products.PluggableAuthService.interfaces.plugins import IAuthenticationPlugin

import communesplone.layout


SERVER_FIXTURE = zope.WSGI_SERVER_FIXTURE

EDITOR = "editor"
EDITOR_PASSWORD = "editor-secret"
SITE_ADMIN = "siteadmin"
SITE_ADMIN_PASSWORD = "siteadmin-secret"


class LayoutLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        self.loadZCML(package=communesplone.layout)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "communesplone.layout:default")
        # editor outside full-layout; site administrator in full-layout through the Site Administrators group
        portal.acl_users.userFolderAddUser(
            EDITOR, EDITOR_PASSWORD, ["Editor", "Contributor"], []
        )
        portal.acl_users.userFolderAddUser(SITE_ADMIN, SITE_ADMIN_PASSWORD, [], [])
        portal.portal_groups.addPrincipalToGroup(SITE_ADMIN, "Site Administrators")
        setRoles(portal, TEST_USER_ID, ["Manager"])
        login(portal, TEST_USER_NAME)
        portal.invokeFactory("Folder", "folder", title="Folder")
        portal.folder.invokeFactory("Document", "doc", title="Document")
        setRoles(portal, TEST_USER_ID, ["Member"])


class SimplifyLayer(PloneSandboxLayer):

    def setUpPloneSite(self, portal):
        applyProfile(portal, "communesplone.layout:simplify")


class MaintenanceLayer(PloneSandboxLayer):
    """The source_users authentication plugin is deactivated (maintenance)."""

    def setUpPloneSite(self, portal):
        portal.acl_users.plugins.deactivatePlugin(IAuthenticationPlugin, "source_users")


FIXTURE = LayoutLayer(name="communesplone.layout:FIXTURE")
SIMPLIFY_FIXTURE = SimplifyLayer(
    bases=(FIXTURE,), name="communesplone.layout:SIMPLIFY_FIXTURE"
)
MAINTENANCE_FIXTURE = MaintenanceLayer(
    bases=(FIXTURE,), name="communesplone.layout:MAINTENANCE_FIXTURE"
)

INTEGRATION = IntegrationTesting(
    bases=(FIXTURE,), name="communesplone.layout:INTEGRATION"
)
FUNCTIONAL = FunctionalTesting(bases=(FIXTURE,), name="communesplone.layout:FUNCTIONAL")
SIMPLIFY_INTEGRATION = IntegrationTesting(
    bases=(SIMPLIFY_FIXTURE,), name="communesplone.layout:SIMPLIFY_INTEGRATION"
)

ACCEPTANCE = FunctionalTesting(
    bases=(FIXTURE, REMOTE_LIBRARY_BUNDLE_FIXTURE, SERVER_FIXTURE),
    name="communesplone.layout:ACCEPTANCE",
)
SIMPLIFY_ACCEPTANCE = FunctionalTesting(
    bases=(SIMPLIFY_FIXTURE, REMOTE_LIBRARY_BUNDLE_FIXTURE, SERVER_FIXTURE),
    name="communesplone.layout:SIMPLIFY_ACCEPTANCE",
)
MAINTENANCE_ACCEPTANCE = FunctionalTesting(
    bases=(MAINTENANCE_FIXTURE, REMOTE_LIBRARY_BUNDLE_FIXTURE, SERVER_FIXTURE),
    name="communesplone.layout:MAINTENANCE_ACCEPTANCE",
)
