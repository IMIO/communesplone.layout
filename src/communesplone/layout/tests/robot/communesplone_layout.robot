*** Settings ***
Documentation  communesplone.layout keywords, built on the ui_plone${PLONE_MAJOR}.robot keywords.
...            Robot Framework 3.0 syntax (shared with the Plone 4.3 environment).
Resource  ui_plone${PLONE_MAJOR}.robot


*** Variables ***
# users and content of communesplone.layout.testing
${EDITOR}  editor
${EDITOR_PASSWORD}  editor-secret
${SITE_ADMIN}  siteadmin
${SITE_ADMIN_PASSWORD}  siteadmin-secret
${FOLDER_URL}  ${PLONE_URL}/folder
${DOC_URL}  ${FOLDER_URL}/doc
${CAPTCHA_ERROR}  Please provide the message here above correctly, case sensitive.


*** Keywords ***
Log in as
    [Arguments]  ${username}  ${password}
    Log in with the login form  ${username}  ${password}
    The user is logged in

The maintenance message is shown
    Element should be visible  css=#no_plugin
    Element should contain  css=#no_plugin  The connection to the site is temporary suspended for maintenance operations.
    Element attribute value should be
    ...  xpath=//*[@id="no_plugin"]//a[normalize-space()="Contact the site administrator"]  href  ${PLONE_URL}/contact-info

The maintenance message is not shown
    Page should not contain element  css=#no_plugin

The edit form shows only its first tab
    The edit form tab is visible  ${FIRST_EDIT_TAB}
    FOR  ${label}  IN  @{OTHER_EDIT_TABS}
        The edit form tab is visible  ${label}  ${False}
    END

The edit form shows all its tabs
    The edit form tab is visible  ${FIRST_EDIT_TAB}
    FOR  ${label}  IN  @{OTHER_EDIT_TABS}
        The edit form tab is visible  ${label}
    END

The send-to form shows the captcha error
    Page should contain  ${CAPTCHA_ERROR}
