# nhs-dentist-alerts
Notifications of NHS dentists accepting new patients

## Python 3.7 virtualenv with pyenv
1. Ensure you have Python 3.7 installed with pyenv
        pyenv install 3.7.4

2. Create if virtualenv for it if necessary
     pyenv virtualenv 3.7.4 nhs-dentist-alerts-3.7.4

3. Activate it
    pyenv local nhs-dentist-alerts-3.7.4

4. Sanity check
    pyenv which python

## Next Steps

[ ] Add click for command line parsing, and invoke from `main()`
[ ] Formatting output
[ ] Add mailer like sendgrid
[ ] Add Celery beat
[ ] Dockerize
[ ] Deploy