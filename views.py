from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from models import BlogPost
from models import PushSubscriber
import datetime
import calendar
# Create your views here.
def view_post(request, post_id):
    template = loader.get_template('blog/post.html')
    post = BlogPost.objects.get(pk=post_id)
    context = {
        'post_title': post.title,
        'post_deck': post.deck,
        'post_header': post.img_name,
        'post_body': post.post_body,
        'date_published': post.publish_date,
        'post_img': post.img_name
    }
    return HttpResponse(template.render(context, request))

def index(request):
    template = loader.get_template('blog/front_page.html')
    tags = BlogPost.tags.most_common()[:5]
    tag = request.GET.get('tag', None)
    year = request.GET.get('year', None)
    month = request.GET.get('month', None)

    blog_years= {}
    for post in BlogPost.objects.filter(publish_date__lte=datetime.date.today()):
        if post.publish_date.year not in blog_years.keys():
            blog_years[post.publish_date.year] = list()
        if calendar.month_name[post.publish_date.month] not in blog_years[post.publish_date.year]:
            blog_years[post.publish_date.year].append(calendar.month_name[post.publish_date.month])

    if tag:
        if year:
            if month:
                month_num = list(calendar.month_abbr).index(str(month)[:3])
                less_than_date = datetime.date(int(year), month_num, get_days_in_month(int(year), month_num))
                greater_than_date = datetime.date(int(year), month_num, 1)
                posts = BlogPost.objects.order_by('publish_date').filter(tags__name__in=[tag], publish_date__lte=less_than_date, publish_date__gte=greater_than_date).reverse().values()
            else:
                less_than_date = datetime.date(int(year), 12, 31)
                greater_than_date = datetime.date(int(year), 1, 1)
                posts = BlogPost.objects.order_by('publish_date').filter(tags__name__in=[tag], publish_date__lte=less_than_date, publish_date__gte=greater_than_date).reverse().values()
        else:
            posts = BlogPost.objects.order_by('publish_date').filter(tags__name__in=[tag], publish_date__lte=datetime.date.today()).reverse().values()
    else:
        if year:
            if month:
                month_num = list(calendar.month_abbr).index(str(month)[:3])
                less_than_date = datetime.date(int(year), month_num, get_days_in_month(int(year), month_num))
                greater_than_date = datetime.date(int(year), month_num, 1)
                posts = BlogPost.objects.order_by('publish_date').filter(publish_date__lte=less_than_date, publish_date__gte=greater_than_date).reverse().values()
            else:
                less_than_date = datetime.date(int(year), 12, 31)
                greater_than_date = datetime.date(int(year), 1, 1)
                posts = BlogPost.objects.order_by('publish_date').filter(publish_date__lte=less_than_date, publish_date__gte=greater_than_date).reverse().values()
        else:
            posts = BlogPost.objects.order_by('publish_date').filter(publish_date__lte=datetime.date.today()).reverse().values()

    context = {
        'posts': posts,
        'tags': tags,
        'blog_dates': blog_years
    }
    return HttpResponse(template.render(context, request))

def get_days_in_month(year, month):
    if month == 2:
        if year % 4 == 0:
            return 29
        else:
            return 28
    elif month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12:
        return 31
    else:
        return 30

def push_notifications(request, js):
    template = loader.get_template('store/push_notifications.js')
    html = template.render()
    return HttpResponse(html, content_type="application/x-javascript")

def add_subscriber(request):
    subscriberId = request.GET['subscriberId[]']
    newSubscriber = PushSubscriber(sub_id=subscriberId)
    newSubscriber.save()
    return HttpResponse('{"status": "success"}')

def remove_subscriber(request):
    subscriberId = request.GET['subscriberId[]']
    currentSubscriber = PushSubscriber.objects.get(sub_id=subscriberId)
    currentSubscriber.delete()
    return HttpResponse('{"status": "success"}')
