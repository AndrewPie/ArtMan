from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.contenttypes.models import ContentType
class SignupForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = ['username','first_name','last_name','password1','password2','user_type']

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'First Name'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Last Name'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm Password'})
        self.fields['user_type'].widget.attrs.update({'class': 'custom-select d-block w-100', 'placeholder': 'User Type'})

    def save(self,commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.clean_password2())
        user.is_active=False
        print(user.get_all_permissions())
        if commit:
            user.save()
            self.add_premissions(user)
            return user
    @staticmethod
    def add_premissions(user):
        print(type(user.user_type))
        content_type = ContentType.objects.get_for_model(get_user_model())
        MEDICAL=[ "Can add medical report",
                  "Can del medical report",
                  "Can change medical report",]
        TECHNICAL=[ "Can add technical report",
                  "Can del technical report",
                  "Can change technical report",]
        SUPPLY=[ "Can add supply report",
                  "Can del supply report",
                  "Can change supply report",]
        group=[MEDICAL,TECHNICAL,SUPPLY]
        
        for i in group[user.user_type]:
            permission = Permission.objects.get(
            name=i,
            content_type=content_type,
            )
            user.user_permissions.add(permission)
        user.save()
        

class LoginForm(forms.Form):
    username=forms.CharField(max_length=64)
    password=forms.CharField(max_length=64,widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['class'] = 'form-control'



