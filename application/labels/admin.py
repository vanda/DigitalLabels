from django.contrib import admin
from labels.models import DigitalLabel, CMSLabel, Image, Group

class CMSLabelInline(admin.StackedInline):
    model = CMSLabel

class ImageInline(admin.TabularInline):
    model = Image

class DigitalLabelAdmin(admin.ModelAdmin):
    inlines = [
        CMSLabelInline,
        ImageInline,
    ]

class CMSLabelAdmin(admin.ModelAdmin):
    pass

class ImageAdmin(admin.ModelAdmin):
    pass

class GroupAdmin(admin.ModelAdmin):
    filter_horizontal = ("digitallabels",)


admin.site.register(DigitalLabel, DigitalLabelAdmin)
#admin.site.register(CMSLabel, CMSLabelAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Group, GroupAdmin)
