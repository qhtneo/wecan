# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm #유저 크리에이션 폼은 username pw1,2있는 폼
from django.contrib.auth.models import User

# UserCreationForm을 상속받는 UserForm을 작성
class UserForm(UserCreationForm):
    email = forms.EmailField(label = "이메일") # label이 뭘까용
    first_name = forms.CharField #first_name이라는 필드 생성
    last_name = forms.CharField

    class Meta : # 폼의 정보를 담고있는 클래스(내부 클래스) #내부 클래스란?
        model = User
        fields = ("username","email","first_name","last_name")

class CustomChangeForm(UserChangeForm):
    class Meta:
        model =User
        fields = ("email","first_name","last_name")
