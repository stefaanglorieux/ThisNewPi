from django.contrib import admin
from datetime import datetime

from .models import Article, Journal, Media, Project, Topic
from django.http.response import HttpResponseRedirect

class JournalAdmin(admin.ModelAdmin):

    change_form_template = "content-admin/change_form.html"

    fieldsets = (
        (None, {
            'fields': ('title', 'body')
        }),
        ('Associations', {
            'classes': ('collapse',),
            'fields': ('topic', 'from_project', 'about_movie')
        }),
        ('Metadata', {
            'classes': ('collapse',),
            'fields': ('entrydate', 'published_at', 'published', 'slug', 'status')
        })
    )

    readonly_fields = ['status', 'published_at', 'published']
    prepopulated_fields = {"slug": ("title",)}
    exclude = ('created_at', 'updated_at', )

    def response_change(self, request, obj):
        if "_publish_content" in request.POST and obj.title and obj.body and not obj.published:
            obj.published_at = datetime.now()
            obj.entrydate = obj.published_at
            obj.status = '2' 
            obj.published = True
            obj.save()
            self.message_user(request, "This content is now published")
            return HttpResponseRedirect(".")
        return super().response_change(request, obj)

admin.site.register(Journal, JournalAdmin)

class ArticleAdmin(admin.ModelAdmin):

    change_form_template = "content-admin/change_form.html"

    fieldsets = (
        (None, {
            'fields': ('title', 'subtitle', 'billboard', 'blurb', 'body')
        }),
        ('Associations', {
            'classes': ('collapse',),
            'fields': ('topic', 'from_project')
        }),
        ('Metadata', {
            'classes': ('collapse',),
            'fields': ('published_at', 'published', 'slug', 'status')
        })
    )

    readonly_fields = ['status', 'published_at', 'published']
    prepopulated_fields = {"slug": ("title",)}
    exclude = ('created_at', 'updated_at', )

    def response_change(self, request, obj):
        if "_publish_content" in request.POST and obj.title and obj.body and obj.blurb and obj.billboard and not obj.published:
            obj.published_at = datetime.now()
            obj.status = '2' 
            obj.published = True
            obj.save()
            self.message_user(request, "This content is now published")
            return HttpResponseRedirect(".")
        return super().response_change(request, obj)

admin.site.register(Article, ArticleAdmin)

class MediaAdmin(admin.ModelAdmin):

    fieldsets = (
        (None, {
            'fields': ('title', 'media', 'body')
        }),
        ('Associations', {
            'classes': ('collapse',),
            'fields': ('linked_article', 'linked_entry')
        }),
        ('Metadata', {
            'classes': ('collapse',),
            'fields': ('slug',)
        })
    )

    prepopulated_fields = {"slug": ("title",)}
    exclude = ('created_at', 'updated_at', )

admin.site.register(Media, MediaAdmin)

class ProjectAdmin(admin.ModelAdmin):

    fieldsets = (
        (None, {
            'fields': ('title', 'billboard', 'body')
        }),
        ('Metadata', {
            'classes': ('collapse',),
            'fields': ('slug',)
        })
    )

    prepopulated_fields = {"slug": ("title",)}
    exclude = ('last_entry', 'created_at', 'updated_at', )

admin.site.register(Project, ProjectAdmin)


class TopicAdmin(admin.ModelAdmin):

    fieldsets = (
        (None, {
            'fields': ('title',)
        }),
        ('Metadata', {
            'classes': ('collapse',),
            'fields': ('slug',)
        })
    )

    prepopulated_fields = {"slug": ("title",)}
    exclude = ('created_at', 'updated_at', )

admin.site.register(Topic, TopicAdmin)
