"""Robot suites of tests/robot, run with the layer of their file name.

ROBOT_PLONE_MAJOR (4 or 6) selects the UI keywords: robotsuite passes the
ROBOT_* environment variables to the suites as robot variables.
Tests tagged plone4-only are not run on Plone 6 (robotsuite has no tag filter).
"""

from ..testing import ACCEPTANCE
from ..testing import MAINTENANCE_ACCEPTANCE
from ..testing import SIMPLIFY_ACCEPTANCE
from importlib.metadata import version
from plone.testing import layered

import os
import robotsuite
import unittest


# suites needing an optional integration layer, e.g. {'test_facetednav.robot': ADDONS_ACCEPTANCE}
SUITE_LAYERS = {
    "test_maintenance.robot": MAINTENANCE_ACCEPTANCE,
    "test_simplify.robot": SIMPLIFY_ACCEPTANCE,
}


def test_suite():
    os.environ.setdefault(
        "ROBOT_PLONE_MAJOR", version("Products.CMFPlone").split(".")[0]
    )
    plone4 = os.environ["ROBOT_PLONE_MAJOR"] == "4"
    suite = unittest.TestSuite()
    robot_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "robot")
    for name in sorted(os.listdir(robot_dir)):
        if name.startswith("test_") and name.endswith(".robot"):
            tests = [
                test
                for test in robotsuite.RobotTestSuite(os.path.join("robot", name))
                if plone4 or "plone4-only" not in test._tags
            ]
            if tests:
                suite.addTest(
                    layered(
                        unittest.TestSuite(tests),
                        layer=SUITE_LAYERS.get(name, ACCEPTANCE),
                    )
                )
    return suite
