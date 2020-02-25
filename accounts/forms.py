from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from django.utils.translation import gettext_lazy as _

from .models import PlayMateUser, PhoneOTP


class LoginForm(forms.Form):
    phone_number = forms.IntegerField(label='Phone Number')
    otp = forms.IntegerField(label='otp')


class VerifyForm(forms.Form):
    key = forms.IntegerField(label='Enter OTP')


class RegisterForm(forms.ModelForm):

    class Meta:
        model = PlayMateUser
        fields = 'phone_number', 'otp'

    def clean_phone(self):
        phone_number = self.cleaned_data['phone_number']
        qs = PlayMateUser.objects.filter(phone_number=phone_number)
        if qs.exists():
            raise forms.ValidationError('Phone number is Taken')
        return phone_number

    def validate_otp(self):
        otp = self.cleaned_data['otp']
        phone_number = self.cleaned_data['phone_number']
        phone_otp = PhoneOTP.objects.filter(otp=otp, phone_number=phone_number)

        if phone_otp.exists():
            phone_otp = phone_otp.first()
            if phone_otp.validate:
                return otp
            raise forms.ValidationError('Validate OTP')
        raise forms.ValidationError('Re enter phone')


class TempRegisterForm(forms.Form):
    phone = forms.IntegerField()
    otp = forms.IntegerField()


class UserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given phone number and
    otp.
    """
    error_messages = {
        'password_mismatch': _("The otp didn't match."),
    }


    class Meta:
        model = PlayMateUser
        fields = "phone_number",

 
    def validate_otp(self):
        otp = self.cleaned_data['otp']
        phone_number = self.cleaned_data['phone_number']
        phone_otp = PhoneOTP.objects.filter(otp=otp, phone_number=phone_number)

        if phone_otp.exists():
            phone_otp = phone_otp.first()
            if phone_otp.validate:
                return otp
            raise forms.ValidationError('Validate OTP')
        raise forms.ValidationError('Re enter phone')

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_unusable_password()
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):

    class Meta:
        model = PlayMateUser
        fields = '__all__'

