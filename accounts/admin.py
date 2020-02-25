from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserChangeForm, UserCreationForm
from .models import PlayMateUser as User, PhoneOTP, PmAuthToken, Profile

from django.utils.translation import gettext_lazy as _

admin.site.site_header = 'PLAYMATE Administration'
admin.site.site_title = 'PLAYNATE'


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (
        (None, {'fields': ('phone_number', 'otp')}),
        (_('Personal info'), {
         'fields': ('first_name', 'last_name', 'email')}),

        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number','otp'),
        }),
    )

    list_display = ('phone_number', 'email', 'first_name',
                    'last_name', 'otp','is_active')
    list_filter = ('is_active',)
    list_display_link = ('phone_number',
                         'first_name', 'last_name', 'email')
    search_fields = ('first_name', 'otp',
                     'last_name', 'email', 'phone_number')
    ordering = ('phone_number',
                'first_name', 'last_name', 'email')

    filter_horizontal = ()

    class Meta:
        model = User

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(UserAdmin, self).get_inline_instances(request, obj)


@admin.register(PhoneOTP)
class PhoneOTPAdmin(admin.ModelAdmin):
    class Meta:
        model = PhoneOTP

    list_display = ('phone_number', 'otp', 'created_at', 'expiry', 'validated', 'used')
    list_filter = ('phone_number', 'validated')
    list_display_link = ('phone_number', 'validated')
    search_fields = ('otp', 'phone_number')
    ordering = ('phone_number', 'otp', 'created_at', 'expiry', 'validated')


admin.site.register(PmAuthToken)


class ProfileAdmin(admin.ModelAdmin):
    class Meta:
        model = Profile

    list_display = ('user', 'display_name', )
    list_filter = ( 'body_type','height', 'gender', 'chat_gender', 'hookup', 'dating', 'description')
    list_display_link = ('user', 'display_name')
    search_fields = ('user', 'display_name', 'age')
    ordering = ('body_type', 'height', 'gender', 'chat_gender', 'hookup',
    'dating', 'description')
    

admin.site.register(Profile, ProfileAdmin)
