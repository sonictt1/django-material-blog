import json
import requests
import secret_data
from django.http import HttpResponse

def notify_users_new_post_action(description='Send push notification to subscribers'):
    def notify_users_new_post(modeladmin, request, queryset):
        id_string_list = []
        for id in queryset.values_list('sub_id', flat=True):
            id_string_list.append(id)
        json_string = '{"registration_ids":'+json.dumps(id_string_list)+' }'
        r = requests.post('https://android.googleapis.com/gcm/send', headers = {'Authorization': 'key='+secret_data.GCM_AUTH_KEY, 'Content-Type': 'application/json'}, data=json_string)
        return HttpResponse(r.text + '<br>' + json_string)
    notify_users_new_post.short_description = description
    return notify_users_new_post
