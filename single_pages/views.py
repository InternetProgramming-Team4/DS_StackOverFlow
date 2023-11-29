from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignUpForm
from django.contrib import auth
from django.contrib.auth import get_user_model
from post.models import Post
from .models import Profile

# 사용자가 있는지 검사하는 함수



# Create your views here.
def main(request):
    return render(
        request,
        'single_pages/index.html'
    )

def user(request):
    post_list = Post.objects.all().order_by('-pk')

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
    if request.method == "POST":
        form = SignUpForm(request.POST)

        if form.is_valid():  # 폼 내용 유효성검사 후 괜찮으면
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            major = form.cleaned_data['major']

            exist_user = User.objects.filter(username=username)
            if exist_user:
                # 사용자가 존재하기 때문에 사용자를 저장하지 않고 회원가입 페이지를 다시 띄움
                messages.warning(request, "이미 있는 이름입니다")
                return render(request, 'single_pages/signup.html')  # 오류메세지 뜨게 할 뭔가 없나

            new_user = User.objects.create_user(username=username, email=email, password=password)
            Profile.objects.create(user=new_user, major=major)
            # 새로운 사용자 User에 추가

            return redirect('../')
            # 회원가입 완료 후에 메인페이지로 이동

    else:
        form = SignUpForm()
        # 뭔가 내용 안 맞으면 다시 form 작성하도록

    context = {'form': form}
    return render(request, 'single_pages/signup.html', context)

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)

        me = authenticate(request, username=username, password=password)

        if me is not None:
            auth_login(request, me)  # 사용자 로그인
            return redirect('../')

        else:
            messages.error(request, '아이디 혹은 비밀번호가 올바르지 않습니다.')
            return redirect('./')

    else:
        return render(request, 'single_pages/login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')


#로그아웃 상태에서 저장을 누르게 되면 로그인창으로 이동
@login_required
def edit_major(request):
    if request.method == 'POST':
        selected_major = request.POST.get('major')
        profile = Profile.objects.get(user=request.user)
        profile.major = selected_major
        profile.save()
        return redirect('/MyPage/')  # 저장 후 프로필 페이지로 이동

    else:
        return redirect('/MyPage/')



