from django.conf import settings
from django.contrib import admin
from django_mptt_admin.admin import DjangoMpttAdmin
from mptt.admin import DraggableMPTTAdmin
from .models import Post, Category, Genre, Country


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


# @admin.register(Category)
# class CategoryAdmin(MPTTModelAdmin):
#     prepopulated_fields = {"slug": ("title",)}


admin.site.register(Genre, DraggableMPTTAdmin,
                    list_display=('tree_actions', 'indented_title',),
                    list_display_links=('indented_title',),
                    )

admin.site.register(Category, DraggableMPTTAdmin,
                    list_display=('tree_actions', 'indented_title',),
                    list_display_links=('indented_title',),
                    )


class ContinentFilter(admin.SimpleListFilter):
    title = "continent"
    parameter_name = "continent"

    def lookups(self, request, model_admin):
        continents = Country.objects.filter(level=1).order_by("name")

        return [(c.name, c.name) for c in continents]

    def queryset(self, request, queryset):
        value = self.value()

        if not value:
            return queryset
        else:
            continent = Country.objects.get(name=value, level=1)

            return continent.get_descendants(include_self=True)


class CountryAdmin(DjangoMpttAdmin):
    tree_auto_open = 0
    list_display = ("code", "name")
    ordering = ("name",)
    list_filter = (ContinentFilter,)

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def get_tree_animation_speed(self):
        if getattr(settings, "DJANGO_TESTING", False):
            return 0
        else:
            return None

    def get_tree_mouse_delay(self):
        if getattr(settings, "DJANGO_TESTING", False):
            return 0
        else:
            return None


admin.site.register(Country, CountryAdmin)
