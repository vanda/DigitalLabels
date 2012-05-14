from django.contrib import admin
import reversion
from sorl.thumbnail.admin import AdminImageMixin
from labels.models import MuseumObject, CMSLabel, Image, DigitalLabel


class CMSLabelInline(admin.TabularInline):
    model = CMSLabel
    extra = 0
    inline_classes = ('collapse open',)


class ImageInline(AdminImageMixin, admin.TabularInline):
    model = Image
    inline_classes = ('collapse open',)
    fields = ('caption', 'image_file', 'position')
    extra = 0
    # define the sortable
    sortable_field_name = "position"


class MuseumObjectInline(admin.TabularInline):
    inline_classes = ('collapse open',)
    fields = ('museum_number', 'name', 'gateway_object', 'position',)
    extra = 0
    model = MuseumObject
    # define the sortable
    sortable_field_name = "position"


class MuseumObjectAdmin(reversion.VersionAdmin):
    list_display = ('thumbnail_tag', 'museum_number', 'name')
    save_on_top = True
    inlines = [
        ImageInline,
        CMSLabelInline,
    ]


class CMSLabelAdmin(reversion.VersionAdmin):
    pass


class ImageAdmin(AdminImageMixin, reversion.VersionAdmin):
    pass


class DigitalLabelAdmin(reversion.VersionAdmin):
    save_on_top = True
    inlines = [
        MuseumObjectInline,
    ]

admin.site.register(MuseumObject, MuseumObjectAdmin)
#admin.site.register(CMSLabel, CMSLabelAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(DigitalLabel, DigitalLabelAdmin)
