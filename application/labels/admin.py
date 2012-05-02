from django.contrib import admin
import reversion
from sorl.thumbnail.admin import AdminImageMixin
from labels.models import DigitalLabel, CMSLabel, Image, Group


class CMSLabelInline(admin.StackedInline):
    model = CMSLabel


class ImageInline(AdminImageMixin, admin.TabularInline):
    model = Image
    inline_classes = ('collapse open',)
    fields = ('caption', 'image_file', 'position')
    extra = 0
    # define the sortable
    sortable_field_name = "position"


class DigitalLabelInline(admin.TabularInline):
    inline_classes = ('collapse open',)
    fields = ('museum_number', 'name', 'position',)
    extra = 0
    model = DigitalLabel
    # define the sortable
    sortable_field_name = "position"


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
    inlines = [
        DigitalLabelInline,
    ]

admin.site.register(DigitalLabel, DigitalLabelAdmin)
#admin.site.register(CMSLabel, CMSLabelAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Group, GroupAdmin)
