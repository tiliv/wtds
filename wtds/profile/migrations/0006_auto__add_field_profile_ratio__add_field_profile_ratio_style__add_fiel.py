# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Profile.ratio'
        db.add_column(u'profile_profile', 'ratio',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=10, blank=True),
                      keep_default=False)

        # Adding field 'Profile.ratio_style'
        db.add_column(u'profile_profile', 'ratio_style',
                      self.gf('django.db.models.fields.CharField')(default='gte', max_length=10),
                      keep_default=False)

        # Adding field 'Profile.height'
        db.add_column(u'profile_profile', 'height',
                      self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Profile.height_style'
        db.add_column(u'profile_profile', 'height_style',
                      self.gf('django.db.models.fields.CharField')(default='gte', max_length=10),
                      keep_default=False)

        # Adding field 'Profile.width'
        db.add_column(u'profile_profile', 'width',
                      self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Profile.width_style'
        db.add_column(u'profile_profile', 'width_style',
                      self.gf('django.db.models.fields.CharField')(default='gte', max_length=10),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Profile.ratio'
        db.delete_column(u'profile_profile', 'ratio')

        # Deleting field 'Profile.ratio_style'
        db.delete_column(u'profile_profile', 'ratio_style')

        # Deleting field 'Profile.height'
        db.delete_column(u'profile_profile', 'height')

        # Deleting field 'Profile.height_style'
        db.delete_column(u'profile_profile', 'height_style')

        # Deleting field 'Profile.width'
        db.delete_column(u'profile_profile', 'width')

        # Deleting field 'Profile.width_style'
        db.delete_column(u'profile_profile', 'width_style')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'profile.profile': {
            'Meta': {'ordering': "('name', '-id')", 'object_name': 'Profile'},
            'height': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'height_style': ('django.db.models.fields.CharField', [], {'default': "'gte'", 'max_length': '10'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'purity_rating': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'purity_style': ('django.db.models.fields.CharField', [], {'default': "'lte'", 'max_length': '10'}),
            'ratio': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'ratio_style': ('django.db.models.fields.CharField', [], {'default': "'gte'", 'max_length': '10'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'width': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'width_style': ('django.db.models.fields.CharField', [], {'default': "'gte'", 'max_length': '10'})
        }
    }

    complete_apps = ['profile']