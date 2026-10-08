# -*- coding: utf-8 -*-
from communesplone.layout.testing import SIMPLIFY_INTEGRATION

import unittest


ADMIN_ROLES = ['Manager', 'Site Administrator']
PERMISSIONS = {
    'Sharing page: Delegate roles': ADMIN_ROLES,
    'Modify view template': ADMIN_ROLES,
    'Review portal content': ['Manager', 'Reviewer', 'Site Administrator'],
    'Modify constrain types': ADMIN_ROLES,
    'CMFPlacefulWorkflow: Manage workflow policies': ADMIN_ROLES,
}


class TestSetuphandlers(unittest.TestCase):

    layer = SIMPLIFY_INTEGRATION

    def setUp(self):
        self.portal = self.layer['portal']
        self.groups = self.portal.portal_groups

    def run_step(self, profile):
        self.portal.portal_setup.runImportStepFromProfile('profile-communesplone.layout:{}'.format(profile),
                                                          'layout-simplify')

    def test_simplify(self):
        # applied by the simplify profile of the layer
        group = self.groups.getGroupById('full-layout')
        self.assertEqual(group.getProperty('title'), 'Full edition layout')
        self.assertEqual(sorted(group.getGroupMemberIds()), ['Administrators', 'Site Administrators'])
        for permission, roles in PERMISSIONS.items():
            self.assertEqual([r['name'] for r in self.portal.rolesOfPermission(permission) if r['selected']], roles)
            self.assertEqual(self.portal.acquiredRolesAreUsedBy(permission), '', permission)
        # second run: the group is created once, its members are not reset
        self.groups.removePrincipalFromGroup('Site Administrators', 'full-layout')
        self.run_step('simplify')
        self.assertEqual(self.groups.getGroupById('full-layout').getGroupMemberIds(), ['Administrators'])
        # the step does nothing for another profile (marker file)
        self.groups.removeGroup('full-layout')
        self.run_step('default')
        self.assertIsNone(self.groups.getGroupById('full-layout'))
        self.run_step('simplify')
        self.assertEqual(sorted(self.groups.getGroupById('full-layout').getGroupMemberIds()),
                         ['Administrators', 'Site Administrators'])
