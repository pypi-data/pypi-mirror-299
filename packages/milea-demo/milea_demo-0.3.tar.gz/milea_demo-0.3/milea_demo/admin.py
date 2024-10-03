from django.contrib import admin

from milea_base.admin import MileaAdmin

from .models import DefaultModal, Position, Tag

class PositionInline(admin.TabularInline):
    model = Position
    extra = 0
    min_num = 1


@admin.register(DefaultModal)
class DefaultModalAdmin(MileaAdmin):

    show_sysdata = True  # Zeigt die Systemfelder an (created, updated, ...)
    list_display = ('verbose_id', 'name', 'progress', 'is_active_badge')
    list_editable = ('name',)
    radio_fields = {'radio': admin.VERTICAL, }
    date_hierarchy = "created_at"

    inlines = [PositionInline, ]
    change_actions = ['set_to_active', 'set_to_inactive']

    fieldsets = (
        ("First Section", {
            'description': "This is a fancy description",
            'classes': ('col-lg-6',),
            'fields': (
                'name',
                ('email', 'url'),
                'text', 'decimal',
                'progress',
            ),
        }),
        ("Second Section", {
            'description': "This is another fancy description",
            'classes': ('col-lg-6',),
            'fields': (
                'image', 'date', 'time', 'timestamp',
                'radio', 'multiple', 'tags',
            ),
        }),
    )

    admin_fieldsets = (
        ("Administration", {
            'description': "This is displayed only to superusers",
            'classes': ('admin-fieldset col-12',),
            'fields': (
                'boolean', 'manager',
            ),
        }),
    )

@admin.register(Tag)
class TagAdmin(MileaAdmin):
    pass
