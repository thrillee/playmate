from django.conf import settings
from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save

from accounts.models import PlayMateUser

from .utils import broadcast_msg_to_chat


class ThreadManager(models.Manager):
    def by_user(self, user):
        qlookup = Q(first=user) | Q(second=user)
        qlookup2 = Q(first=user) & Q(second=user)
        qs = self.get_queryset().filter(qlookup).exclude(qlookup2).distinct()
        return qs

    def get_or_new(self, user, other_user_id):  # get_or_create
        user_id = user.id
        if user_id == other_user_id:
            return None
        qlookup1 = Q(first__id=user_id) & Q(
            second__id=other_user_id)
        qlookup2 = Q(first__id=other_user_id) & Q(
            second__id=user_id)
        qs = self.get_queryset().filter(qlookup1 | qlookup2).distinct()
        if qs.count() == 1:
            return qs.first(), False
        elif qs.count() > 1:
            return qs.order_by('timestamp').first(), False
        else:
            Klass = user.__class__
            user2 = Klass.objects.get(id=other_user_id)
            if user != user2:
                obj = self.model(
                    first=user,
                    second=user2
                )
                obj.save()
                return obj, True
            return None, False


class Thread(models.Model):
    first = models.ForeignKey(
        PlayMateUser, on_delete=models.CASCADE, related_name='chat_thread_first')
    second = models.ForeignKey(
        PlayMateUser, on_delete=models.CASCADE, related_name='chat_thread_second')
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    confirm = models.BooleanField(default=True)
    objects = ThreadManager()

    @property
    def room_group_name(self):
        return f'chat_{self.id}'

    def broadcast(self, msg=None):
        if msg is not None:
            broadcast_msg_to_chat(
                msg, group_name=self.room_group_name, user='admin')
            return True
        return False


class ChatMessage(models.Model):
    thread = models.ForeignKey(
        Thread, null=True, blank=True, on_delete=models.CASCADE)
    user = models.ForeignKey(PlayMateUser,
                             verbose_name='sender', on_delete=models.CASCADE)
    message = models.CharField(max_length=10000, blank=True, null=True)
    image = models.ImageField(upload_to='chat-imgaes', null=True, blank=True)
    files = models.FileField(upload_to='chat-files', null=True, blank=True)
    status = models.CharField(default='sent', max_length=10)
    seen = models.BooleanField(default=False)
    sent_at = models.TimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)


class ChatList(models.Model):
    thread = models.ForeignKey(
        Thread, null=True, blank=True, on_delete=models.CASCADE)
    user = models.ForeignKey(PlayMateUser, on_delete=models.CASCADE)
    message = models.ForeignKey(ChatMessage, null=True, blank=True, on_delete=models.CASCADE)
    counter = models.IntegerField(default=0)


class Call(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    user = models.ForeignKey(PlayMateUser, on_delete=models.CASCADE)
    call_type = models.CharField(max_length=10)
    missed = models.BooleanField(default=False)
    available = models.BooleanField(default=True)
    started_at = models.TimeField(auto_now_add=True, null=True, blank=True,)
    ended_at = models.TimeField(auto_now=False, auto_now_add=False, null=True, blank=True,)
    timestamp = models.DateTimeField(auto_now_add=True)
    size = models.FloatField(default=0.0)


class CallList(models.Model):
    user = models.ForeignKey(PlayMateUser, on_delete=models.CASCADE)
    call = models.ForeignKey(Call, on_delete=models.CASCADE)
    info = models.CharField(max_length=10, null=True, blank=True)
    details = models.CharField(max_length=10, null=True, blank=True)
    counter = models.IntegerField(default=0)


def add_to_list(sender, instance, *args, **kwargs):
    first = ChatList.objects.get_or_create(user=instance.thread.first, thread=instance.thread)
    second = ChatList.objects.get_or_create(user=instance.thread.second, thread=instance.thread)

    first[0].message = instance
    first[0].counter += 1

    second[0].message = instance
    second[0].counter += 1

    first[0].save(), second[0].save()
    del first, second
    if not instance.seen:
        
        return 
    message = ChatList.objects.get(user=instance.user, message=instance.message)
    message.counter = 0
    message.save()
    return 





def add_to_call_log(sender, instance, *args, **kwargs):
    if instance.user == instance.thread.first:
        caller = CallList.objects.create(user=instance.user, call=instance)
        receiver = CallList.objects.create(
            user=instance.thread.second, call=instance)

        # receiver.call = instance
        # caller.call = instance

        caller.info = "Outgoing"
        receiver.info = "Incoming"
        
        if instance.missed:
            caller.detail = "Call declined"
            receiver.detail = "Missed Call"
        if instance.available:
            caller.detail = "Unavailable"
            receiver.detail = "Missed Call"

    else:
        caller = CallList.objects.create(user=instance.user, call=instance)
        receiver = CallList.objects.create(
            user=instance.thread.first, call=instance)
        caller.info = "Outgoing"
        receiver.info = "Incoming"

        # caller.call = instance
        # receiver.call = instance

        if instance.missed:
            caller.detail = "Call declined"
            receiver.detail = "Missed Call"
        if instance.available:
            caller.detail = "Unavailable"
            receiver.detail = "Missed Call"

    # print(caller.save(), receiver.save())
    caller.save(), receiver.save()







post_save.connect(add_to_list, sender=ChatMessage)
post_save.connect(add_to_call_log, sender=Call)
