# Generated by Django 4.1.7 on 2023-03-17 15:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reserve',
            name='passenger',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='passenger'),
        ),
        migrations.AddField(
            model_name='reserve',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.room', verbose_name='room'),
        ),
        migrations.AddField(
            model_name='place',
            name='amenities',
            field=models.ManyToManyField(limit_choices_to={'is_shared': True}, to='core.amenities', verbose_name='amenities'),
        ),
        migrations.AddField(
            model_name='place',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.owner', verbose_name='owner'),
        ),
        migrations.AddField(
            model_name='place',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.placecategory', verbose_name='type'),
        ),
        migrations.AlterUniqueTogether(
            name='room',
            unique_together={('place', 'room_number')},
        ),
        migrations.AlterUniqueTogether(
            name='place',
            unique_together={('owner', 'name')},
        ),
    ]
