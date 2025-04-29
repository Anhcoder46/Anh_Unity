*** Settings ***
Library    SeleniumLibrary

*** Variables ***
${URL}    https://opensource-demo.orangehrmlive.com/web/index.php/auth/login
${BROWSER}      Chrome
# Tài khoản đăng nhập thành công
${USERNAME}       Admin
${PASSWORD}       admin123
# Tài khoản đăng nhập không thành công
${WRONG_USER}     wronguser
${WRONG_PASS}     wrongpass

*** Test Cases ***
Đăng nhập thành công
    [Documentation]    Kiểm tra đăng nhập thành công với thông tin hợp lệ
    Open Browser    ${URL}    ${BROWSER}
    Wait Until Element Is Visible    name=username    timeout=10s
    Input Text    name=username    ${USERNAME}
    Input Text    name=password    ${PASSWORD}
    Click Button    xpath=//button[@type='submit']

    Wait Until Element Is Visible    xpath=//h6[contains(@class,'oxd-topbar-header-breadcrumb')]    timeout=10s
    Element Text Should Be    xpath=//h6[contains(@class,'oxd-topbar-header-breadcrumb')]    Dashboard
    Log To Console    Đăng nhập thành công như mong đợi
    
    Click Element    xpath=//i[contains(@class,'oxd-userdropdown-icon')]
    Wait Until Element Is Visible    xpath=//a[text()='Logout']    timeout=5s
    Click Link    xpath=//a[text()='Logout']
    Close Browser

Đăng nhập thất bại
    [Documentation]    Kiểm tra đăng nhập thất bại với thông tin không hợp lệ
    Open Browser    ${URL}    ${BROWSER}
    Wait Until Element Is Visible    name=username    timeout=10s
    Input Text    name=username    ${WRONG_USER}
    Input Text    name=password    ${WRONG_PASS}
    Click Button    xpath=//button[@type='submit']
    
    Wait Until Element Is Visible    xpath=//div[contains(@class,'oxd-alert-content')]    timeout=10s
    Element Should Contain    xpath=//div[contains(@class,'oxd-alert-content')]    Invalid credentials
    Log To Console    Đăng nhập thất bại như mong đợi
    Close Browser