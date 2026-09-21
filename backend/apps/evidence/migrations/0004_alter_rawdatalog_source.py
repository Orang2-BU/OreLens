from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('evidence', '0003_rawdatalog_data_origin')]

    operations = [
        migrations.AlterField(
            model_name='rawdatalog',
            name='source',
            field=models.CharField(choices=[('Seed Demo', 'Seed demo data'), ('Sectors', 'Sectors API'), ('World Bank', 'World Bank API'), ('FRED', 'FRED Federal Reserve API'), ('UN Comtrade', 'UN Comtrade API'), ('EIA', 'EIA Energy API')], max_length=50),
        ),
    ]
