from django.contrib import admin
from .models import Question, Choices

class ChoiceInline(admin.StackedInline):
    model = Choices
    extra: 3

class QuestionAdmin(admin.ModelAdmin):
    fields = ['pub_date', 'questiontext']
    inlines = [ChoiceInline]
    list_display = ('questiontext', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['questiontext']

admin.site.register(Question, QuestionAdmin)