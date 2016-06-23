from django.contrib import admin
from actions import notify_users_new_post_action
import models
# Register your models here.
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'publish_date')

admin.site.register(models.BlogPost, BlogPostAdmin)

class PushSubscriberAdmin(admin.ModelAdmin):
    actions = [notify_users_new_post_action()]

admin.site.register(models.PushSubscriber, PushSubscriberAdmin)
