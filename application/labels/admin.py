from django.contrib import admin
from digitallabels.labels.models import DigitalLabel, CMSLabel, Image

class DigitalLabelAdmin(admin.ModelAdmin):
    pass

class CMSLabelAdmin(admin.ModelAdmin):
    pass

class ImageAdmin(admin.ModelAdmin):
    pass

admin.site.register(DigitalLabel, DigitalLabelAdmin)
admin.site.register(CMSLabel, CMSLabelAdmin)
admin.site.register(Image, ImageAdmin)
