from django.contrib import admin
import models
# Register your models here.
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'publish_date')

admin.site.register(models.BlogPost, BlogPostAdmin)
