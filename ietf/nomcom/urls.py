
from ietf.nomcom.forms import EditMembersForm, EditMembersFormPreview
from ietf.nomcom import views
from ietf.message import views as message_views
from ietf.utils.urls import url

urlpatterns = [
    url(r'^$', views.index),
    url(r'^ann/$', views.announcements),
    url(r'^(?P<year>\d{4})/private/$', views.private_index),
    url(r'^(?P<year>\d{4})/private/key/$', views.private_key),
    url(r'^(?P<year>\d{4})/private/help/$', views.configuration_help),
    url(r'^(?P<year>\d{4})/private/nominate/$', views.private_nominate),
    url(r'^(?P<year>\d{4})/private/nominate/newperson$', views.private_nominate_newperson),
    url(r'^(?P<year>\d{4})/private/feedback/$', views.private_feedback),
    url(r'^(?P<year>\d{4})/private/feedback-email/$', views.private_feedback_email),
    url(r'^(?P<year>\d{4})/private/questionnaire-response/$', views.private_questionnaire),
    url(r'^(?P<year>\d{4})/private/view-feedback/$', views.view_feedback),
    url(r'^(?P<year>\d{4})/private/view-feedback/unrelated/$', views.view_feedback_unrelated),
    url(r'^(?P<year>\d{4})/private/view-feedback/pending/$', views.view_feedback_pending),
    url(r'^(?P<year>\d{4})/private/view-feedback/nominee/(?P<nominee_id>\d+)$', views.view_feedback_nominee),
    url(r'^(?P<year>\d{4})/private/edit/nominee/(?P<nominee_id>\d+)$', views.edit_nominee),
    url(r'^(?P<year>\d{4})/private/merge-nominee/?$', views.private_merge_nominee),
    url(r'^(?P<year>\d{4})/private/merge-person/?$', views.private_merge_person),
    url(r'^(?P<year>\d{4})/private/send-reminder-mail/(?P<type>\w+)/$', views.send_reminder_mail),
    url(r'^(?P<year>\d{4})/private/edit-members/$', EditMembersFormPreview(EditMembersForm), name='ietf.nomcom.forms.EditMembersFormPreview'),
    url(r'^(?P<year>\d{4})/private/edit-nomcom/$', views.edit_nomcom),
    url(r'^(?P<year>\d{4})/private/chair/templates/$', views.list_templates),
    url(r'^(?P<year>\d{4})/private/chair/templates/(?P<template_id>\d+)/$', views.edit_template),
    url(r'^(?P<year>\d{4})/private/chair/position/$', views.list_positions),
    url(r'^(?P<year>\d{4})/private/chair/position/add/$', views.edit_position),
    url(r'^(?P<year>\d{4})/private/chair/position/(?P<position_id>\d+)/$', views.edit_position),
    url(r'^(?P<year>\d{4})/private/chair/position/(?P<position_id>\d+)/remove/$', views.remove_position),

    url(r'^(?P<year>\d{4})/$', views.year_index),
    url(r'^(?P<year>\d{4})/requirements/$', views.requirements),
    url(r'^(?P<year>\d{4})/expertise/$', views.requirements),
    url(r'^(?P<year>\d{4})/questionnaires/$', views.questionnaires),
    url(r'^(?P<year>\d{4})/feedback/$', views.public_feedback),
    url(r'^(?P<year>\d{4})/nominate/$', views.public_nominate),
    url(r'^(?P<year>\d{4})/nominate/newperson$', views.public_nominate_newperson),
    url(r'^(?P<year>\d{4})/process-nomination-status/(?P<nominee_position_id>\d+)/(?P<state>[\w]+)/(?P<date>[\d]+)/(?P<hash>[a-f0-9]+)/$', views.process_nomination_status),
# use the generic view from message
    url(r'^ann/(?P<message_id>\d+)/$', message_views.message, {'group_type': "nomcom" }),
]
