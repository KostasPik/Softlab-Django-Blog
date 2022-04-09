from django.db import models
from django.db.models.expressions import OrderBy
from pyuploadcare.dj.models import ImageField
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse

# Create your models here.





class Tag(models.Model):    # categories that a post can belong to.
    name = models.CharField(max_length=20, unique=True) 
    slug = models.SlugField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=300, unique=True)
    slug = models.SlugField(max_length=300, unique=True, db_index=True, allow_unicode=True)
    meta_keywords = models.CharField(max_length=100, default='Coding, Blog Post, SoftLab, Tutorial')
    thumbnail = ImageField(blank=True, manual_crop="")
    tags = models.ManyToManyField(Tag, related_name="blog_tags", blank=True)
    snippet = models.TextField(max_length=255, blank=True)
    body = RichTextUploadingField(blank=True, null=True)
    published = models.BooleanField(default=True, db_index=True) # Should the post be visible to the public or is it a draft?
    premium = models.BooleanField(default=False, db_index=True) # Should only premium users be able to view the post?
    related_posts = models.ManyToManyField('self', blank=True, null=True) #realted posts to show at the end of the article.
    updated = models.DateField(auto_now=True)
    post_date = models.DateField(auto_now_add=True)
    post_time = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_details', args=[str(self.slug)])

    @property
    def comments_count(self):
        return Comment.objects.filter(post=self).count()

    class Meta:
       ordering = ['-post_time']
       indexes = [
            models.Index(fields=['slug','published']),
        ]
    




class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=1000, default='Anonymous', blank=True)
    email = models.EmailField(max_length=1000, blank=True)
    body = models.TextField(max_length=1000, blank=False)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='+') # parent comment because it might be a reply comment.
    post_date = models.DateField(auto_now_add=True)
    post_time = models.DateTimeField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    active = models.BooleanField(default=True) # do we want to show the comment to the public?


    @property
    def children(self):
        return Comment.objects.filter(parent=self, active=True).order_by('-post_time').all()
        

    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False



    class Meta:
        ordering = ('-post_time',)
        indexes = [
        models.Index(fields=['active']),
        ]

    def __str__(self):
        return f'Comment by {self.name} , on {self.post_date}'