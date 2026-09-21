import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('commodities', '0001_initial'), ('evidence', '0002_normalizedmetric_commodity')]
    operations = [migrations.AddField(
        model_name='commoditydriver', name='evidence',
        field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='commodity_drivers', to='evidence.normalizedmetric'),
    )]
