from django import forms
from django.contrib.auth.models import User


class SignUpForm(forms.Form):
    username = forms.CharField(
        max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Duksung'}))
    email = forms.EmailField(
        max_length=254, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'duksung@duksung.ac.kr'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    major = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'major'})
    )

# 위에 코드만 사용했더니 비밀번호가 한자리여도 통과되는 문제가 생김... 유효성 검사하는 함수 추가

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")

        if len(password) < 8:
            self.add_error('password', '비밀번호는 8자 이상이어야 합니다.')

        elif password is None:   # TypeError: object of type 'NoneType' has no len() 오류 때문에 추가
            self.add_error('password', '비밀번호를 입력하세요.')






