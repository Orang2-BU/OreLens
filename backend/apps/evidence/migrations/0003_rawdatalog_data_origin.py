from django.db import migrations, models


def reclassify_demo_seed(apps, schema_editor):
    RawDataLog = apps.get_model('evidence', 'RawDataLog')
    NormalizedMetric = apps.get_model('evidence', 'NormalizedMetric')
    logs = RawDataLog.objects.filter(
        source='Sectors', endpoint__startswith='/v1/company/report/', response_payload__status='audited',
    )
    ids = list(logs.values_list('id', flat=True))
    logs.update(source='Seed Demo', data_origin='seed_demo')
    NormalizedMetric.objects.filter(raw_data_ref_id__in=ids).update(source='Seed Demo', confidence='Low')


class Migration(migrations.Migration):
    dependencies = [('evidence', '0002_normalizedmetric_commodity')]

    operations = [
        migrations.AddField(
            model_name='rawdatalog',
            name='data_origin',
            field=models.CharField(choices=[('live_api', 'Live API'), ('imported_file', 'Imported file'), ('derived', 'Derived'), ('seed_demo', 'Seed demo')], default='live_api', max_length=20),
        ),
        migrations.RunPython(reclassify_demo_seed, migrations.RunPython.noop),
    ]
