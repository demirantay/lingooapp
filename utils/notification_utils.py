

def get_unread_notifications(NotificationBase, current_basic_user_profile,
                             ObjectDoesNotExist):
    """checks if there are unread notifications of the current user"""
    # Get all of the notifications
    try:
        all_notifications = NotificationBase.objects.filter(
            notified_user=current_basic_user_profile
        ).order_by("-id")
    except ObjectDoesNotExist:
        all_notifications = None

    # check if the user has unread notifications
    has_unread_notifications = False

    for notification in all_notifications:
        if notification.is_read == False:
            has_unread_notifications = True
            break
        else:
            continue

    return has_unread_notifications
