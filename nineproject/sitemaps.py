from django.contrib import sitemaps
from django.urls import reverse
from  nineapp.models import Post

class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ["indexpage","reg","signin",  "logout", "reset_password",  "contact", "page_not_found",    ]

    def location(self, item):
        return reverse(item)


class DynamicPostSiteMap(sitemaps.Sitemap):
    priority = 1.0
    changefreq = 'daily'

    def items(self):
        return Post.objects.all()

    def location(self, obj):
        return obj.get_absolute_url()

    def lastmod(self, obj):
        return obj.modified
