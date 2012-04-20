from django.contrib import admin
from labels.models import DigitalLabel, CMSLabel, Image

class CMSLabelInline(admin.TabularInline):
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



admin.site.register(DigitalLabel, DigitalLabelAdmin)
admin.site.register(CMSLabel, CMSLabelAdmin)
admin.site.register(Image, ImageAdmin)
