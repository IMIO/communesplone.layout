*** Settings ***
Documentation  Login form of the skin layer when the source_users plugin is active (F3).
...            Version-independent: Plone selectors are in ui_plone*.robot.
Resource  communesplone_layout.robot
Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***
A user logs in with the login form
    Open the login page
    The maintenance message is not shown
    The password field is visible
    The forgotten password link is visible
    Log in as  ${EDITOR}  ${EDITOR_PASSWORD}
