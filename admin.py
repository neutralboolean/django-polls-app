from django.contrib import admin

from .models import Choice, Question

# Register your models here.

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filters = ['pub_date']
    field_sets = [
        (None,			{'fields': ['question_text']}),
        ('Date Information',	{'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    search_filters = ['question_text']


admin.site.register(Question, QuestionAdmin)
