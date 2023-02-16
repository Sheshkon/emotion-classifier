# Generated by Django 4.1.7 on 2023-02-16 15:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0002_alter_profile_avatar_alter_profile_bio'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageClassifier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('input', models.ImageField(upload_to='image_classifier/')),
                ('input_binary', models.BinaryField()),
                ('output', models.ImageField(upload_to='image_classifier')),
                ('output_binary', models.BinaryField()),
                ('date_time', models.DateTimeField(auto_now_add=True)),
                ('description', models.TextField()),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='calcs_images', to='accounts.profile')),
            ],
        ),
    ]
