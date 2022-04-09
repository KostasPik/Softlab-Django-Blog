from django.contrib.sitemaps import Sitemap
from posts.models import Post


class PostSitemap(Sitemap): # a sitemap helps boost SEO.
   changefreq = 'weekly'
   priority = 1

   def items(self):
       return Post.objects.filter(published=True).all()

   def lastmod(self, obj):
       return obj.updated