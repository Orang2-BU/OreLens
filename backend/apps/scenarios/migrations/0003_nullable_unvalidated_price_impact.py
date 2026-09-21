from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('scenarios', '0002_alter_scenarioinput_options_and_more')]
    operations = [
        migrations.AlterField(
            model_name='scenarioresult', name='estimated_price_impact_pct',
            field=models.FloatField(blank=True, help_text='Estimated price change percentage; null without a validated coefficient', null=True),
        ),
        migrations.AlterField(
            model_name='scenarioresult', name='estimated_new_price',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=14, null=True),
        ),
    ]
