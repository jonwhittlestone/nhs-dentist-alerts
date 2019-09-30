# nhs-dentist-alerts
Notifictions of NHS dentists accepting new patients

## Python 3.7 virtualenv with pyenv
1. Ensure you have Python 3.7 installed with pyenv
        pyenv install 3.7.4

2. Create if virtualenv for it if necessary
     pyenv virtualenv 3.7.4 nhs-dentist-alerts-3.7.4

3. Activate it
    pyenv local nhs-dentist-alerts-3.7.4

4. Sanity check
    pyenv which python

## Current Problem

I have refactored code into separate modules.

`main.py` is still the top-most module that is executed to run the main program, but I cannot have both the main program and the `pytest` tests running succesfully.

The two variations are:

* MAIN PROGRAM RUN **PASS** | TESTS RUN **FAIL**
    - `collectors.py`: `from config import *`
    - error on `pytest`:
        - `E   ModuleNotFoundError: No module named 'config'`

* MAIN PROGRAM RUN **FAIL** | TESTS RUN **PASS**
    - `collectors.py`: `from .config import *`
    - error on main program:
        - `ImportError: attempted relative import with no known parent package`
        
        


