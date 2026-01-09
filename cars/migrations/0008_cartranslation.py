from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0007_car_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='CarTranslation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(choices=[('hy', 'Armenian'), ('ru', 'Russian'), ('en', 'English')], max_length=5)),
                ('make', models.CharField(max_length=50)),
                ('model', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True, default='')),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='cars.car')),
            ],
            options={
                'unique_together': {('car', 'language')},
            },
        ),
    ]

