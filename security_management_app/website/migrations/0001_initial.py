# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Device'
        db.create_table(u'website_device', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('uid', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('os', self.gf('django.db.models.fields.CharField')(default='Unknown', max_length=50)),
            ('nickname', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('last_updated', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
        ))
        db.send_create_signal(u'website', ['Device'])

        # Adding model 'Vulnerability'
        db.create_table(u'website_vulnerability', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cve', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
            ('summary', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('published', self.gf('django.db.models.fields.DateTimeField')()),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')()),
            ('score', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('access_vector', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('access_complexity', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('authentication', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('confidentiality_impact', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('integrity_impact', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('availability_impact', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal(u'website', ['Vulnerability'])

        # Adding model 'Reference'
        db.create_table(u'website_reference', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('vulnerability', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['website.Vulnerability'])),
            ('source', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal(u'website', ['Reference'])

        # Adding model 'Cpe'
        db.create_table(u'website_cpe', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cpe', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
            ('part', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('vendor', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('product', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('version', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('update', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('edition', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('sw_edition', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('target_sw', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('target_hw', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('other', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'website', ['Cpe'])

        # Adding model 'Application'
        db.create_table(u'website_application', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cpe', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['website.Cpe'])),
        ))
        db.send_create_signal(u'website', ['Application'])

        # Adding M2M table for field vulnerability on 'Application'
        m2m_table_name = db.shorten_name(u'website_application_vulnerability')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('application', models.ForeignKey(orm[u'website.application'], null=False)),
            ('vulnerability', models.ForeignKey(orm[u'website.vulnerability'], null=False))
        ))
        db.create_unique(m2m_table_name, ['application_id', 'vulnerability_id'])

        # Adding model 'DeviceUpdate'
        db.create_table(u'website_deviceupdate', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('device', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['website.Device'])),
            ('application', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['website.Application'])),
            ('version', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'website', ['DeviceUpdate'])

        # Adding model 'UpdateApplications'
        db.create_table(u'website_updateapplications', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('device', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['website.Device'])),
            ('application', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['website.Application'])),
            ('version', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'website', ['UpdateApplications'])


    def backwards(self, orm):
        # Deleting model 'Device'
        db.delete_table(u'website_device')

        # Deleting model 'Vulnerability'
        db.delete_table(u'website_vulnerability')

        # Deleting model 'Reference'
        db.delete_table(u'website_reference')

        # Deleting model 'Cpe'
        db.delete_table(u'website_cpe')

        # Deleting model 'Application'
        db.delete_table(u'website_application')

        # Removing M2M table for field vulnerability on 'Application'
        db.delete_table(db.shorten_name(u'website_application_vulnerability'))

        # Deleting model 'DeviceUpdate'
        db.delete_table(u'website_deviceupdate')

        # Deleting model 'UpdateApplications'
        db.delete_table(u'website_updateapplications')


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
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'nickname': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'os': ('django.db.models.fields.CharField', [], {'default': "'Unknown'", 'max_length': '50'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'uid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        u'website.deviceupdate': {
            'Meta': {'object_name': 'DeviceUpdate'},
            'application': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['website.Application']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'device': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['website.Device']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '50'})
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
            'device': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['website.Device']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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