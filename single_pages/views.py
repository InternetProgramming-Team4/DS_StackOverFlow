from django.shortcuts import render

# Create your views here.
def main(request):
    return render(
        request,
        'single_pages/index.html'
    )

def user(request):
    return render(
        request,
        'single_pages/MyPage.html'
    )

def login(request):
    return render(
        request,
        'single_pages/login.html'
    )

def signup(request):
    return render(
        request,
        'single_pages/signup.html'
    )