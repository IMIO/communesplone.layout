*** Settings ***
Documentation  Plone 6 Classic UI keywords. Same keyword names and arguments as ui_plone4.robot.
...            Robot Framework 3.0 syntax: shared with the Plone 4.3 (Python 2) environment.
...            Selectors checked on Plone 6.1 (collective.contact.contactlist) and 6.2 (communesplone.layout phase 7).
Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot
Library  Remote  ${PLONE_URL}/RobotRemote


*** Variables ***
${MODAL}  css=.modal-dialog
${ERROR_PAGE_TEXT}  there seems to be an error
${NOT_FOUND_TEXT}  This page does not seem to exist
# tabs of the edit form of a Document (Dexterity fieldset labels)
${FIRST_EDIT_TAB}  Default
@{OTHER_EDIT_TABS}  Categorization  Dates  Ownership  Settings


*** Keywords ***
Log in with the login form
    [Documentation]  Real login (creates the user folder), unlike autologin
    [Arguments]  ${username}  ${password}
    Disable autologin
    Go to  ${PLONE_URL}/login
    Input text  css=#__ac_name  ${username}
    Input password  css=#__ac_password  ${password}
    # 6.2: the button keeps a disabled class until the validation pattern ran
    Wait until page does not contain element  css=#buttons-login.disabled
    Click button  css=#buttons-login
    Wait until page contains element  css=#personaltools-menulink

Click the content action
    [Documentation]  Item of the Actions menu (object_buttons), by action id
    [Arguments]  ${action_id}
    Click element  css=#plone-contentmenu-actions > a
    Wait until element is visible  css=#plone-contentmenu-actions-${action_id}
    Click element  css=#plone-contentmenu-actions-${action_id}

The content action is available
    [Arguments]  ${action_id}  ${expected}=${True}
    Click element  css=#plone-contentmenu-actions > a
    Wait until element is visible  css=#plone-contentmenu-actions ul
    Run keyword if  ${expected}
    ...  Page should contain element  css=#plone-contentmenu-actions-${action_id}
    ...  ELSE  Page should not contain element  css=#plone-contentmenu-actions-${action_id}

Open the add menu
    Click element  css=#plone-contentmenu-factories > a
    Wait until element is visible  css=#plone-contentmenu-factories ul

The personal action links to
    [Documentation]  Item of the user menu (user actions), by action id
    [Arguments]  ${action_id}  ${url}
    Element attribute value should be  css=#personaltools-${action_id}  href  ${url}

The personal action is not available
    [Arguments]  ${action_id}
    Page should not contain element  css=#personaltools-${action_id}

The modal is open
    [Documentation]  Overlay (Plone 4) or modal (Plone 6) showing a form
    Wait until element is visible  ${MODAL} form

Modal element
    [Documentation]  Locator of the element with this id inside the modal
    ...              (an argument starting with # would be a robot comment)
    [Arguments]  ${id}
    [Return]  ${MODAL} [id="${id}"]

Save the modal
    Click button  css=.modal-footer #form-buttons-save

Cancel the modal
    Click button  css=.modal-footer #form-buttons-cancel

The modal is closed
    Wait until page does not contain element  ${MODAL}

The status message contains
    [Arguments]  ${text}
    Wait until element contains  css=.portalMessage  ${text}

The page is not an error
    Page should not contain  ${ERROR_PAGE_TEXT}

The page is not found
    Page should contain  ${NOT_FOUND_TEXT}

The edit link is not available
    Page should not contain element  css=#contentview-edit

# communesplone.layout keywords below: checked on Plone 6.2, except the send-to ones (plone4-only scenario)

The element is visible
    [Documentation]  Visible, or (expected False) hidden or absent
    [Arguments]  ${locator}  ${expected}=${True}
    Run keyword if  ${expected}  Element should be visible  ${locator}
    ...  ELSE  Element should not be visible  ${locator}

The user is logged in
    Page should contain element  css=#personaltools-logout
    Page should not contain element  css=#personaltools-login

Open the login page
    Go to  ${PLONE_URL}/login

The password field is visible
    [Arguments]  ${expected}=${True}
    The element is visible  css=#__ac_password  ${expected}

The forgotten password link is visible
    [Arguments]  ${expected}=${True}
    The element is visible  css=a[href$="/@@login-help"]  ${expected}

The actions menu is visible
    [Arguments]  ${expected}=${True}
    The element is visible  css=#plone-contentmenu-actions  ${expected}

The sharing tab is visible
    [Arguments]  ${expected}=${True}
    The element is visible  css=#contentview-local_roles  ${expected}

The display menu is visible
    [Arguments]  ${expected}=${True}
    The element is visible  css=#plone-contentmenu-display  ${expected}

Open the edit form
    [Documentation]  Edit form of a Dexterity content (autotoc tabs)
    [Arguments]  ${url}
    Go to  ${url}/edit
    Wait until page contains element  css=nav.autotoc-nav

The edit form tab is visible
    [Documentation]  Tab of the edit form, by label: shown, or (expected False) in the page but hidden
    [Arguments]  ${label}  ${expected}=${True}
    ${locator}=  Set variable  xpath=//nav[contains(@class, "autotoc-nav")]//a[normalize-space()="${label}"]
    Page should contain element  ${locator}
    The element is visible  ${locator}  ${expected}

Open the send-to form
    [Arguments]  ${url}
    Go to  ${url}/@@sendto_form

The captcha is asked
    Element should be visible  css=input[name="captcha"]
    Page should contain image  css=img[src$="/@@captcha/image"]

Send the page
    [Arguments]  ${send_to_address}  ${captcha}
    Input text  css=#form-widgets-send_to_address  ${send_to_address}
    Input text  css=input[name="captcha"]  ${captcha}
    Click button  css=#form-buttons-send
