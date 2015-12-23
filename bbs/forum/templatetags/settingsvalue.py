__author__ = 'TianShuo'
from django import template
from ddbid import settings
from ddbid import conf

register = template.Library()


'''
usage:
first
    {% load settingsvalue %}
then
   {% settings_value "MAX_UPLOAD_SIZE" %}
   or
    {% settings_value "logoname" %}

'''

@register.simple_tag
def settings_value(name):
    return getattr(settings, name, "")

@register.simple_tag
def conf_value(name):
    return getattr(conf, name, "")


def phone_cut(name):
    return ''.join([name[0:3],'****',name[-4:]]).strip()
register.filter(phone_cut)

def multiplicative_page(page):
    return (int(page)-1)*18
register.filter(multiplicative_page)

def title_cut(title):
    return title[0:8]
register.filter(title_cut)


@register.filter(is_safe=False)
def add_filter(value, arg):
    return len(value) + len(arg)

