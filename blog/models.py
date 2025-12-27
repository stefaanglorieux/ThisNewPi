from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError

import uuid

STATUS = [
    ('0', 'Draft'),
    ('2', 'Published'),
]

class Topic(models.Models):
    title = models.Charfield(max_length=35)
    slug = models.Charfield(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name_plural = "Topic"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Topic, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

class Project(models.Model):
    title = models.Charfield(max_length=100, unique=True)
    billboard = models.ImageField(upload_to='media', blank=True, null=False)
    body = models.Textfield(blank=True, null=False)
    last_entry = models.DateTimeField(null=True, blank=True)
    slug = models.Charfield(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name_plural = "Projects"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Project, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
    
class Journal(models.Model):
    entrydate = models.DateField()
    title = models.CharField(max_length=100, unique=True)
    body = models.TextField()
    topic = models.ForeignKey(Topic, null=True, blank=True, on_delete=models.SET_NULL, related_name='journal_topic')
    from_project = models.ForeignKey(Project, null=True, blank=True, on_delete=models.SET_NULL, related_name='journal')
    status = models.CharField(max_length=1, choices=STATUS)
    slug = models.SlugField(max_length=120, blank=True, unique=True, default=uuid.uuid1) # default uuid, what does this mean?
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    published = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = "Journal Entries"
        ordering = ['-entrydate']




class Article(models.Model):
    title = models.CharField(max_length=100, unique=True)
    subtitle = models.CharField(max_length=120, blank=True, null=False)
    billboard = models.ImageField(upload_to='media', blank=True, null=False)
    blurb = models.TextField(max_length=200, blank=True, null=True)
    body = models.TextField(blank=True, null=False)
    topic = models.ForeignKey(Topic, null=True, on_delete=models.SET_NULL, related_name='article_topic') # What does related name mean?
    from_project = models.ForeignKey(Project, null=True, blank=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=1, choices=STATUS)
    slug = models.SlugField(max_length=100, blank=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    published = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True)

    class Meta:
        verbose_name_plural = "Articles"
        ordering = ['-published_at']

    @property
    def last_project_update(self)
        return self.from_project.last_entry
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        if self.from_project is not None: # Does this mean no update once article is created?
            if not self.last_project_update:
                self.from_project.last_entry = self.updated_at
                self.from_project.save()

        super(Article, self).save(*args, **kwargs)

    def attachedMedia(self):
        myId = self.id
        myArticle = Article.objects.get(pk=myId) #why not just get article from Self?
        image = myArticle.media_set.all()
        output = image[0].title
        return output

class Media(models.Model):
    title = models.CharField(max_length=100, unique=True)
    body = models.TextField(blank=True, null=True)
    media = models.ImageField(upload_to='media')
    linked_article = models.ForeignKey(Article, null=True, blank=True, on_delete=models.SET_NULL)
    linked_entry = models.ForeignKey(Journal, null=True, blank=True, on_delete=models.SET_NULL)
    slug = models.SlugField(max_Length=120)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name_plural = "Media"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Media, self).save(*args, **kwargs)

    def clean(self):
        # Media can only be linked to one thing
        if self.linked_article is not None and self.linked_entry is not None:
                raise ValidationError(_("Media can only be linked to one thing"))
        
    def __str__(self):
        return self.title