from django.contrib import admin
import reversion
from sorl.thumbnail.admin import AdminImageMixin
from labels.models import MuseumObject, CMSLabel, Image, DigitalLabel, Portal


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
    extra = 1
    model = MuseumObject
    # define the sortable
    sortable_field_name = "position"
    template = 'admin/object_inline/tabular.html'


class MuseumObjectAdmin(reversion.VersionAdmin):
    list_display = ('thumbnail_tag', 'object_number', 'museum_number',
                                            'name', 'artist_maker', 'place')
    list_display_links = ('object_number', 'museum_number', 'name',)
    list_per_page = 25
    list_selected_related = True
    list_filter = ('digitallabel',)
    search_fields = ['name', 'museum_number', 'object_number']
    save_on_top = True
    inlines = [
        ImageInline,
        CMSLabelInline,
    ]

    class Media:
        js = [
            '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            '/static/js/tinymce_setup.js',
        ]


class ImageAdmin(AdminImageMixin, reversion.VersionAdmin):
    pass


class DigitalLabelAdmin(reversion.VersionAdmin):
    save_on_top = True
    inlines = [
        MuseumObjectInline,
    ]


class PortalImageInline(AdminImageMixin, admin.TabularInline):
    inline_classes = ('collapse open',)
    fields = ('caption', 'image_file', 'position',)
    extra = 0
    model = Image
    # define the sortable
    sortable_field_name = "position"


class HistoricalImageInline(PortalImageInline):
    title = "Historical Context Images"
    verbose_name = "Historical Context Image"
    fk_name = "portal_historical"


class MainImageInline(PortalImageInline):
    title = "Main Images"
    verbose_name = "Main Image"
    fk_name = "portal_main"


class ObjectImageInline(PortalImageInline):
    title = "Object Images"
    verbose_name = "Object Image"
    fk_name = "portal_object"


class PortalAdmin(reversion.VersionAdmin):
    save_on_top = True
    inlines = [
        HistoricalImageInline,
        MainImageInline,
        ObjectImageInline
    ]

    class Media:
        js = [
            '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            '/static/js/tinymce_setup.js',
        ]


class PortalImageAdmin(AdminImageMixin, reversion.VersionAdmin):
    pass


admin.site.register(MuseumObject, MuseumObjectAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(DigitalLabel, DigitalLabelAdmin)
admin.site.register(Portal, PortalAdmin)
