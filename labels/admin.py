from django.contrib import admin
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
import reversion
from sorl.thumbnail.admin import AdminImageMixin
from labels.filters import PortalListFilter
from labels.forms import MuseumObjectForm, ObjectReadObjNumbForm
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
    form = ObjectReadObjNumbForm
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


class MuseumObjectAdmin(reversion.VersionAdmin):
    form = MuseumObjectForm

    def response_change(self, request, model=None):
        if request.GET.get('referrer'):
            referrer_model = request.GET.get('referrer')
            return HttpResponseRedirect(reverse('admin:labels_%s_change' % (referrer_model),
                                                args=(getattr(model, referrer_model).pk,)))
        else:
            return HttpResponseRedirect('../')

    list_display = ('thumbnail_tag', 'object_number', 'museum_number',
                                            'name', 'artist_maker',
                                            'place', 'digital_label', '_portal')
    list_display_links = ('thumbnail_tag', 'object_number', 'museum_number', 'name',)
    list_per_page = 25
    list_selected_related = True
    list_filter = ('digitallabel', 'portal',)
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


class TextLabelAdmin(reversion.VersionAdmin):
    def response_change(self, request, model=None):
        if request.GET.get('referrer'):
            referrer_model = request.GET.get('referrer')
            return HttpResponseRedirect(reverse('admin:labels_%s_change' % (referrer_model),
                                                args=(getattr(model, referrer_model).pk,)))
        else:
            return HttpResponseRedirect('../')

    list_display = ('thumbnail_tag', 'title', '_portal')
    list_display_links = ('thumbnail_tag', 'title',)
    list_per_page = 25
    list_selected_related = True
    list_filter = ('portal',)
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
