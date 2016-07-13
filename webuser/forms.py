# coding:utf-8
# __author__ = 'BianXuesheng'
# __data__ = '2016/07/12_14:06 '

from numpy import *
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib import auth
from django.utils.safestring import mark_safe


def ForbiddenUsernamesValidator(value):
    forbidden_usernames = ['admin', 'settings', 'news', 'about', 'help', 'signin', 'signup',
                           'signout', 'terms', 'privacy', 'cookie', 'new', 'login', 'logout', 'administrator',
                           'join', 'account', 'username', 'root', 'blog', 'user', 'users', 'billing', 'subscribe',
                           'reviews', 'review', 'blog', 'blogs', 'edit', 'mail', 'email', 'home', 'job', 'jobs',
                           'contribute', 'newsletter', 'shop', 'profile', 'register', 'auth', 'authentication',
                           'campaign', 'config', 'delete', 'remove', 'forum', 'forums', 'download', 'downloads',
                           'contact', 'blogs', 'feed', 'feeds', 'faq', 'intranet', 'log', 'registration', 'search',
                           'explore', 'rss', 'support', 'status', 'static', 'media', 'setting', 'css', 'js',
                           'follow', 'activity', 'questions', 'articles', 'network', '',]
    if value.lower() in forbidden_usernames:
        raise ValidationError(u'被限制用户名.')


def InvalidUsernameValidator(value):
    if '@' in value or '+' in value or '-' in value:
        raise ValidationError(u'输入正确的用户名.')


def UniqueEmailValidator(value):
    if User.objects.filter(email__iexact=value).exists():
        raise ValidationError(u'该邮箱已经被注册')


def UniqueUsernameIgnoreCaseValidator(value):
    if User.objects.filter(username__iexact=value).exists():
        raise ValidationError(u'用户名已经存在.')


class SignUpForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                               max_length=30,
                               label=u"用户名",
                               required=True,
                               help_text='用户名最好包括 <strong>字母和数字</strong>, <strong>特殊</strong> 字符')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label=u"密码")
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                       label=u"确认密码",
                                       required=True)
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control'}),
                            required=True,
                            label=u'邮箱',
                            max_length=75)
    hospital = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                            required=True,
                            label=u'所在医院',
                            max_length=75)

    class Meta:
        model = User
        exclude = ['last_login', 'date_joined']
        fields = ['username', 'email', 'password', 'confirm_password', ]

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].validators.append(ForbiddenUsernamesValidator)
        self.fields['username'].validators.append(InvalidUsernameValidator)
        self.fields['username'].validators.append(UniqueUsernameIgnoreCaseValidator)
        self.fields['email'].validators.append(UniqueEmailValidator)

    def clean(self):
        super(SignUpForm, self).clean()
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and password != confirm_password:
            self._errors['password'] = self.error_class([u'密码不匹配'])
        return self.cleaned_data


class LoginForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                               max_length=30, required=True, label=u'用户名', error_messages={'required': u'用户名不能为空'})
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                               label=u'密码', error_messages={'required': u'密码不能为空'},
                               required=True)

    class Meta:
        model = User
        fields = ['username', 'password']
        exclude = ['last_login', 'date_joined', 'email', 'confirm_password']

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password:
            self.user_cache = auth.authenticate(username=username, password=password)
            if self.user_cache is None:
                self._errors['username'] = self.error_class([u'账号密码不匹配'])
        return self.cleaned_data


class ChangePasswordForm(forms.ModelForm):
    id = forms.CharField(widget=forms.HiddenInput())
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                   label=u'旧密码', required=True)
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                   label=u'新密码', required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                       label=u'确认新密码', required=True)

    class Meta:
        model = User
        fields = ['id', 'old_password', 'new_password', 'confirm_password']

    def clean(self):
        super(ChangePasswordForm, self).clean()
        old_password = self.cleaned_data.get('old_password')
        new_password = self.cleaned_data.get('new_password')
        confirm_password = self.cleaned_data.get('confirm_password')
        id = self.cleaned_data.get('id')
        print id
        user = User.objects.get(pk=id)
        if not user.check_password(old_password):
            self._errors['old_password'] = self.error_class([u'旧密码不对.'])
        if new_password and new_password != confirm_password:
            self._errors['new_password'] = self.error_class([u'密码不一致.'])
        return self.cleaned_data


class ChangeEmailForm(forms.ModelForm):
    id = forms.CharField(widget=forms.HiddenInput())
    old_email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control'}),
                                label=u'旧邮箱', required=True)
    new_email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control'}),
                                label=u'新邮箱', required=True)

    class Meta:
        model = User
        fields = ['id', 'old_email', 'new_email']

    def clean(self):
        super(ChangeEmailForm, self).clean()
        old_email = self.cleaned_data.get('old_email')
        new_email = self.cleaned_data.get('new_email')
        id = self.cleaned_data.get('id')
        print id
        user = User.objects.get(pk=id)
        print user.email
        if not old_email == user.email:
            self._errors['old_email'] = self.error_class([u'旧邮箱不对.'])
        return self.cleaned_data
