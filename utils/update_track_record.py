def update_track_record(current_record, LessonTrackRecord, current_basic_user_profile):
    """updates the profile track record"""
    # chekc if record exists, if it doesn't create a new record
    if current_record == None:
        new_record = LessonTrackRecord(
            user=current_basic_user_profile,
            amount=1,
        )
        new_record.save()
    else:
        # if it exists just update it.
        current_record.amount += 1
        current_record.save()
