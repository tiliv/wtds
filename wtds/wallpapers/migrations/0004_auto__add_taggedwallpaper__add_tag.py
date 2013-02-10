# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

# NOTE: This is a modified migration to rename the taggit tables to the new model tables.
# After the rename, it regereates the taggit tables as they were before.  The taggit table
# migrations were generated by asking south to create an initial migration on taggit itself.

class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TaggedWallpaper'
        db.rename_table(u'taggit_taggeditem', u'wallpapers_taggedwallpaper')
        db.send_create_signal(u'wallpapers', ['TaggedWallpaper'])
        db.create_table(u'taggit_taggeditem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tag', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'taggit_taggeditem_items', to=orm['taggit.Tag'])),
            ('object_id', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'taggit_taggeditem_tagged_items', to=orm['contenttypes.ContentType'])),
        ))
        db.send_create_signal(u'taggit', ['TaggedItem'])

        # Adding model 'Tag'
        db.rename_table(u'taggit_tag', u'wallpapers_tag')
        db.send_create_signal(u'wallpapers', ['Tag'])
        db.create_table(u'taggit_tag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=100)),
        ))
        db.send_create_signal(u'taggit', ['Tag'])


    def backwards(self, orm):
        # Deleting model 'TaggedWallpaper'
        db.delete_table(u'taggit_taggeditem')
        db.rename_table(u'wallpapers_taggedwallpaper', u'taggit_taggeditem')

        # Deleting model 'Tag'
        db.delete_table(u'taggit_tag')
        db.rename_table(u'wallpapers_tag', u'taggit_tag')


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
        u'wallpapers.author': {
            'Meta': {'object_name': 'Author'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '500', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        u'wallpapers.license': {
            'Meta': {'object_name': 'License'},
            'allow_commercial_use': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'allow_derivatives': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'attribute_author': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'persist_license': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'summary': ('django.db.models.fields.CharField', [], {'max_length': '400'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '400', 'blank': 'True'})
        },
        u'wallpapers.tag': {
            'Meta': {'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'wallpapers.taggedwallpaper': {
            'Meta': {'object_name': 'TaggedWallpaper'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'wallpapers_taggedwallpaper_tagged_items'", 'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['wallpapers.Tag']"})
        },
        u'wallpapers.wallpaper': {
            'Meta': {'object_name': 'Wallpaper'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['wallpapers.Author']", 'null': 'True', 'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'duplicate_of': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['wallpapers.Wallpaper']", 'null': 'True', 'blank': 'True'}),
            'height': ('django.db.models.fields.PositiveIntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'license': ('django.db.models.fields.related.ForeignKey', [], {'default': '8', 'to': u"orm['wallpapers.License']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'purity_rating': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'raw_ratio': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'uploader': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'views': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'width': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        u'taggit.tag': {
            'Meta': {'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'taggit.taggeditem': {
            'Meta': {'object_name': 'TaggedItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'taggit_taggeditem_tagged_items'", 'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'taggit_taggeditem_items'", 'to': u"orm['taggit.Tag']"})
        }
    }

    complete_apps = ['wallpapers']