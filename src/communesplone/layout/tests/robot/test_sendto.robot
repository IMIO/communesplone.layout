*** Settings ***
Documentation  Send-to form of the skin layer (F6): needs collective.captcha, installed in the 4.3 test env only.
...            Version-independent: Plone selectors are in ui_plone*.robot.
Resource  communesplone_layout.robot
Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***
The send-to form asks for a captcha
    [Tags]  plone4-only
    Log in as  ${EDITOR}  ${EDITOR_PASSWORD}
    Open the send-to form  ${DOC_URL}
    The captcha is asked
    Send the page  to@example.com  WRONG
    The send-to form shows the captcha error
    The captcha is asked
