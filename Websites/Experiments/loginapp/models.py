from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import logging
# Create your models here.

log = logging.getLogger(__name__)

class Registration(models.Model):
    user = models.OneToOneField(User)
    
    comment = models.CharField(max_length=35, null=True, default=None,blank=True)

    def __str__(self):
        return self.title

class EmailBody(models.Model):
	body_text = models.TextField()

class EmailThread(models.Model):
        title = models.TextField()
	parent_email = models.ForeignKey(EmailBody, related_name = 'current_email')
	child_email = models.ForeignKey(EmailBody, related_name = 'child_email',default = None, null=True, blank=True)

class KnowledgeSource(models.Model):        
	source_doc = models.TextField()

class Session_log(models.Model):
	user = models.ForeignKey(User)
	time_action = models.DateTimeField(default=timezone.now)
	START_ACTION = '_start'
    	END_ACTION = '_end'
	ACTION_CHOICES = (
		(START_ACTION, '_start'),
		(END_ACTION,'_end'),
	)
	session_action = models.CharField(choices = ACTION_CHOICES, default = START_ACTION ,max_length=255)

class Survey_response(models.Model):      
	q1 = models.TextField(null=True, default=None,blank=True)
	q2 = models.TextField(null=True, default=None,blank=True)
	q2_extended = models.TextField(null=True, default=None,blank=True)
	q3 = models.TextField(null=True, default=None,blank=True)
	q4 = models.TextField(null=True, default=None,blank=True)
	q4_extended = models.TextField(null=True, default=None,blank=True)

class Survey(models.Model):
	session = models.ForeignKey(Session_log)
	survey_response = models.ForeignKey(Survey_response)
	timestamp_survey_start = models.TextField(null=True, default=None,blank=True)
	timestamp_survey_end = models.DateTimeField(default=timezone.now)

class UserConsent(models.Model):
	user = models.ForeignKey(User)
	session = models.ForeignKey(Session_log)
	email_thread = models.TextField()	
	knowledge_source = models.ForeignKey(KnowledgeSource)


class Click_log(models.Model):
	user = models.ForeignKey(User)
	session = models.ForeignKey(Session_log)
	timestamp_clicked = models.DateTimeField(default=timezone.now)
	SHOW_ACTION = '_show'
    	HIDE_ACTION = '_hide'
	ACTION_CHOICES = (
		(SHOW_ACTION, '_show'),
		(HIDE_ACTION,'_hide'),
	)
	click_action = models.CharField(choices = ACTION_CHOICES, default = SHOW_ACTION ,max_length=255)
	for_email = models.ForeignKey(EmailBody)

class Box_log(models.Model):
	user = models.ForeignKey(User)
	session = models.ForeignKey(Session_log)
	timestamp_resize = models.DateTimeField(default=timezone.now)
	width = models.CharField(max_length=35, null=True, default=None,blank=True)
	height = models.CharField(max_length=35, null=True, default=None,blank=True)
	for_email = models.ForeignKey(EmailBody)

class Box_scroll_log(models.Model):
	user = models.ForeignKey(User)
	session = models.ForeignKey(Session_log)
	timestamp_resize = models.DateTimeField(default=timezone.now)
	scrollbar_pos = models.CharField(max_length=35, null=False, default=None,blank=True)
	for_email = models.ForeignKey(EmailBody)


        


	
	
