from django.contrib.admin import SimpleListFilter
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from labels.models import Portal

class PortalListFilter(SimpleListFilter):
    title = 'portal'
    parameter_name = 'portal__id__exact'
    def lookups(self, request, model_admin):
        qs = Portal.objects.all().values_list('id', 'name')
        return [(str(x), y) for x, y in qs]

    def queryset(self, request, queryset):
        if self.value() is not None:
            return queryset.filter(
                                   Q(museumobject__portal__id__exact=self.value()) |
                                   Q(textlabel__portal__id__exact=self.value())
                                  )
        else:
            return queryset
