def delete_teacher_user_session(request):
    """
    deletes the teacher user's session values
    so that the users cannot see teacher panel
    """
    if "teacher_user_logged_in" in request.session:
        del request.session["teacher_user_logged_in"]
