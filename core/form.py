import random
import string

from django import forms

from core.models import Url, MyUser
from core.tasks import parse_original_url


class UrlForm(forms.ModelForm):

    url = forms.CharField(label='')
    short_url = forms.CharField(label='', required=False)

    class Meta:
        model = Url
        fields = ('url', 'short_url')

    def clean_url(self):

        url = self.cleaned_data['url']

        if not (url.startswith('https://') or url.startswith('http://')):
            raise forms.ValidationError('The URL entered is invalid. (is http:// missing?)')

        return url

    def clean_short_url(self):

        short_url = self.cleaned_data['short_url']
        urls = Url.objects.all()

        for url in urls:
            if url.short_url == short_url:
                if url.short_url != '':
                    raise forms.ValidationError('Short url with the same name already exists! '
                                                'Please, choose another url!')

        return short_url

    def save(self, *args, **kwargs):

        url = super().save(commit=False)
        url.author = kwargs.get('user')

        if not self.cleaned_data['short_url']:
            short_url = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
            url.short_url = short_url

        url.save()

        parse_original_url.delay(url.id)

        return url


class RegistrationForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}))
    password_check = forms.CharField(widget=forms.PasswordInput)

    class Meta:

        model = MyUser
        fields = ('username', 'password', 'password_check', 'first_name', 'last_name', 'email', 'date_of_birth',
                  'personal_information', 'avatar')
        help_texts = {
            'username': None,
        }

    def clean(self):

        cleaned_data = self.cleaned_data

        username = cleaned_data['username']
        password = cleaned_data['password']
        password_check = cleaned_data['password_check']
        email = cleaned_data['email']

        if MyUser.objects.filter(username=username).exists():
            self.add_error('username', 'Пользователь с таким именем уже зарегестрирован!')

        if password != password_check:
            self.add_error('password', 'Пароли не совпадают!')

        if MyUser.objects.filter(email=email).exists():
            self.add_error('email', 'Пользователь с таким емайлом уже зарегестрирован!')

        return cleaned_data

    def save(self, *args, **kwargs):

        user = super().save(commit=False)

        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        email = self.cleaned_data['email']
        date_of_birth = self.cleaned_data['date_of_birth']
        personal_information = self.cleaned_data['personal_information']
        avatar = self.cleaned_data['avatar']

        user.username = username
        user.set_password(password)
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.date_of_birth = date_of_birth
        user.personal_information = personal_information
        user.avatar = avatar

        user.save()

        return user


class LoginForm(forms.Form):

    username = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput())

    def clean(self):

        cleaned_data = self.cleaned_data

        username = cleaned_data['username']
        password = cleaned_data['password']

        if not MyUser.objects.filter(username=username).exists():
            self.add_error('username', 'Пользователь с таким именем не зарегестрирован!')

        try:
            user = MyUser.objects.get(username=username)
        except:
            user = None

        if user and not user.check_password(password):
            self.add_error('password', 'Не верный пароль!')

        return cleaned_data
