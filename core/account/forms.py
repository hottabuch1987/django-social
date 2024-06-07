from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput
from .models import User, Forum, UserImage, Reviews
from django import forms
from typing import Any
from django.core.exceptions import ValidationError
from datetime import date
from django import forms
from django.core.validators import RegexValidator
from django.contrib import messages



class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(UserCreationForm,self).__init__(*args, **kwargs)
        self.fields['email'].label = 'Ваш адрес электронной почты'
        self.fields['email'].required = True
        self.fields['username'].help_text = ''
        self.fields['password1'].help_text = ''

    def clean_email(self):
        email = self.cleaned_data['email'].lower()

        if User.objects.filter(email=email).exists() or len(email) > 254:
            raise forms.ValidationError("Электронный адрес уже существует")
        return email
        
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control'}))
    

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    tel = forms.CharField(max_length=12, min_length=11, validators=[RegexValidator(regex='^\+?1?\d{9,15}$', message='Введите корректный номер телефона.')])
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(UserUpdateForm,self).__init__(*args, **kwargs)
        self.fields['email'].label = 'Ваш адрес электронной почты'
        self.fields['email'].required = True
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'birth_date','tel', 'bio', 'gender', 'avatar', 'marital_status']
        exclude = ['password1', 'password2']

    
    def clean_email(self):
        email = self.cleaned_data['email'].lower()

        if User.objects.filter(email=email).exclude(id=self.instance.id).exists() and len(email) > 254:
            raise forms.ValidationError("Электронная почта уже используется или слишком длинная")
        return email
    
    def clean_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')

        if birth_date:
            age = date.today().year - birth_date.year
            
            if age < 18:
                raise ValidationError("Вы должны быть старше 18 лет для регистрации")
                messages.error("Validation error message")
            if age > 100:
                raise ValidationError("Возраст не должен превышать 100 лет")
                

        return birth_date



class UserImageForm(forms.ModelForm):
    image = forms.ImageField(label='Еще', required=False)  # Задаем свою метку

    class Meta:
        model = UserImage
        fields = [
            'image',
        ]
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file', 'id': 'avatar'}),

        }


class ForumForm(forms.ModelForm):
    class Meta:
        model = Forum
        fields = [
            
            'message_file',
            'content',
           
        ]
    



class ReviewsForm(forms.ModelForm):
    class Meta:
        model = Reviews
        fields = ['phone_number', 'text']

    def __init__(self, *args, **kwargs):
        super(ReviewsForm, self).__init__(*args, **kwargs)
        self.fields['phone_number'].widget.attrs.update({'class': 'form-control', 'placeholder': 'В формате +7 999 999 99'})
        self.fields['text'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Опишите проблему'})

    # def as_styled(self):
    #     for field_name, field in self.fields.items():
    #         field.widget.attrs.update({
    #             'class': 'form-control my-2',
    #             'placeholder': f'Enter your {field.label.lower()}',
    #         })
    #         if field_name == 'text':
    #             field.widget.attrs['rows'] = 3





