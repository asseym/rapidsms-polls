# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ResponseCategory'
        db.create_table('poll_responsecategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['poll.Category'])),
            ('response', self.gf('django.db.models.fields.related.ForeignKey')(related_name='categories', to=orm['poll.Response'])),
            ('is_override', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True)),
        ))
        db.send_create_signal('poll', ['ResponseCategory'])

        # Adding model 'Poll'
        db.create_table('poll_poll', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('question', self.gf('django.db.models.fields.CharField')(max_length=160)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('start_date', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('end_date', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('type', self.gf('django.db.models.fields.SlugField')(max_length=8, null=True, blank=True)),
            ('default_response', self.gf('django.db.models.fields.CharField')(max_length=160, null=True, blank=True)),
            ('response_type', self.gf('django.db.models.fields.CharField')(default='a', max_length=1, null=True, blank=True)),
        ))
        db.send_create_signal('poll', ['Poll'])

        # Adding M2M table for field messages on 'Poll'
        db.create_table('poll_poll_messages', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('poll', models.ForeignKey(orm['poll.poll'], null=False)),
            ('message', models.ForeignKey(orm['db.message'], null=False))
        ))
        db.create_unique('poll_poll_messages', ['poll_id', 'message_id'])

        # Adding M2M table for field contacts on 'Poll'
        db.create_table('poll_poll_contacts', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('poll', models.ForeignKey(orm['poll.poll'], null=False)),
            ('contact', models.ForeignKey(orm['rapidsms.contact'], null=False))
        ))
        db.create_unique('poll_poll_contacts', ['poll_id', 'contact_id'])

        # Adding M2M table for field sites on 'Poll'
        db.create_table('poll_poll_sites', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('poll', models.ForeignKey(orm['poll.poll'], null=False)),
            ('site', models.ForeignKey(orm['sites.site'], null=False))
        ))
        db.create_unique('poll_poll_sites', ['poll_id', 'site_id'])

        # Adding model 'Category'
        db.create_table('poll_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('poll', self.gf('django.db.models.fields.related.ForeignKey')(related_name='categories', to=orm['poll.Poll'])),
            ('priority', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True)),
            ('color', self.gf('django.db.models.fields.CharField')(max_length=6)),
            ('default', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('response', self.gf('django.db.models.fields.CharField')(max_length=160, null=True)),
            ('error_category', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('poll', ['Category'])

        # Adding model 'Response'
        db.create_table('poll_response', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('message', self.gf('django.db.models.fields.related.ForeignKey')(related_name='poll_responses', null=True, to=orm['db.Message'])),
            ('poll', self.gf('django.db.models.fields.related.ForeignKey')(related_name='responses', to=orm['poll.Poll'])),
            ('contact', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='responses', null=True, to=orm['rapidsms.Contact'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('has_errors', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('poll', ['Response'])

        # Adding model 'Rule'
        db.create_table('poll_rule', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('regex', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(related_name='rules', to=orm['poll.Category'])),
            ('rule_type', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('rule_string', self.gf('django.db.models.fields.CharField')(max_length=256, null=True)),
            ('rule', self.gf('django.db.models.fields.IntegerField')(max_length=10, null=True)),
        ))
        db.send_create_signal('poll', ['Rule'])

        # Adding model 'Translation'
        db.create_table('poll_translation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('field', self.gf('django.db.models.fields.TextField')(db_index=True)),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=5, db_index=True)),
            ('value', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('poll', ['Translation'])

        # Adding unique constraint on 'Translation', fields ['field', 'language']
        db.create_unique('poll_translation', ['field', 'language'])


    def backwards(self, orm):
        # Removing unique constraint on 'Translation', fields ['field', 'language']
        db.delete_unique('poll_translation', ['field', 'language'])

        # Deleting model 'ResponseCategory'
        db.delete_table('poll_responsecategory')

        # Deleting model 'Poll'
        db.delete_table('poll_poll')

        # Removing M2M table for field messages on 'Poll'
        db.delete_table('poll_poll_messages')

        # Removing M2M table for field contacts on 'Poll'
        db.delete_table('poll_poll_contacts')

        # Removing M2M table for field sites on 'Poll'
        db.delete_table('poll_poll_sites')

        # Deleting model 'Category'
        db.delete_table('poll_category')

        # Deleting model 'Response'
        db.delete_table('poll_response')

        # Deleting model 'Rule'
        db.delete_table('poll_rule')

        # Deleting model 'Translation'
        db.delete_table('poll_translation')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'db.message': {
            'Meta': {'object_name': 'Message'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'delivered': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'direction': ('django.db.models.fields.CharField', [], {'max_length': '1', 'db_index': 'True'}),
            'external_id': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_response_to': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'responses'", 'null': 'True', 'to': "orm['db.Message']"}),
            'sent': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'Q'", 'max_length': '1', 'db_index': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'db_index': 'True', 'blank': 'True'})
        },
        'eav.attribute': {
            'Meta': {'ordering': "['name']", 'unique_together': "(('site', 'slug'),)", 'object_name': 'Attribute'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'datatype': ('eav.fields.EavDatatypeField', [], {'max_length': '6'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'enum_group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eav.EnumGroup']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'slug': ('eav.fields.EavSlugField', [], {'max_length': '50'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'})
        },
        'eav.enumgroup': {
            'Meta': {'object_name': 'EnumGroup'},
            'enums': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['eav.EnumValue']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        'eav.enumvalue': {
            'Meta': {'object_name': 'EnumValue'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'})
        },
        'eav.value': {
            'Meta': {'object_name': 'Value'},
            'attribute': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eav.Attribute']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'entity_ct': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'value_entities'", 'to': "orm['contenttypes.ContentType']"}),
            'entity_id': ('django.db.models.fields.IntegerField', [], {}),
            'generic_value_ct': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'value_values'", 'null': 'True', 'to': "orm['contenttypes.ContentType']"}),
            'generic_value_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'value_bool': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'value_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'value_enum': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'eav_values'", 'null': 'True', 'to': "orm['eav.EnumValue']"}),
            'value_float': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'value_int': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'value_text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'locations.location': {
            'Meta': {'object_name': 'Location'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.NullBooleanField', [], {'default': 'True', 'null': 'True', 'blank': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parent_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'parent_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True', 'blank': 'True'}),
            'point': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['locations.Point']", 'null': 'True', 'blank': 'True'}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'status': ('django.db.models.fields.NullBooleanField', [], {'default': 'True', 'null': 'True', 'blank': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'tree_parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['locations.Location']"}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'locations'", 'null': 'True', 'to': "orm['locations.LocationType']"})
        },
        'locations.locationtype': {
            'Meta': {'object_name': 'LocationType'},
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'primary_key': 'True'})
        },
        'locations.point': {
            'Meta': {'object_name': 'Point'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '13', 'decimal_places': '10'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '13', 'decimal_places': '10'})
        },
        'poll.category': {
            'Meta': {'ordering': "['name']", 'object_name': 'Category'},
            'color': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'default': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'error_category': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'poll': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'categories'", 'to': "orm['poll.Poll']"}),
            'priority': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            'response': ('django.db.models.fields.CharField', [], {'max_length': '160', 'null': 'True'})
        },
        'poll.poll': {
            'Meta': {'ordering': "['-end_date']", 'object_name': 'Poll'},
            'contacts': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'polls'", 'symmetrical': 'False', 'to': "orm['rapidsms.Contact']"}),
            'default_response': ('django.db.models.fields.CharField', [], {'max_length': '160', 'null': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'messages': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['db.Message']", 'null': 'True', 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '160'}),
            'response_type': ('django.db.models.fields.CharField', [], {'default': "'a'", 'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['sites.Site']", 'symmetrical': 'False'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'type': ('django.db.models.fields.SlugField', [], {'max_length': '8', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'poll.response': {
            'Meta': {'object_name': 'Response'},
            'contact': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'responses'", 'null': 'True', 'to': "orm['rapidsms.Contact']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'has_errors': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'poll_responses'", 'null': 'True', 'to': "orm['db.Message']"}),
            'poll': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'responses'", 'to': "orm['poll.Poll']"})
        },
        'poll.responsecategory': {
            'Meta': {'object_name': 'ResponseCategory'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['poll.Category']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_override': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'response': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'categories'", 'to': "orm['poll.Response']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True'})
        },
        'poll.rule': {
            'Meta': {'object_name': 'Rule'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rules'", 'to': "orm['poll.Category']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'regex': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'rule': ('django.db.models.fields.IntegerField', [], {'max_length': '10', 'null': 'True'}),
            'rule_string': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True'}),
            'rule_type': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        },
        'poll.translation': {
            'Meta': {'unique_together': "(('field', 'language'),)", 'object_name': 'Translation'},
            'field': ('django.db.models.fields.TextField', [], {'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '5', 'db_index': 'True'}),
            'value': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'rapidsms.contact': {
            'Meta': {'object_name': 'Contact'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'birthdate': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['auth.Group']", 'null': 'True', 'blank': 'True'}),
            'health_facility': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_caregiver': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '6', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'occupation': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'reporting_location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['locations.Location']", 'null': 'True', 'blank': 'True'}),
            'subcounty': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'subcounties'", 'null': 'True', 'to': "orm['locations.Location']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'contact'", 'unique': 'True', 'null': 'True', 'to': "orm['auth.User']"}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'village': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'villagers'", 'null': 'True', 'to': "orm['locations.Location']"}),
            'village_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['poll']