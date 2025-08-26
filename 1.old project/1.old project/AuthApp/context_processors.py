# AuthApp/context_processors.py

def unread_notifications(request):
    if request.user.is_authenticated:
        try:
            unread_count = request.user.notifications.filter(is_read=False).count()
        except Exception:
            unread_count = 0
    else:
        unread_count = 0
    return {
        'unread_notifications_count': unread_count
    }
