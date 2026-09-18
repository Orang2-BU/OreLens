import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('commodities', '0001_initial'),
        ('evidence', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='normalizedmetric',
            name='commodity',
            field=models.ForeignKey(blank=True, help_text='Required for company metrics scoped to one commodity', null=True, on_delete=django.db.models.deletion.SET_NULL, to='commodities.commodity'),
        ),
    ]
