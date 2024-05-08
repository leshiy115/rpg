from django.contrib import admin
from announcement.models import Announcement, Comment



admin.site.register([Announcement, Comment])
