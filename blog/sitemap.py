from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse
from django.db.models import Q
from blog.models import *


class StaticSitemap(Sitemap):
    priority = 0.7
    lastmod = None
    changefreq = "monthly"

    def items(self):
        return [
                "/",
                "/about/",
            ]

    def location(self, obj):
        return obj[0] if isinstance(obj, tuple) else obj


class BaseSitemap(Sitemap):
    priority = 0.5
    changefreq = "weekly"

    def location(self, obj):
        return obj.get_absolute_url(False)

    def lastmod(self, obj):
        return obj.modified or obj.created

class PostSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return Post.objects.filter(visibility=VISIBILITY_PUBLIC)

    def location(self, obj):
        return reverse('blog.views.detail', kwargs={'id': obj.id, 'slug': obj.slug})

class TagSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.4

    def items(self):
        return Tag.objects.all()

    def location(self, obj):
        return reverse('blog.views.listing', kwargs={'tag_slug': obj.slug})

class CategorySitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return Category.objects.all()

    def location(self, obj):
        return reverse('blog.views.listing', kwargs={'category_slug': obj.slug})

sitemaps = dict(
        static = StaticSitemap,
        posts = PostSitemap,
        tags = TagSitemap,
        categories = CategorySitemap
    )
