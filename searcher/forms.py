# coding=utf-8
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.forms.widgets import RadioFieldRenderer
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from searcher.models import UserInformation

__author__ = 'py'
from django import forms


class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    email = forms.EmailField(required=False)
    message = forms.CharField(widget=forms.Textarea)

    def clean_message(self):
        message = self.cleaned_data['message']
        num_words = len(message.split())
        if num_words < 4:
            raise forms.ValidationError("Not enough words!")
        return message


class SearchForm(forms.Form):
    searchWord = forms.IntegerField(required=False, widget=forms.TextInput(
        attrs={'type': 'text', 'placeholder': '请输入投资金额'}))


class LoginForm(forms.Form):
    username = forms.CharField(
        required=True,
        label=u"手机号",
        error_messages={'required': '请输入手机号'},
        widget=forms.TextInput(
            attrs={
                'placeholder': u"手机号",
                'type': 'text',
                'name': 'name',
                'class': 'inputxt'
            }
        ),
    )

    password = forms.CharField(
        required=True,
        label=u"密码",
        error_messages={'required': u'请输入密码'},
        widget=forms.PasswordInput(
            attrs={
                'placeholder': u"密码",
                'type': 'password',
                'name': 'userpassword',
                'class': 'inputxt',
            }
        ),
    )

    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError(u"用户名和密码为必填项")
        else:
            return super(LoginForm, self).clean()

    def valiatetype(self, a):
        global msg
        if a == 2:
            msg = u"用户不存在"
            self._errors["username"] = self.error_class([msg])
        elif a == 3:
            msg = u"用户被锁定"
            self._errors["username"] = self.error_class([msg])
        elif a == 4:
            msg = u"用户名或密码错误"
            print "flase"
            self._errors["username"] = self.error_class([msg])


class RegisterForm(forms.Form):
    username = forms.CharField(
        required=True,
        label=u"手机号",
        error_messages={'required': '请输入手机号'},
        widget=forms.TextInput(
            attrs={
                'placeholder': u"手机号",
                'type': 'text',
                'class': 'inputxt',
            }
        ),
    )


    password = forms.CharField(
        required=True,
        label=u"密码",
        error_messages={'required': u'请输入密码'},
        widget=forms.PasswordInput(
            attrs={
                'placeholder': u"密码",
                'type': 'password',
                'name': 'userpassword',
                'class': 'inputxt'
            }
        ),
    )
    password2 = forms.CharField(
        required=True,
        label=u"确认密码",
        error_messages={'required': u'请重新输入密码'},
        widget=forms.PasswordInput(
            attrs={
                'placeholder': u"确认密码",
                'type': 'password',
                'name': 'userpassword2',
                'class': 'inputxt'
            }
        ),
    )
    smscode = forms.CharField(
        required=True,
        label=u"短信验证码",
        error_messages={'required': u'请输入短信验证码'},
        widget=forms.TextInput(
            attrs={
                'placeholder': u"短信验证码",
                'type': 'text',
                'name': 'smscode',
                'class': 'inputxt',
            }
        ),
    )

    vcode = forms.CharField(
        required=True,
        label=u"验证码",
        error_messages={'required': u'请输入验证码'},
        widget=forms.TextInput(
            attrs={
                'placeholder': u"验证码",
                'type': 'text',
                'name': 'yzm',
                'class': 'inputxt',
            }
        ),
    )

    def valiatetype(self, a):
        global msg
        if a == 2:
            msg = u"用户已存在"
            self._errors["username"] = self.error_class([msg])
        elif a == 3:
            msg = u"两次密码输入不一致"
            self._errors["password2"] = self.error_class([msg])
        elif a == 4:
            msg = u"图片验证码错误"
            self._errors["vcode"] = self.error_class([msg])
        elif a == 5:
            msg = u"短信验证码错误"
            self._errors["smscode"] = self.error_class([msg])

class WXLoginForm(forms.Form):
    username = forms.CharField(
        required=True,
        label=u"用户名",
        error_messages={'required': '请输入用户名'},
        widget=forms.TextInput(
            attrs={
                'placeholder': u"用户名",
                'type': 'text',
                'name': 'name',
                'class': 'inputxt'
            }
        ),
    )
    password = forms.CharField(
        required=True,
        label=u"密码",
        error_messages={'required': u'请输入密码'},
        widget=forms.PasswordInput(
            attrs={
                'placeholder': u"密码",
                'type': 'password',
                'name': 'userpassword',
                'class': 'inputxt'
            }
        ),
    )


    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError(u"用户名和密码为必填项")
        else:
            return super(WXLoginForm, self).clean()

    def valiatetype(self, a):
        global msg
        if a == 2:
            msg = u"用户不存在"
            self._errors["username"] = self.error_class([msg])
        elif a == 3:
            msg = u"用户被锁定"
            self._errors["username"] = self.error_class([msg])
        elif a == 4:
            msg = u"验证码错误"
            self._errors["vcode"] = self.error_class([msg])


class WXRegisterForm(forms.Form):
    username = forms.CharField(
        required=True,
        label=u"用户名",
        error_messages={'required': '请输入用户名'},
        widget=forms.TextInput(
            attrs={
                'placeholder': u"用户名",
                'type': 'text',
                'class': 'inputxt',
                'ajaxurl': '/register/'
            }
        ),
    )
    password = forms.CharField(
        required=True,
        label=u"密码",
        error_messages={'required': u'请输入密码'},
        widget=forms.PasswordInput(
            attrs={
                'placeholder': u"密码",
                'type': 'password',
                'name': 'userpassword',
                'class': 'inputxt'
            }
        ),
    )
    password2 = forms.CharField(
        required=True,
        label=u"确认密码",
        error_messages={'required': u'请重新输入密码'},
        widget=forms.PasswordInput(
            attrs={
                'placeholder': u"确认密码",
                'type': 'password',
                'name': 'userpassword2',
                'class': 'inputxt'
            }
        ),
    )
    email = forms.EmailField(
        required=True,
        label=u"邮箱",
        error_messages={'required': u'请输入邮箱'},
        widget=forms.TextInput(
            attrs={
                'placeholder': u"邮箱",
                'type': 'text',
                'name': 'mail',
                'class': 'inputxt'
            }
        ),
    )


    def valiatetype(self, a):
        global msg
        if a == 2:
            msg = u"用户已存在"
            self._errors["username"] = self.error_class([msg])
        elif a == 3:
            msg = u"两次密码输入不一致"
            self._errors["password2"] = self.error_class([msg])
        elif a == 4:
            msg = u"验证码错误"
            self._errors["vcode"] = self.error_class([msg])



class TRegForm(forms.Form):
    username = forms.CharField(
        required=True,
        label=u"用户名",
        error_messages={'required': '请输入用户名'},
        widget=forms.TextInput(
            attrs={
                'placeholder': u"用户名",
                'type': 'text',
                'class': 'inputxt',
                'ajaxurl': '/qq_is_first/'
            }
        ),
    )
    email = forms.EmailField(
        required=True,
        label=u"邮箱",
        error_messages={'required': u'请输入邮箱'},
        widget=forms.TextInput(
            attrs={
                'placeholder': u"邮箱",
                'type': 'text',
                'name': 'mail',
                'class': 'inputxt'
            }
        ),
    )
    # email = forms.EmailField(
    #     required=True,
    #     label=u"email",
    #     error_messages={'required': ''},
    #     widget=forms.TextInput(
    #         attrs={
    #             'placeholder': u"email",
    #         }
    #     ),
    # )
    wbid = forms.CharField(
        required=False,
        label=u"微博ID",
        widget=forms.HiddenInput(attrs={'value': 'a'}),
    )
    openid = forms.CharField(
        required=False,
        label=u"OPENID",
        widget=forms.HiddenInput(attrs={'value': 'a'}),
    )
    accessToken = forms.CharField(
        required=False,
        label=u"访问秘钥",
        widget=forms.HiddenInput(attrs={'value': 'a'}),
    )
    url = forms.CharField(
        required=False,
        label=u"头像路径",
        widget=forms.HiddenInput(attrs={'value': 'a'}),
    )
    def valiatetype(self, a):
        global msg
        if a == 8:
            msg = u"用户已存在"
            self._errors["username"] = self.error_class([msg])
            msg2 = u"please input email!"
            self._errors["email"] = self.error_class([msg2])


class FavoriteForm(forms.Form):
    user_id = forms.IntegerField()
    favorite_type = forms.IntegerField()
    favorite_id = forms.IntegerField()


class MyCustomRenderer(RadioFieldRenderer):
    def render(self):
        """Outputs a series of label fields for this set of radio fields."""
        return mark_safe(u'&nbsp;&nbsp;'.join([u'%s' % force_unicode(w) for w in self]))


class UserInformationForm(ModelForm):
    class Meta:
        model = UserInformation
        fields = ('realname', 'gender', 'birthday', 'cellphone', 'email', 'city', 'address', 'education',
                  'monthly_income', 'marriage', 'qq_num', 'wechat_num', 'weibo_num')
        widgets = {
            # 'nickname': forms.TextInput(attrs={'class': 'user_text'}),
            'realname': forms.TextInput(attrs={'class': 'user_text'}),
            'gender': forms.RadioSelect(renderer=MyCustomRenderer, attrs={'class': 'user_radio'}),
            'birthday': forms.TextInput(attrs={'class': 'user_text'}),
            'cellphone': forms.TextInput(attrs={'class': 'user_text'}),
            'email': forms.EmailInput(attrs={'class': 'user_text'}),
            'city': forms.TextInput(attrs={'class': 'user_text'}),
            'address': forms.TextInput(attrs={'class': 'user_text'}),
            'education': forms.Select(attrs={'class': 'user_select'}),
            'monthly_income': forms.Select(attrs={'class': 'user_select'}),
            'marriage': forms.RadioSelect(renderer=MyCustomRenderer, attrs={'class': 'user_radio'}),
            'qq_num': forms.TextInput(attrs={'class': 'user_text'}),
            'wechat_num': forms.TextInput(attrs={'class': 'user_text'}),
            'weibo_num': forms.TextInput(attrs={'class': 'user_text'}),
        }

    def clean_qq_num(self):
        qq_num = self.cleaned_data['qq_num']
        if len(qq_num) > 0 and not qq_num.isdigit():
            raise forms.ValidationError(u"请输入合法qq号")
        return qq_num

    def clean_cellphone(self):
        cellphone = self.cleaned_data['cellphone']
        if len(cellphone) > 0:
            if len(cellphone) != 11 or not cellphone.isdigit():
                raise forms.ValidationError(u"请输入合法手机号")
        return cellphone


class UserReminderForm(forms.Form):
    checkkb = forms.CheckboxInput(attrs={'class': 'user_checkbox'})
    checkmb = forms.CheckboxInput(attrs={'class': 'user_checkbox'})
    checkhk = forms.CheckboxInput(attrs={'class': 'user_checkbox'})


class ForgetPW(forms.Form):
    username = forms.CharField(
        required=True,
        label=u"手机号",
        error_messages={'required': '请输入手机号'},
        widget=forms.TextInput(
            attrs={
                'placeholder': u"手机号",
                'type': 'text',
                'name': 'name',
                'class': 'inputxt'
            }
        ),
    )

    smscode = forms.CharField(
        required=True,
        label=u"短信验证码",
        error_messages={'required': u'请输入短信验证码'},
        widget=forms.TextInput(
            attrs={
                'placeholder': u"短信验证码",
                'type': 'text',
                'name': 'smscode',
                'class': 'inputxt',
                'ajaxurl': '/checksmscode/'
            }
        ),
    )

    def valiatetype(self, a):
        global msg
        if a == 2:
            msg = u"验证码错误!"
            self._errors["smscode"] = self.error_class([msg])

class ModfiyPW(forms.Form):
     password = forms.CharField(
        required=True,
        label=u"密码",
        error_messages={'required': u'请输入xin密码'},
        widget=forms.PasswordInput(
            attrs={
                'placeholder': u"密码",
                'type': 'password',
                'name': 'userpassword',
                'class': 'inputxt'
            }
        ),
     )
     password2 = forms.CharField(
        required=True,
        label=u"确认密码",
        error_messages={'required': u'再次输入xin密码'},
        widget=forms.PasswordInput(
            attrs={
                'placeholder': u"确认密码",
                'type': 'password',
                'name': 'userpassword2',
                'class': 'inputxt'
            }
        ),
     )

