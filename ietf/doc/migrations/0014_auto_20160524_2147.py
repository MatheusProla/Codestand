# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('message', '__first__'),
        ('doc', '0013_auto_20151027_1127'),
    ]

    operations = [
        migrations.CreateModel(
            name='AddedMessageEvent',
            fields=[
                ('docevent_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='doc.DocEvent')),
                ('msgtype', models.CharField(max_length=25)),
                ('in_reply_to', models.ForeignKey(related_name='doc_irtomanual', blank=True, to='message.Message', null=True)),
                ('message', models.ForeignKey(related_name='doc_manualevents', blank=True, to='message.Message', null=True)),
            ],
            options={
            },
            bases=('doc.docevent',),
        ),
        migrations.AlterField(
            model_name='docevent',
            name='type',
            field=models.CharField(max_length=50, choices=[(b'new_revision', b'Added new revision'), (b'changed_document', b'Changed document metadata'), (b'added_comment', b'Added comment'), (b'added_message', b'Added message'), (b'deleted', b'Deleted document'), (b'changed_state', b'Changed state'), (b'changed_stream', b'Changed document stream'), (b'expired_document', b'Expired document'), (b'extended_expiry', b'Extended expiry of document'), (b'requested_resurrect', b'Requested resurrect'), (b'completed_resurrect', b'Completed resurrect'), (b'changed_consensus', b'Changed consensus'), (b'published_rfc', b'Published RFC'), (b'added_suggested_replaces', b'Added suggested replacement relationships'), (b'reviewed_suggested_replaces', b'Reviewed suggested replacement relationships'), (b'changed_group', b'Changed group'), (b'changed_protocol_writeup', b'Changed protocol writeup'), (b'changed_charter_milestone', b'Changed charter milestone'), (b'initial_review', b'Set initial review time'), (b'changed_review_announcement', b'Changed WG Review text'), (b'changed_action_announcement', b'Changed WG Action text'), (b'started_iesg_process', b'Started IESG process on document'), (b'created_ballot', b'Created ballot'), (b'closed_ballot', b'Closed ballot'), (b'sent_ballot_announcement', b'Sent ballot announcement'), (b'changed_ballot_position', b'Changed ballot position'), (b'changed_ballot_approval_text', b'Changed ballot approval text'), (b'changed_ballot_writeup_text', b'Changed ballot writeup text'), (b'changed_rfc_editor_note_text', b'Changed RFC Editor Note text'), (b'changed_last_call_text', b'Changed last call text'), (b'requested_last_call', b'Requested last call'), (b'sent_last_call', b'Sent last call'), (b'scheduled_for_telechat', b'Scheduled for telechat'), (b'iesg_approved', b'IESG approved document (no problem)'), (b'iesg_disapproved', b'IESG disapproved document (do not publish)'), (b'approved_in_minute', b'Approved in minute'), (b'iana_review', b'IANA review comment'), (b'rfc_in_iana_registry', b'RFC is in IANA registry'), (b'rfc_editor_received_announcement', b'Announcement was received by RFC Editor'), (b'requested_publication', b'Publication at RFC Editor requested'), (b'sync_from_rfc_editor', b'Received updated information from RFC Editor'),]),
            preserve_default=True,
        ),
    ]
