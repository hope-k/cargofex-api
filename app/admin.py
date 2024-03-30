from django.contrib import admin
from users.models import User
from django.contrib.auth.admin import UserAdmin
from . import models
from django.db.models import F, Case, When

admin.site.site_header = "LOGISTICS ADMIN"
admin.site.register(models.LogisticCompany)


@admin.register(User)
class AuthUserAdmin(UserAdmin):
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
    )

    list_filter = ("is_staff", "is_active")
    search_fields = ("username", "email", "first_name", "last_name")
    ordering = ("username",)


@admin.register(models.Tracking)
class TrackingAdmin(admin.ModelAdmin):
    list_display = ("id","shipment", "message","status", "location", "updated_at", "created_at")
    list_display_links = ("shipment",)

    list_filter = ("shipment__tracking_number", "id")
    search_fields = ("shipment__id", "shipment__tracking_number")
    search_help_text = "Search by Package Tracking Number or ID"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(shipment__manager=request.user)


@admin.register(models.Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "tracking_number",
        "origin",
        "destination",
        "receiver_name",
        "receiver_phone",
    
        "created_at",
    )
    list_display_links = ("tracking_number",)
    list_filter = ("tracking_number",)
    search_fields = ("tracking_number",)
    search_help_text = "Search by Tracking Number"
    date_hierarchy = "created_at"

    # making manager readonly so users cant change it
    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return ()
        return ("manager",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(manager=request.user)
    
    def save_model(self, request, obj, form, change):
        if not obj.manager:
            obj.manager = request.user
        super().save_model(request, obj, form, change)

    # def get_exclude(self, request, obj=None):
    #     if request.user.is_superuser:
    #         return ()
    #     return ("manager",)

    # def get_fields(self, request, obj=None):
    #     fields = super().get_fields(request, obj)
    #     if not request.user.is_superuser:
    #         fields.remove("manager")
    #     return fields


# @admin.register(models.Item)
# class ItemAdmin(admin.ModelAdmin):
#     list_display = ("name", "shipment", "quantity", "weight")
#     search_fields = ("name",)
#     search_help_text = "Search by Package Item Name"
#     date_hierarchy = "shipment__created_at"

#     def get_queryset(self, request):
#         qs = super().get_queryset(request)
#         if request.user.is_superuser:
#             return qs
#         return qs.filter(shipment__manager=request.user)


@admin.register(models.Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("address", "city", "state", "country")
    search_fields = ("address", "city", "state", "country")
    search_help_text = "Search by Address, City, State or Country"
    list_filter = ("country", "state", "city")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(shipment_origin__manager=request.user)  

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["address"].help_text = (
            "Provide the complete address for the location."
        )
        form.base_fields["city"].help_text = (
            "Specify the city where the location is situated."
        )
        form.base_fields["state"].help_text = "Specify the state for the location."
        form.base_fields["country"].help_text = "Enter the country of the location."
        form.base_fields["latitude"].help_text = (
            "Provide the latitude coordinate for the location. Use decimal format."
        )
        form.base_fields["longitude"].help_text = (
            "Provide the longitude coordinate for the location. Use decimal format."
        )
        return form


@admin.register(models.Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "image",
    )
    search_fields = ("id", "name")
    search_help_text = "Search by Name or ID"
    list_filter = ("name",)

    # ! using delete_queryset() to delete images from cloudinary because the default delete_queryset() does not delete images from cloudinary
    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.image.storage.delete(obj.image.name)

        super().delete_queryset(request, queryset)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(shipment__manager=request.user)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["image"].help_text = "Upload the image for the shipment."
        return form
    
@admin.register(models.Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("title", "message", "created_at")
    search_fields = ("message",)
    search_help_text = "Search by Notification Message"
    date_hierarchy = "created_at"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(shipment__manager=request.user)
