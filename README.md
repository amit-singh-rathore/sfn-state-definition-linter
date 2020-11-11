# Pystatelint
A simple Amazon States Language validator based on JSON schemas written in python. 

It will return following error codes with detial message if there are violations in the schema definition:
* MISSING_STATE_INCOMING
* MISSING_STATE_DEFINITION
* DUPLICATE_STATE_DEFINITION
* NO_END_STATE
* INVALID_DEF
* INCORRECT_PATH
 
This can be extended by adding a cutsom rule based on business requrement. Some example are like below
* INVALID_RESOURCE_ARN
* MISSING_CALLBACK


## Why we need this?
When writing SFN state machine, we cant validate state machine definition locally. This project makes it possible in python environment.

## Usage

```python
from pystatelint import validate

validate.validate(definition)
```








