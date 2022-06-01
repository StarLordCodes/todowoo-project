from django.contrib import admin
from .models import Todo

# adding a class to customise how the admin can see the information in the model
# here created has automatically generated field value so is not visible, hence
# we are adding a custom class


class TodoAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)


admin.site.register(Todo, TodoAdmin)
