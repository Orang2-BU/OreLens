from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('commodities', '0002_commoditydriver_evidence')]
    operations = [migrations.AddField(
        model_name='commoditydriver', name='validation_details',
        field=models.JSONField(blank=True, default=dict),
    )]
