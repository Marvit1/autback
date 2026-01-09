from django.contrib import admin
from django.utils.html import format_html
from .models import Car, CarImage, CarTranslation


# ----------------------------
# Նկարների Inline (Preview-ով)
# ----------------------------
class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 3
    max_num = 10
    fields = ("image", "image_preview")
    readonly_fields = ("image_preview",)

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height:80px; border-radius:8px; box-shadow:0 2px 6px rgba(0,0,0,0.2);" />',
                obj.image.url
            )
        return "📷 Նկար չկա"

    image_preview.short_description = "Նախադիտում"


# ----------------------------
# Թարգմանությունների Inline
# ----------------------------
class CarTranslationInline(admin.TabularInline):
    model = CarTranslation
    extra = 1
    max_num = 3
    fields = ("language", "make", "model", "description")
    verbose_name = "Թարգմանություն"
    verbose_name_plural = "Թարգմանություններ"


# ----------------------------
# Car Admin (Գլխավոր)
# ----------------------------
@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = (
        "make",
        "model",
        "year",
        "price",
        "status",
        "mileage",
        "created_at",
    )

    list_editable = ("status",)
    list_filter = (
        "status",
        "make",
        "year",
        "fuel",
        "transmission",
        "color",
    )

    search_fields = (
        "make",
        "model",
        "year",
        "color",
    )

    ordering = ("-created_at",)
    date_hierarchy = "created_at"
    save_on_top = True

    inlines = [
        CarTranslationInline,
        CarImageInline,
    ]

    fieldsets = (
        ("🚗 Հիմնական տվյալներ", {
            "fields": ("make", "model", "year", "price", "status")
        }),
        ("⚙️ Տեխնիկական տվյալներ", {
            "fields": ("fuel", "transmission", "mileage", "color"),
            "classes": ("collapse",),
        }),
    )


# ----------------------------
# Առանձին CarImage Admin
# ----------------------------
@admin.register(CarImage)
class CarImageAdmin(admin.ModelAdmin):
    list_display = ("car", "image_preview")
    list_filter = ("car__make", "car__model")
    search_fields = ("car__make", "car__model")
    readonly_fields = ("image_preview",)

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height:60px; border-radius:6px;" />',
                obj.image.url
            )
        return "Նկար չկա"

    image_preview.short_description = "Նախադիտում"
