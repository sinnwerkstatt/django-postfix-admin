# Generated by Django 2.1.5 on 2019-02-13 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mail', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='alias',
            options={'ordering': ['name'], 'verbose_name_plural': 'Aliases'},
        ),
        migrations.AlterModelOptions(
            name='aliasdomain',
            options={'ordering': ['name'], 'verbose_name_plural': 'AliasDomains'},
        ),
        migrations.AlterModelOptions(
            name='domain',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='mailbox',
            options={'ordering': ['name'], 'verbose_name_plural': 'Mailboxes'},
        ),
        migrations.AlterModelOptions(
            name='tlspolicy',
            options={'ordering': ['domain'], 'verbose_name': 'TLS Policy', 'verbose_name_plural': 'TLS Policies'},
        ),
        migrations.RemoveField(
            model_name='alias',
            name='target',
        ),
        migrations.AddField(
            model_name='alias',
            name='targets',
            field=models.TextField(default='', help_text='You can specify multiple recipients, one per line.'),
            preserve_default=False,
        ),
    ]
