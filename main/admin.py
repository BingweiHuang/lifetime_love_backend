from django.contrib import admin

# Register your models here.

from main.models.models import Literature
from main.models.models import Figure
from main.models.models import FigureCategory
from main.models.models import Category

admin.site.register(Literature)
admin.site.register(Figure)
admin.site.register(FigureCategory)
admin.site.register(Category)
