from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('scenarios', '0003_nullable_unvalidated_price_impact')]
    operations = [
        migrations.AddField(
            model_name='scenarioresult', name='run_metadata',
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.AddField(
            model_name='scenarioresult', name='run_status',
            field=models.CharField(choices=[
                ('arithmetic_preview', 'Arithmetic preview'),
                ('preliminary_sensitivity', 'Preliminary sensitivity'),
                ('validated_sensitivity', 'Validated sensitivity'),
            ], default='arithmetic_preview', max_length=40),
        ),
    ]
