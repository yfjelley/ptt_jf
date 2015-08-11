# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse

from ddbid.conf import site_off
from bbs.forum.views import error


class SiteOff(object):

    def process_request(self, request):
        if (site_off) and (request.path != reverse('signin')) and (not request.user.is_superuser):
            return error(request, 'down for maintenace')
