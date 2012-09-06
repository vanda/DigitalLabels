from django.contrib import admin
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
import reversion
from sorl.thumbnail.admin import AdminImageMixin
from labels.filters import PortalListFilter
from labels.forms import EditMuseumObjectForm
from labels.models import MuseumObject, TextLabel, CMSLabel, Image, DigitalLabel, Portal


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
    form = EditMuseumObjectForm
    inline_classes = ('collapse open',)
    extra = 0
    model = MuseumObject
    template = 'admin/objects_labels_inline/tabular.html'

class MuseumObject_dl_Inline(MuseumObjectInline):
    fields = ('object_number', 'name', 'gateway_object', 'dl_position',)
    ordering = ['dl_position']
    # define the sortable
    sortable_field_name = "dl_position"
    custom_radio = "gateway_object"

class MuseumObject_pt_Inline(MuseumObjectInline):
    fields = ('object_number', 'name', 'pt_position',)
    ordering = ['pt_position']
    # define the sortable
    sortable_field_name = "pt_position"


class TextLabelInline(admin.TabularInline):
    inline_classes = ('collapse open',)
    fields = ('title', 'position', 'biography',)
    extra = 0
    model = TextLabel
    # define the sortable
    sortable_field_name = "position"
    custom_radio = "biography"
    template = 'admin/objects_labels_inline/tabular.html'


class ResponseChange(reversion.VersionAdmin):
    def response_change(self, request, obj):
        if request.GET.get('referrer')\
        and not (request.POST.has_key("_continue") or request.POST.has_key("_saveasnew") or\
                request.POST.has_key("_addanother")):
            referrer_model = request.GET.get('referrer')
            return HttpResponseRedirect(reverse('admin:labels_%s_change' % (referrer_model),
                                                args=(getattr(obj, referrer_model).pk,)))
        return super(ResponseChange, self).response_change(request, obj)

class MuseumObjectAdmin(ResponseChange):
    form = EditMuseumObjectForm

    list_display = ('thumbnail_tag', 'object_number', 'museum_number',
                                            'name', 'artist_maker',
                                            'place', 'digital_label', '_portal')
    list_display_links = ('thumbnail_tag', 'object_number', 'museum_number', 'name',)
    list_per_page = 25
    list_selected_related = True
    list_filter = ('digitallabel', 'portal',)
    exclude = ('gateway_object', 'dl_position', 'pt_position')
    search_fields = ['name', 'museum_number', 'object_number', 'artist_maker']
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


class TextLabelAdmin(ResponseChange):
    list_display = ('thumbnail_tag', 'title', '_portal')
    list_display_links = ('thumbnail_tag', 'title',)
    list_per_page = 25
    list_selected_related = True
    list_filter = ('portal',)
    exclude = ('biography', 'position',)
    search_fields = ['title']
    save_on_top = True
    inlines = [
        ImageInline,
    ]

    class Media:
        js = [
            '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            '/static/js/tinymce_setup.js',
        ]


class CMSLabelAdmin(reversion.VersionAdmin):
    pass


class ImageAdmin(AdminImageMixin, reversion.VersionAdmin):
    list_display = ('thumb', 'caption', 'object_link', 'label_link',)
    list_display_links = ('thumb',)
    list_selected_related = True
    list_filter = ('museumobject__digitallabel', PortalListFilter,)
    search_fields = ['caption', 'museumobject__name', 'textlabel__title', ]
    save_on_top = True


class DigitalLabelAdmin(reversion.VersionAdmin):
    list_display = ('id', 'name', '_Objects')
    list_display_links = ('id', 'name',)
    search_fields = ['name']
    save_on_top = True
    filter_horizontal = ('timeout_images',)
    inlines = [
        MuseumObject_dl_Inline,
    ]

class PortalAdmin(reversion.VersionAdmin):
    list_display = ('id', 'name', '_Labels', '_Objects')
    list_display_links = ('id', 'name',)
    search_fields = ['name']
    save_on_top = True
    filter_horizontal = ('timeout_images',)
    inlines = [
        TextLabelInline,
        MuseumObject_pt_Inline,
    ]

admin.site.register(MuseumObject, MuseumObjectAdmin)
#admin.site.register(CMSLabel, CMSLabelAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(DigitalLabel, DigitalLabelAdmin)
admin.site.register(Portal, PortalAdmin)
admin.site.register(TextLabel, TextLabelAdmin)
