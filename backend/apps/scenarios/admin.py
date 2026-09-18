from django.contrib import admin
from .models import Scenario, ScenarioInput, ScenarioResult


class ScenarioInputInline(admin.TabularInline):
    model = ScenarioInput
    extra = 1


class ScenarioResultInline(admin.StackedInline):
    model = ScenarioResult
    can_delete = False


@admin.register(Scenario)
class ScenarioAdmin(admin.ModelAdmin):
    list_display = ('name', 'commodity', 'status', 'created_by', 'created_at')
    list_filter = ('commodity', 'status')
    search_fields = ('name', 'description')
    inlines = [ScenarioInputInline, ScenarioResultInline]
