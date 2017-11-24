from django.shortcuts import redirect


def login_redirect(self):
    return redirect('/ordering/login')
