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
                'class': 'inputxt',
                'ajaxurl': '/checkuser/'
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
                'ajaxurl': '/checkvcode/'
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
            msg = u"用户名和密码不匹配！"
            self._errors["username"] = self.error_class([msg])
        elif a == 3:
            msg = u"用户被锁定"
            self._errors["username"] = self.error_class([msg])
        elif a == 4:
            msg = u"验证码错误"
            self._errors["vcode"] = self.error_class([msg])


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
                'ajaxurl': '/checkvcode/'
            }
        ),
    )
    extend = forms.CharField(
        required=False,
        label=u"邀请码",
        error_messages={'required': u'请输入邀请码'},
        widget=forms.TextInput(
            attrs={
                'placeholder': u"没有可以不填",
                'type': 'text',
                'name': 'extend',
                'class': 'inputxt',
                #'ajaxurl': ''
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
        fields = ('cate','nickname', 'gender', 'birthday', 'cellphone', 'email', 'city', 'address', 'education',
                  'monthly_income', 'marriage', 'qq_num', 'wechat_num', 'weibo_num')
        widgets = {
            'cate': forms.Select(attrs={'class': 'user_select'}),
            'nickname': forms.TextInput(attrs={'class': 'user_text'}),
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

class ModfiyPForm(forms.Form):
    username = forms.CharField(
        required=True,
        label=u"手机号",
        error_messages={'required': '请输入手机号'},
        widget=forms.TextInput(
            attrs={
                'placeholder': u"手机号",
                'type': 'text',
                'name': 'name',
                'class': 'inputxt',
                'ajaxurl': '/checkuser_phone/'
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
                'ajaxurl': '/checkvcode/'
            }
        ),
    )

    def valiatetype(self, a):
        global msg
        if a == 2:
            msg = u"验证码错误!"
            self._errors["smscode"] = self.error_class([msg])
    def valiatetype(self, a):
        global msg
        if a == 10:
            msg = u"修改密码成功!"
            self._errors["username"] = self.error_class([msg])

class ForgetPWForm(forms.Form):
    username = forms.CharField(
        required=True,
        label=u"手机号",
        error_messages={'required': '请输入手机号'},
        widget=forms.TextInput(
            attrs={
                'placeholder': u"手机号",
                'type': 'text',
                'name': 'name',
                'class': 'inputxt',
                'ajaxurl': '/checkuser/'
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
                'ajaxurl': '/checkvcode/'
            }
        ),
    )

    def valiatetype(self, a):
        global msg
        if a == 2:
            msg = u"验证码错误!"
            self._errors["smscode"] = self.error_class([msg])
    def valiatetype(self, a):
        global msg
        if a == 10:
            msg = u"修改密码成功!"
            self._errors["username"] = self.error_class([msg])

class ModfiyPWForm(forms.Form):
     password = forms.CharField(
        required=True,
        label=u"密码",
        error_messages={'required': u'请输入新密码'},
        widget=forms.PasswordInput(
            attrs={
                'placeholder': u"密码",
                'type': 'password',
                #'name': 'userpassword',
                'class': 'inputxt'
            }
        ),
     )
     password2 = forms.CharField(
        required=True,
        label=u"确认密码",
        error_messages={'required': u'再次输入新密码'},
        widget=forms.PasswordInput(
            attrs={
                'placeholder': u"确认密码",
                'type': 'password',
                #'name': 'userpassword2',
                'class': 'inputxt'
            }
        ),
     )
     def valiatetype(self, a):
        global msg
        if a == 2:
            msg = u"两次输入密码不一致!"
            self._errors["password2"] = self.error_class([msg])
     def valiatetype(self, a):
        global msg
        if a == 3:
            msg = u"请重新输入密码!"
            self._errors["password"] = self.error_class([msg])
     def valiatetype(self, a):
        global msg
        if a == 4:
            msg = u"密码修改成功!"
            self._errors["password"] = self.error_class([msg])

cate_choice = (('1', '在线金融',), ('2', '生活服务',),('3', '电子商务',),('4', '医疗',),('5', '互联网',),('6', '社交',),)
status_choice = (('1', '预热',), ('2', '众筹',),('3', '预热',))
class PublishForm(forms.Form):
    project = forms.CharField(
        required=True,
        label=u"项目名称",
        error_messages={'required': '请输入项目名称'},
        widget=forms.TextInput(
            attrs={
                'placeholder': u"",
                'type': 'text',
                'name': 'project',
                'class': 'xmcj_input',
            }
        ),
    )

    introduction = forms.CharField(
        required=True,
        label=u"项目简介",
        error_messages={'required': u'请输入项目简介'},
        widget=forms.TextInput(
            attrs={
                'placeholder': u"",
                'type': 'text',
                'name': 'introduction',
                'class': 'xmcj_input'
            }
        ),
    )

    description = forms.CharField(
        required=True,
        label=u"项目描述",
        error_messages={'required': u'请输入项目描述'},
        widget=forms.Textarea(
            attrs={
                'placeholder': u"",
                'type': 'textarea',
                'name': 'description',
                'class': 'xxms_input'
            }
        ),
    )

    category = forms.ChoiceField(
        label=u"行业领域",
        choices= cate_choice,
        widget=forms.Select(
             attrs={
                'type': 'select',
                'name': 'category',
                'class': 'xmly_input',
            }
         ),
    )

    status = forms.ChoiceField(
        label=u"项目阶段",
        choices= status_choice,
        widget=forms.Select(
            attrs={
                'type': 'select',
                'name': 'status',
                'class': 'xmjd_input'
            }
        ),
    )

    founder = forms.CharField(
        required=True,
        label=u"项目创始人",
        error_messages={'required': u'请输入项目创始人'},
        widget=forms.TextInput(
            attrs={
                'placeholder': u"",
                'type': 'text',
                'name': 'founder',
                'class': 'xmcj_input'
            }
        ),
    )

    def valiatetype(self, a):
        global msg
        if a == 2:
            msg = u"请输入项目名称"
            self._errors["project"] = self.error_class([msg])
        elif a == 3:
            msg = u"请输入项目简介"
            self._errors["introduction"] = self.error_class([msg])
        elif a == 4:
            msg = u"请输入项目描述"
            self._errors["description"] = self.error_class([msg])
        elif a == 5:
            msg = u"请输入项目创始人"
            self._errors["founder"] = self.error_class([msg])


