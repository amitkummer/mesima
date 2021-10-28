# Generated by Django 3.2.8 on 2021-10-28 12:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1000)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('favoriteProgrammingLanguage', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1000)),
                ('details', models.CharField(max_length=1000)),
                ('dueDate', models.DateField()),
                ('status', models.CharField(choices=[('active', 'active'), ('done', 'done')], max_length=100)),
                ('ownerId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.person')),
            ],
        ),
    ]
