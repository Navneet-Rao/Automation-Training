*** Settings ***
Library  SSHLibrary

*** Variables ***
${Router}   192.168.62.131
&{cred}   user=navneet   pass=Navneet@123
${Router2}    192.168.62.132
&{cred2}    user=navneet  pass=Navneet@123
@{Switch}    10.1.1.1   10.1.1.2   10.1.1.3

*** Test Cases ***


Login To Router
    [Documentation]    Router connection
        [Tags]   Navo
        [Setup]    Connect To Router
        [Teardown]    Close All Connections
        ${host}=   Set Variable   8.8.8.8
        ${output}=   Execute Command    ip a
        Should Contain   ${output}    00:0c:29:ee:59:7b
        Log To Console  ${output}
        Log To Console  ${host}

Addition
        ${sum}=  Add   5   6
        Log    Sum is ${sum}
Greet
    Simple

Default route
        [Setup]    Connect To Router
        [Teardown]    Close All Connections
        ${route} =   Execute Command  ip r
        IF      "192.168.10.1" in $route
            Log    default route is valid
        ELSE
            Log     Default route is invalid
        END

For Loop
    FOR   ${IP}   IN   @{Switch}
        Log To Console  ${IP}
    END

While
    ${count}=   Set Variable  ${0}
    WHILE  ${count}<5
        Log To Console  count is ${count}
        ${count}=   Evaluate   ${count}+1
    END

Exception

    TRY
        Connect To Router2
        Log To Console   Logged in successfully

    EXCEPT
        Log To Console   Login failed

    ELSE
        Log To Console   Login passed

    FINALLY
        Close Connection



    END

*** Keywords ***
 Add
    [Arguments]       ${a}     ${b}
    ${result}=   Evaluate  ${a} + ${b}
    RETURN   ${result}

 Simple
    [Arguments]      ${name}=Nav
    Log     Hello, ${name}

 Connect To Router
    Open Connection   ${Router}
    Login    ${cred}[user]   ${cred}[pass]

 Connect To Router2
    Open Connection   ${Router2}
    Login    ${cred2}[user]   ${cred2}[pass]

 Close All Connections
    Close Connection

