from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={},
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('admin', 'Администратор'), ('moderator', 'Администратор'), ('user', 'Администратор')], default='user', max_length=25),
        ),
        migrations.AlterUniqueTogether(
            name='user',
            unique_together={('username', 'email')},
        ),
    ]
