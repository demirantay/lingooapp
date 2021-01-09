# `Version 1.5.0`

## Design Summary

In this update I added the Voting System and Feedback System. In the voting part for now we only have a basci congress system where the users are able to create bills (user made feature requests) and the bills get voted to be built or not built by the community. The feedback system isa basic post mechanism where users create in order to give feedback to the development team.

## Frontend Updates

At this point there is no libraries or any other frontend framework implemented in the site. It uses vanilla html, css, javascript and uses Django template engine to display the data not JSON API format

Newly Additions to the template folder:

- For "Voting System" Template and Static directories named `basic_voting_sys`
   - Create Bill page
   - Landing Page
   - New Page
   - Passed Page
   - Read Bill Page
   - Shelved Page
   - Update Bill Page
- For "Feedback System" Template and Static directories named `basic_feedback`
  - Read Page
  - Landing Page

## Backend Updates

`basic_voting_sys` feature new models:

```python
# Bill Model
# -------------------
# A bill is a record that is createdd by the users and they are usually a
# request from the developers weather it is a feature request, a feature that
# they do not like ... etc
class Bill(models.Model):
    id = models.AutoField(primary_key=True)
    creation_date = models.DateField(default=timezone.now)
    sponsor = models.ForeignKey(BasicUserProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=True, blank=True)
    content = models.TextField(default="...", null=True, blank=True)
    STATUS_CHOICES = (
        ("voting", "voting"),
        ("passed", "passed"),
        ("shelved", "shelved"),
    )
    status = models.CharField(max_length=100, default="voting",
                              choices=STATUS_CHOICES)
    CATEGORY_CHOICES = (
        ("new_feature", "New Feature"),
        ("small_addition", "Small Addition"),
        ("feature_complaint", "Feature Complaint"),
        ("small_removal", "Small Removal"),
        ("feature_removal", "Feature Removal"),
    )
    category = models.CharField(max_length=100, default="new_feature",
                                choices=CATEGORY_CHOICES)
    karma = models.IntegerField(default=0)

    def __str__(self):
        return "Bill id: " + str(self.id)


# Bill Last Add Date
# ------------
# This model holds the bill last creaiton dates so that the user cannot create
# more than one bill in a single day to prevent spamming and brute force
class LastBillCreationDate(models.Model):
    id = models.AutoField(primary_key=True)
    user_profile = models.OneToOneField(BasicUserProfile, on_delete=models.CASCADE)
    creation_date = models.DateField(default=timezone.now, null=True, blank=True)

    def __str__(self):
        return "user: " + str(self.user_profile) + " | last creation: " + \
                str(self.creation_date)


# Bill Votes
# --------------
# This model holds the records for the user votes on the bills
class BillVote(models.Model):
    id = models.AutoField(primary_key=True)
    creation_date = models.DateField(default=timezone.now)
    voter = models.ForeignKey(BasicUserProfile, on_delete=models.CASCADE)
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    VOTE_CHOICES = (
        ("aye", "aye"),
        ("neutral", "neutral"),
        ("nay", "nay"),
    )
    vote = models.CharField(max_length=50, default="neutral",
                            choices=VOTE_CHOICES)

    def __str__(self):
        return "Voter: " + str(self.voter.user.username) + " | bill: " \
                + str(self.bill.id)


# Bill Update History
# -----------
# In this model the bills edit (update) history is archived
class BillUpdateHistory(models.Model):
    id = models.AutoField(primary_key=True)
    creation_date = models.DateField(default=timezone.now)
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=True, blank=True)
    content = models.TextField(default="...", null=True, blank=True)

    def __str__(self):
        return "Bill: " + str(self.bill)


# Bill Delete Request
# ---------
# The users cannot delete their bill if there is a vote other than their own
# account that is why they need to request it
class BillDeleteRequest(models.Model):
    id = models.AutoField(primary_key=True)
    creation_date = models.DateField(default=timezone.now)
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)

    def __str__(self):
        return "Delete id: " + str(self.id)

```

`basic_voting_sys` feature new views:

- Create Bill Page: (`basic_language_explore`) -- url path: `voting/congress/bill/create/`
- Post Bill Read Page: (`basic_read_bill`) -- url path: `voting/congress/bill/read/<int:bill_id>/`
- Post Update Page: (`basic_update_bill`) -- url path: `voting/congress/bill/update/<int:bill_id>/`
- Bill Landing Page: (`basic_bill_landing_page`) -- url path: `voting/congress/<int:page>/`
- Bill Passed Page: (`basic_bill_passed_page`) -- url path: `voting/congress/passed/<int:page>/`
- Bill Shelved Page: (`basic_bill_shelved_page`) -- url path: `voting/congress/shelved/<int:page>/`
- Bill New Page: (`basic_bill_new_page`) -- url path: `voting/congress/new/<int:page>/`


`basic_feedback` feature new models:

```python
# Feedback Model
# ----------------
# This is the model that the users can create feedbacks for the devs of theSite
class Feedback(models.Model):
    id = models.AutoField(primary_key=True)
    creation_date = models.DateField(default=timezone.now)
    user = models.ForeignKey(BasicUserProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=True, blank=True, default="...")
    content = models.TextField(default="...", null=True, blank=True)
    views = models.IntegerField(default=0)

    def __str__(self):
        return "Id: " + str(self.id) + " | user: " + str(self.user.username) \
               + " | title: " + self.title


# Feedback Dev Answer
# -----------------
# This model holds the records for the dev answers of the feedback models
class FeedbackDevAnswer(models.Model):
    id = models.AutoField(primary_key=True)
    creation_date = models.DateField(default=timezone.now)
    feedback = models.ForeignKey(Feedback, on_delete=models.CASCADE)
    content = models.TextField(default="...", null=True, blank=True)

    def __str__(self):
        return "Feedback ID: " + str(self.feedback.id)


# Feedback Comment
# -----------------
# This model holds the records for the feedback posts comments
class FeedbackComment(models.Model):
    id = models.AutoField(primary_key=True)
    creation_date = models.DateField(default=timezone.now)
    comment_owner = models.ForeignKey(BasicUserProfile, on_delete=models.CASCADE)
    feedback = models.ForeignKey(Feedback, on_delete=models.CASCADE)
    content = models.TextField(default="...", null=True, blank=True)
    karma = models.IntegerField(default=0)

    def __str__(self):
        return "Feedback ID: " + str(self.feedback.id) + " | Comment ID: " \
               + str(self.id)


# Feedback Comment Reply
# ------------------
# This model holds the records for the replies for the feedback comments
class FeedbackCommentReply(models.Model):
    id = models.AutoField(primary_key=True)
    creation_date = models.DateField(default=timezone.now)
    comment = models.ForeignKey(FeedbackComment, on_delete=models.CASCADE)
    feedback = models.ForeignKey(Feedback, on_delete=models.CASCADE,
                                 null=True, blank=True)
    reply_owner = models.ForeignKey(BasicUserProfile, on_delete=models.CASCADE)
    content = models.TextField(default="...", null=True, blank=True)

    def __str__(self):
        return "Feedback ID: " + str(self.feedback.id) + " | Comment ID: " \
               + str(self.comment.id) + " | Reply ID: " + str(self.id)

```

`basic_feedback` feature new views:

- Feedback Landing Page: (`basic_feedback_landing_page`) -- url path: `feedback/<int:page>/`
- Feedback Read Page: (`basic_feedback_read`) -- url path: `feedback/read/<int:feedback_id>/`


## DevOps Updates

At this version I haven't implemented anything regarding DevOps.

## Mobile Updates

At this version I haven't implemented anything regarding mobile.

## Security

I just scanned it with OWASP zap, I havent implemented anything at the moment.
