from django.contrib import admin


from .models import Thread, ChatMessage, ChatList, Call, CallList


class ChatMessage(admin.TabularInline):
    model = ChatMessage


class ThreadAdmin(admin.ModelAdmin):
    inlines = [ChatMessage]

    class Meta:
        model = Thread

class ChatListAdmin(admin.ModelAdmin):
    list_display = ['user', 'counter']
    list_display_links = ['user', 'counter']
    list_filter = ['user', 'counter']
    search_field = ['user', 'counter', 'message']
    class Meta:
        model = ChatList

class CallAdmin(admin.ModelAdmin):
    list_display = ['thread', 
                    'call_type',
                
                    'started_at',
                    'ended_at',
                    'timestamp',
                    'size',]
    list_display_links = ['thread',]
    list_filter = ['call_type', 'size']
    search_field = ['thread']

    class Meta:
        model = Call


class CallListAdmin(admin.ModelAdmin):
    list_display = ['user', 'counter']
    list_display_links = ['user']
    search_field = ['user']

    class Meta:
        model = Call


admin.site.register(Thread, ThreadAdmin)
admin.site.register(ChatList, ChatListAdmin)
admin.site.register(Call, CallAdmin)
admin.site.register(CallList, CallListAdmin)
