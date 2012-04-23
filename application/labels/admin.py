from django.contrib import admin
import reversion
from sorl.thumbnail.admin import AdminImageMixin
from labels.models import DigitalLabel, CMSLabel, Image, Group

class CMSLabelInline(admin.StackedInline):
    model = CMSLabel

class ImageInline(AdminImageMixin, admin.TabularInline):
    model = Image

class DigitalLabelAdmin(reversion.VersionAdmin):
    save_on_top = True
    inlines = [
        CMSLabelInline,
        ImageInline,
    ]

class CMSLabelAdmin(reversion.VersionAdmin):
    pass

class ImageAdmin(AdminImageMixin, reversion.VersionAdmin):
    pass

class GroupAdmin(reversion.VersionAdmin):
    save_on_top = True
    filter_horizontal = ("digitallabels",)


admin.site.register(DigitalLabel, DigitalLabelAdmin)
#admin.site.register(CMSLabel, CMSLabelAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Group, GroupAdmin)
