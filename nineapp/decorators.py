from functools import wraps
from django.conf import settings
from django.contrib import messages

import requests

# view_func reps the view.py function that is wrapped or to be decorated
# using the basis of request which formally represents any request to a url in the app
# check if request.is_valid else if not

def check_recaptcha(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.method == "POST":
            url = "https://www.google.com/recaptcha/api/siteverify"
            ca = request.POST["g-recaptcha-response"]
            params = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': ca,
            }
            verify_rs = requests.get(url, params=params, verify=True)
            verify_rs = verify_rs.json()
            status =  verify_rs.get("success", False)
            request.recaptcha_is_valid = status
            if not request.recaptcha_is_valid:
                messages.error(request, '⚠: 🧐reCaptcha entry is incorrect: Try again')


        return view_func(request, *args, **kwargs)
    return _wrapped_view
