from django.contrib import admin
from .models import Service,Category, Review

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    
admin.site.register(Category,CategoryAdmin)
admin.site.register(Service)
admin.site.register(Review)