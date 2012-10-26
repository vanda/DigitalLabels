from django.contrib import admin
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
import reversion
from sorl.thumbnail.admin import AdminImageMixin
from labels.filters import PortalListFilter
from labels.forms import EditMuseumObjectForm
from labels.models import MuseumObject, TextLabel, CMSLabel, Image, DigitalLabel, \
                            Portal, DigitalLabelObject, PortalObject, PortalTextLabel


class CMSLabelInline(admin.TabularInline):
    model = CMSLabel
    extra = 0
    inline_classes = ('collapse open',)


class ImageInline(AdminImageMixin, admin.TabularInline):
    model = Image
    inline_classes = ('collapse open',)
    fields = ('caption', 'image_file', 'position')
    extra = 0
    template = 'admin/image_inline/tabular.html'
    # define the sortable
    sortable_field_name = "position"


class RelationInline(admin.TabularInline):
    inline_classes = ('collapse open',)
    extra = 0
    sortable_field_name = "position"
    template = 'admin/objects_labels_inline/tabular.html'


class DigitalLabelObject(RelationInline):
    model = DigitalLabelObject
    fields = ('museumobject', 'position', 'gateway_object',)
    custom_radio = "gateway_object"


class PortalObject(RelationInline):
    model = PortalObject
    fields = ('museumobject', 'position',)


class PortalTextLabel(RelationInline):
    model = PortalTextLabel
    fields = ('textlabel', 'position', 'biography',)
    custom_radio = "biography"


class PortalAdmin(reversion.VersionAdmin):
    list_display = ('id', 'name', '_Labels', '_Objects')
    list_display_links = ('id', 'name',)
    search_fields = ['name']
    save_on_top = True
    filter_horizontal = ('timeout_images',)
    inlines = [
        PortalTextLabel,
        PortalObject,
    ]


class DigitalLabelAdmin(reversion.VersionAdmin):
    list_display = ('id', 'name', '_Objects')
    list_display_links = ('id', 'name',)
    search_fields = ['name']
    save_on_top = True
    filter_horizontal = ('timeout_images',)
    inlines = [
        DigitalLabelObject,
    ]


class ResponseChange(reversion.VersionAdmin):
    def response_change(self, request, obj):
        global referrer_model
        referrer_model = request.GET.get('referrer')
        referrer_pk = request.GET.get('bind')
        if request.GET.get('referrer') and request.GET.get('bind')\
        and not (request.POST.has_key("_continue") or request.POST.has_key("_saveasnew") or\
                request.POST.has_key("_addanother")):
            return HttpResponseRedirect(reverse('admin:labels_%s_change' % (referrer_model),
                                                args=(referrer_pk,)))
        elif request.GET.get('referrer') and request.GET.get('bind') and request.POST.has_key("_continue"):
            return HttpResponseRedirect(request.path + "?referrer=%s&bind=%s" % (referrer_model, referrer_pk))
        return super(ResponseChange, self).response_change(request, obj)


class MuseumObjectAdmin(ResponseChange):
    form = EditMuseumObjectForm

    list_display = ('thumbnail_tag', 'object_number', 'museum_number',
                                            'name', 'artist_maker', 'place')
    list_display_links = ('thumbnail_tag', 'object_number', 'museum_number', 'name',)
    list_per_page = 25
    list_selected_related = True
    list_filter = ('digitallabel', 'portal',)
    search_fields = ['name', 'museum_number', 'object_number', 'artist_maker']
    save_on_top = True
    inlines = [
        CMSLabelInline,
    ]

    class Media:
        js = [
            '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            '/static/js/tinymce_setup.js',
        ]


class TextLabelAdmin(ResponseChange):
    list_display = ('thumbnail_tag', 'title')
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


class ImageAdmin(AdminImageMixin, reversion.VersionAdmin):
    list_display = ('thumb', 'caption', 'object_link', 'label_link',)
    list_display_links = ('thumb',)
    list_selected_related = True
    list_filter = ('museumobject__digitallabel', PortalListFilter,)
    search_fields = ['caption', 'museumobject__name', 'textlabel__title', ]
    save_on_top = True


admin.site.register(Portal, PortalAdmin)
admin.site.register(DigitalLabel, DigitalLabelAdmin)
admin.site.register(MuseumObject, MuseumObjectAdmin)
admin.site.register(TextLabel, TextLabelAdmin)
admin.site.register(Image, ImageAdmin)
