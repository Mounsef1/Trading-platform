from django.contrib import admin
from .models import UserInterest, ArticleData

# Customizing the UserInterest model in the admin interface
@admin.register(UserInterest)
class UserInterestAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'company_name')  # Fields to display in list view
    search_fields = ('user__username', 'company_name')  # Add search functionality
    list_filter = ('user',)  # Filter by user in the admin panel
    ordering = ('user', 'company_name')  # Order by user and company name

# Customizing the ArticleData model in the admin interface
@admin.register(ArticleData)
class ArticleDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'interest', 'link', 'date')  # Fields to display in list view
    search_fields = ('interest__company_name', 'link')  # Enable searching by interest and link
    list_filter = ('date',)  # Filter by date in the admin panel
    ordering = ('-date',)  # Order by date, latest first
    readonly_fields = ('date',)  # Make date read-only to prevent manual editing
