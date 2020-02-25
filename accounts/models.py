from django.contrib import auth
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from knox import crypto
from knox.settings import CONSTANTS, knox_settings

from future.backports.datetime import timedelta



def update_last_login(sender, user, **kwargs):
    """
    A signal receiver which updates the last_login date for
    the user logging in.
    """
    user.last_login = timezone.now()
    user.save()


class PlayMateUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, phone_number, otp, **extra_fields):
        """
        Create and save a user with the given phone number and password.
        """
        if not phone_number:
            raise ValueError('The given phone number must be set')

        phone_number = self.model.normalize_username(phone_number)
        user = self.model(phone_number=phone_number, otp=otp, **extra_fields)
        user.set_unusable_password()
        user.save(using=self._db)
        return user, True

    def create_user(self, phone_number, otp, **extra_fields):
        return self._create_user(phone_number, otp, **extra_fields)



class PlayMateUser(AbstractBaseUser):
    phone_number = models.CharField(_('Phone number'), max_length=15, unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True, null=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), blank=True, null=True)
    otp = models.CharField(_('otp'), max_length=6, blank=True)

    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)


    objects = PlayMateUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_phone_number(self):
        return self.phone_number
        

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    # def save(self, *args, **kwargs):
    #     print(dir(self))
    #     self.save_base()
    #     # try:
    #     #     self.save_base()
    #     # except:
    #     #     self.save()

        

class PhoneOTPManager(models.Manager):
    def create(self, phone_number, otp):
        phone_otp = self.model(phone_number=phone_number, otp=otp)
        expiry = timezone.now() + timedelta(minutes=2)
        phone_otp.expiry = expiry
        phone_otp.save()
        return phone_otp
        

class PhoneOTP(models.Model):
    # phone_regex = RegexValidator(regex=r'^\+?234?\d(9,14)$',
    #     message="Phone number must be entered in format of +2348044234244 up to 14 digits")
    # phone = models.CharField(validator=[phone_regex], max_length=15, unique=True)
    phone_number = models.CharField(max_length=15)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expiry = models.DateTimeField(null=True, blank=True)
    validated = models.BooleanField(default=False)
    used = models.BooleanField(default=False)

    objects = PhoneOTPManager()

    def __str__(self):
        return f'{self.phone_number} is sent {self.otp}'


class PmAuthTokenManager(models.Manager):
    def create(self, user, expiry=knox_settings.TOKEN_TTL):
        token = crypto.create_token_string()
        salt = crypto.create_salt_string()
        digest = crypto.hash_token(token, salt)

        if expiry is not None:
            expiry = timezone.now() + expiry

        instance = super(PmAuthTokenManager, self).create(
            token_key=token[:CONSTANTS.TOKEN_KEY_LENGTH], digest=digest,
            salt=salt, user=user, expiry=expiry)
        return instance, token


class PmAuthToken(models.Model):
    
    objects = PmAuthTokenManager()

    digest = models.CharField(
        max_length=CONSTANTS.DIGEST_LENGTH, primary_key=True)
    token_key = models.CharField(
        max_length=CONSTANTS.TOKEN_KEY_LENGTH, db_index=True)
    salt = models.CharField(
        max_length=CONSTANTS.SALT_LENGTH, unique=True)
    user = models.ForeignKey(PlayMateUser, null=False, blank=False,
                             related_name='auth_token_set', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    expiry = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return '%s : %s' % (self.digest, self.user)


class Profile(models.Model):
    user = models.OneToOneField(PlayMateUser, related_name="user_profile", on_delete=models.CASCADE)
    display_name = models.CharField(max_length=50, null=True, blank=True)
    chatDistance = models.IntegerField(default=10)
    gender = models.CharField(max_length=6, null=True, blank=True)
    chat_gender = models.CharField(max_length=6, null=True, blank=True)
    description = models.CharField(max_length=100, null=True, blank=True)
    age = models.CharField(max_length=4, null=True, blank=True)
    height = models.CharField(max_length=4, null=True, blank=True)
    body_type = models.CharField(max_length=15, null=True, blank=True)
    dating = models.BooleanField(default=False)
    hookup = models.BooleanField(default=False)
    image = models.ImageField(upload_to='profile_image', blank=True)


def create_profile(sender, instance, *arg, **kwargs):
    return Profile.objects.get_or_create(user=instance)

post_save.connect(create_profile, sender=PlayMateUser)
