*** Settings ***
Documentation  Editor interface with the simplify profile (F10, F11). Layer SIMPLIFY_ACCEPTANCE.
...            Version-independent: Plone selectors are in ui_plone*.robot.
Resource  communesplone_layout.robot
Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***
An editor outside full-layout gets a simplified interface
    Log in as  ${EDITOR}  ${EDITOR_PASSWORD}
    Go to  ${FOLDER_URL}
    The actions menu is visible  ${False}
    The sharing tab is visible  ${False}
    The display menu is visible  ${False}
    Open the edit form  ${DOC_URL}
    The edit form shows only its first tab

A site administrator in full-layout gets the full interface
    Log in as  ${SITE_ADMIN}  ${SITE_ADMIN_PASSWORD}
    Go to  ${FOLDER_URL}
    The actions menu is visible
    The sharing tab is visible
    The display menu is visible
    Open the edit form  ${DOC_URL}
    The edit form shows all its tabs
