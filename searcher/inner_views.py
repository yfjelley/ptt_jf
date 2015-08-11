# coding=utf-8
import datetime
import json
import random

from DjangoCaptcha import Captcha
from django.contrib import auth
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.http import HttpResponse
from django.template import RequestContext
from django.template.loader import get_template
from dateutil.relativedelta import relativedelta
from searcher.models import Bid, UserFilter, DimensionChoice


__author__ = 'pony'


def user_auth(request, username, password):
    user = auth.authenticate(username=username, password=password)
    ca = Captcha(request)
    if user is None:
        a = 2
    elif not user.is_active:
        a = 3
    else:
        auth.login(request, user)
        a = 1
    return a


def refresh_header(request, a):
    if a == 1:
        t = get_template('header.html')
        content_html = t.render(RequestContext(request))
        payload = {
            'content_html': content_html,
            'success': True
        }
        return HttpResponse(json.dumps(payload), content_type="application/json")
    else:
        response = HttpResponse()
        response['Content-Type'] = "text/javascript"
        response.write(a)
        return HttpResponse(response)


def combination_bid(amount, ctype):
    # date1 = datetime.datetime.now()
    global a
    if None == amount:
        if ctype == 1:
            a = Bid.objects.filter(income_rate__lte=8)
        elif ctype == 2:
            a = Bid.objects.filter(income_rate__lte=15, income_rate__gte=8)
        elif ctype == 3:
            a = Bid.objects.filter(income_rate__gte=15)
    else:
        if ctype == 1:
            a = Bid.objects.filter(amount__lte=amount, income_rate__lte=8)
        elif ctype == 2:
            a = Bid.objects.filter(amount__lte=amount, income_rate__lte=15, income_rate__gte=8)
        elif ctype == 3:
            a = Bid.objects.filter(amount__lte=amount, income_rate__gte=15)

    if len(a) >= 2:
        aa = random.sample(a, 2)
        cid = []
        term = []
        for t in aa:
            cid.append(str(t.id))
            if t.term != int(t.term):
                term.append(round(t.term, 2))
            else:
                term.append(int(t.term))
        c = {'ids': '&'.join(cid)}
        tmax = max(term)
        tmin = min(term)
        if tmax == tmin:
            c.update({'term': str(tmax)})
        else:
            c.update({'term': str(tmin) + '-' + str(tmax)})
        # print(c)

        # p = re.compile(r'0*()$')
        # print p.sub(r'\1', str(aa[0].term))

        # c.update({'term1': aa[0].term, 'term2': aa[1].term})
        c.update(dict(income_rate=(aa[0].income_rate + aa[1].income_rate) / 2))
        if ctype == 1:
            c.update({'name': '天天搜贷 保守型'})
        elif ctype == 2:
            c.update({'name': '天天搜贷 稳健型'})
        elif ctype == 3:
            c.update({'name': '天天搜贷 激进型'})
        c.update({'amount': (aa[0].amount + aa[1].amount)})
        if aa[0].ten_thousand_revenue and aa[1].ten_thousand_revenue:
            ten_thousand_revenue = aa[0].ten_thousand_revenue + aa[1].ten_thousand_revenue
        else:
            ten_thousand_revenue = aa[0].income_rate / 12 * aa[0].term * 10000 + aa[1].income_rate / 12 * aa[
                1].term * 10000
        c.update({'thousandincome': ten_thousand_revenue})
    else:
        c = None
    # date2 = datetime.datetime.now()
    # print(u'组合耗时' + str(ctype) + str((date2 - date1).seconds) + u'秒')
    return c


def fil_yield(results, cal_type, value1, value2):
    if cal_type == 1:
        return results.filter(income_rate__lte=value1)
    elif cal_type == 2:
        return results.filter(income_rate=value1)
    elif cal_type == 3:
        return results.filter(income_rate__gte=value1)
    elif cal_type == 4:
        return results.filter(income_rate__gte=value1, income_rate__lte=value2)
    elif cal_type == 0:
        return results


def fil_time(results, cal_type, value1, value2):
    if cal_type == 1:
        return results.filter(term__lte=value1)
    elif cal_type == 2:
        return results.filter(term=value1)
    elif cal_type == 3:
        return results.filter(term__gte=value1)
    elif cal_type == 4:
        return results.filter(term__gte=value1, term__lte=value2)
    elif cal_type == 0:
        return results


def fil_lz(results, cal_type, value1, value2):
    if cal_type == 0:
        return results
    elif cal_type == 2:
        if value1 == 1:
            return results.filter(transfer_claim='Y')
        else:
            return results.filter(transfer_claim='N')


def fil_capital(results, cal_type, value1, value2):
    if cal_type == 0:
        return results
    elif cal_type == 1:
        return results.filter(platform__capital__lte=value1)
    elif cal_type == 3:
        return results.filter(platform__capital__gte=value1)
    elif cal_type == 4:
        return results.filter(platform__capital__gte=value1, platform__capital__lte=value2)


def fil_online(results, cal_type, value1, value2):
    if cal_type == 0:
        return results
    elif cal_type == 1:
        return results.filter(platform__online_time__gte=datetime.date.today() + relativedelta(months=-int(value1)))
    elif cal_type == 3:
        return results.filter(platform__online_time__lte=datetime.date.today() + relativedelta(months=-int(value1)))
    elif cal_type == 4:
        return results.filter(platform__online_time__lte=datetime.date.today() + relativedelta(months=-int(value1)),
                              platform__online_time__gte=datetime.date.today() + relativedelta(months=-int(value2)))


def fil_type(results, cal_type, choice_name):
    if cal_type == 0:
        return results
    elif cal_type == 2:
        return results.filter(type=choice_name)


def fil_background(results, cal_type, choice_name):
    if cal_type == 0:
        return results
    elif cal_type == 2:
        return results.filter(platform__background=choice_name)


def get_user_filter(user):
    f_l = []
    f_list = UserFilter.objects.filter(user=user)
    if len(f_list) > 0:
        for f in f_list:
            k = str(f.choices)
            a = map(int, k.split(','))
            filters = DimensionChoice.objects.filter(id__in=a)
            f_l.append({'id': f.id, 'name': f.name, 'choices': k, 'filters': filters})
    return f_l


def data_filter(data, filters):  # queryset
    results = data
    for f in filters:
        if f.dimension.id == 1:
            results = fil_yield(results, f.cal_type, f.choice_value1, f.choice_value2)
        elif f.dimension.id == 2:
            results = fil_time(results, f.cal_type, f.choice_value1, f.choice_value2)
        elif f.dimension.id == 3:
            results = fil_lz(results, f.cal_type, f.choice_value1, f.choice_value2)
        elif f.dimension.id == 4:
            results = fil_capital(results, f.cal_type, f.choice_value1, f.choice_value2)
        elif f.dimension.id == 5:
            results = fil_online(results, f.cal_type, f.choice_value1, f.choice_value2)
        elif f.dimension.id == 6:
            results = fil_type(results, f.cal_type, f.choice_name)
        elif f.dimension.id == 7:
            results = fil_background(results, f.cal_type, f.choice_name)
    return results


def index_loading(amount, params, page):
    c_bs = combination_bid(amount, 1)
    c_wj = combination_bid(amount, 2)
    c_jj = combination_bid(amount, 3)
    c_result = [c_bs, c_wj, c_jj]
    dimensions = DimensionChoice.objects.all()
    if None == amount:
        results = Bid.objects.all().order_by("random_rank")
    else:
        results = Bid.objects.filter(amount__gte=amount).order_by("random_rank")
    if params is not None:
        a = params.split(',')
        filters = DimensionChoice.objects.filter(id__in=a)
        results = data_filter(results, filters)
    # random.shuffle(results)
    # results = results.order_by('?')
    ppp = Paginator(results, 5)
    last_page = ppp.page_range[len(ppp.page_range) - 1]
    try:
        results = ppp.page(page)
    except (EmptyPage, InvalidPage):
        results = ppp.page(ppp.num_pages)
    page_set = get_pageset(last_page, results.number)
    index_parts = {'dimensions': dimensions, 'results': results, 'c_result': c_result, 'last_page': last_page,
                   'page_set': page_set}
    return index_parts


def get_pageset(last_page, pagenum):
    page_set = []
    if pagenum <= 3:
        start = 0
        end = 6
    elif pagenum > last_page - 3:
        start = last_page - 4
        end = last_page + 1
    else:
        start = pagenum - 2
        end = pagenum + 3
    for i in range(start, end, 1):
        if i <= 0:
            pass
        elif i > last_page:
            break
        else:
            page_set.append(i)
    return page_set


def result_sort(data, sorttype, sortorder):
    if sorttype == u'1' and sortorder == u'1':
        o_string = "income_rate"
    elif sorttype == u'1' and sortorder == u'2':
        o_string = "-income_rate"
    elif sorttype == u'2' and sortorder == u'1':
        o_string = "term"
    elif sorttype == u'2' and sortorder == u'2':
        o_string = "-term"
    else:
        o_string = None
    if o_string:
        data = data.order_by(o_string)
    return data
