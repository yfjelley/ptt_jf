from django.contrib import admin
from searcher.models import UserFavorite, Bid, FilterDimension, DimensionChoice, \
    UserFilter, ReminderUnit, UserReminder, CombBidType, WeekHotSpot,UserInformation,Project,\
    invest_detail,project_forum,Signal,RegistrationAgreement,About_us,Partners,Frendlink


class FilterDimensionAdmin(admin.ModelAdmin):
    list_display = ('id', 'dimensionname', 'add_date', 'modify_date')


class DimensionChoiceAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'dimension', 'choice_name', 'choice_value1', 'choice_value2', 'cal_type', 'add_date', 'modify_date')


class UserFilterAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'filter_order', 'choices', 'add_date', 'modify_date')


class WeekHotSpotAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'url', 'status', 'add_date', 'modify_date')


#admin.site.register(UserFavorite)

#admin.site.register(FilterDimension, FilterDimensionAdmin)
#admin.site.register(DimensionChoice, DimensionChoiceAdmin)
#admin.site.register(UserFilter, UserFilterAdmin)
#admin.site.register(ReminderUnit)
#admin.site.register(UserReminder)
admin.site.register(About_us)
admin.site.register(UserInformation)
admin.site.register(Project)
admin.site.register(invest_detail)
admin.site.register(project_forum)
admin.site.register(Signal)
admin.site.register(RegistrationAgreement)
admin.site.register(Partners)
admin.site.register(Frendlink)


