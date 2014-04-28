# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'UpdateApplications.device'
        db.delete_column(u'website_updateapplications', 'device_id')

        # Deleting field 'UpdateApplications.version'
        db.delete_column(u'website_updateapplications', 'version')

        # Adding field 'UpdateApplications.update'
        db.add_column(u'website_updateapplications', 'update',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['website.DeviceUpdate']),
                      keep_default=False)

        # Deleting field 'DeviceUpdate.version'
        db.delete_column(u'website_deviceupdate', 'version')

        # Deleting field 'DeviceUpdate.application'
        db.delete_column(u'website_deviceupdate', 'application_id')


        # Changing field 'DeviceUpdate.date'
        db.alter_column(u'website_deviceupdate', 'date', self.gf('django.db.models.fields.DateTimeField')())

    def backwards(self, orm):
        # Adding field 'UpdateApplications.device'
        db.add_column(u'website_updateapplications', 'device',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['website.Device']),
                      keep_default=False)

        # Adding field 'UpdateApplications.version'
        db.add_column(u'website_updateapplications', 'version',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=100),
                      keep_default=False)

        # Deleting field 'UpdateApplications.update'
        db.delete_column(u'website_updateapplications', 'update_id')

        # Adding field 'DeviceUpdate.version'
        db.add_column(u'website_deviceupdate', 'version',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=50),
                      keep_default=False)

        # Adding field 'DeviceUpdate.application'
        db.add_column(u'website_deviceupdate', 'application',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['website.Application']),
                      keep_default=False)


        # Changing field 'DeviceUpdate.date'
        db.alter_column(u'website_deviceupdate', 'date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True))

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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'website.application': {
            'Meta': {'object_name': 'Application'},
            'cpe': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['website.Cpe']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'vulnerability': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['website.Vulnerability']", 'symmetrical': 'False'})
        },
        u'website.cpe': {
            'Meta': {'object_name': 'Cpe'},
            'cpe': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'edition': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'other': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'part': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'product': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'sw_edition': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'target_hw': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'target_sw': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'update': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'vendor': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'website.device': {
            'Meta': {'object_name': 'Device'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'nickname': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'os': ('django.db.models.fields.CharField', [], {'default': "'Unknown'", 'max_length': '50'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'uid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        u'website.deviceupdate': {
            'Meta': {'object_name': 'DeviceUpdate'},
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'device': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['website.Device']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'website.reference': {
            'Meta': {'object_name': 'Reference'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'vulnerability': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['website.Vulnerability']"})
        },
        u'website.updateapplications': {
            'Meta': {'object_name': 'UpdateApplications'},
            'application': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['website.Application']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'update': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['website.DeviceUpdate']"})
        },
        u'website.vulnerability': {
            'Meta': {'object_name': 'Vulnerability'},
            'access_complexity': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'access_vector': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'authentication': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'availability_impact': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'confidentiality_impact': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'cve': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'integrity_impact': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {}),
            'published': ('django.db.models.fields.DateTimeField', [], {}),
            'score': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'summary': ('django.db.models.fields.CharField', [], {'max_length': '1000'})
        }
    }

    complete_apps = ['website']