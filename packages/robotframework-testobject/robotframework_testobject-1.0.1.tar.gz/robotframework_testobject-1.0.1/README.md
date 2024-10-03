# robotframework-testobject
A simple test object for robot framework without external dependancies and without UI that can be used for trainings and demos

## Installation
```bash
pip install robotframework-testobject
```

## Usage
```robot
*** Settings ***
Library    TestObject

*** Test Cases ***
Test Password Change
    Login User    captain    1234567890
    ${username} =    Get Username
    Should Be Equal    Steve Rogers    ${username}
    Change Own Password    new_password=new_password    old_password=1234567890
    Logout User
    TRY
        Login User    captain     1234567890
    EXCEPT    ValueError: Invalid Password    AS    ${e}
        Log     Access Denied
    ELSE
        Fail    illegal access possible
    END
    Login User    captain     new_password
```
