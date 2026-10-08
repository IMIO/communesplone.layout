*** Settings ***
Documentation  Login page while the source_users plugin is deactivated (F4). Layer MAINTENANCE_ACCEPTANCE.
...            Version-independent: Plone selectors are in ui_plone*.robot.
Resource  communesplone_layout.robot
Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***
The login page shows the maintenance message instead of the login form
    Open the login page
    The maintenance message is shown
    The password field is visible  ${False}
    The forgotten password link is visible  ${False}
