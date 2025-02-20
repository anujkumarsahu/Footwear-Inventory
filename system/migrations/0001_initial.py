# Generated by Django 4.2.16 on 2025-02-19 16:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ViewMenuUrlPermission',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('role_id', models.IntegerField()),
                ('role_name', models.CharField(max_length=50)),
                ('user_id', models.IntegerField()),
                ('user_name', models.CharField(max_length=50)),
                ('module_id', models.IntegerField()),
                ('module_name', models.CharField(max_length=50)),
                ('menu_id', models.IntegerField()),
                ('menu_name', models.CharField(max_length=50)),
                ('parent_menu_id', models.IntegerField()),
                ('parent_menu_name', models.CharField(max_length=50)),
                ('permission_id', models.IntegerField()),
                ('permission_detail_id', models.IntegerField()),
                ('menu_status', models.IntegerField()),
                ('user_status', models.IntegerField()),
                ('permisstion_status', models.IntegerField()),
                ('permission_dtl_status', models.IntegerField()),
                ('is_save', models.BooleanField(default=False)),
                ('is_update', models.BooleanField(default=False)),
                ('is_close', models.BooleanField(default=False)),
                ('is_list', models.BooleanField(default=True)),
                ('is_delete', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'view_menu_url_permission',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='MenuUrlMaster',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('menu_name', models.CharField(max_length=200)),
                ('url', models.CharField(max_length=200)),
                ('is_toolbar', models.BooleanField(default=False)),
                ('order_no', models.PositiveSmallIntegerField(default=1)),
                ('clear_query', models.CharField(default='cmd=clear', max_length=10)),
                ('stampdatetime', models.DateTimeField()),
                ('updatestampdatetime', models.DateTimeField()),
                ('status', models.IntegerField(default=1)),
            ],
            options={
                'db_table': 'tbl_menu_url_mstr',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='RoleMaster',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=80, unique=True)),
                ('description', models.CharField(max_length=200)),
                ('stampdatetime', models.DateTimeField()),
                ('updatestampdatetime', models.DateTimeField()),
                ('status', models.IntegerField(default=1)),
            ],
            options={
                'db_table': 'tbl_role_mstr',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='UserMaster',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=200)),
                ('mobile_no', models.PositiveBigIntegerField(unique=True)),
                ('address', models.TextField()),
                ('upload_file', models.FileField(upload_to='staff/Adhaar/')),
                ('stampdatetime', models.DateTimeField(auto_now_add=True)),
                ('updatestampdatetime', models.DateTimeField(auto_now=True)),
                ('status', models.IntegerField(default=1)),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.rolemaster')),
            ],
            options={
                'db_table': 'tbl_user_mstr',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='ModuleMaster',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('db_name', models.CharField(max_length=50)),
                ('db_schema_name', models.CharField(max_length=50)),
                ('db_pass', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=500)),
                ('module_img', models.FileField(upload_to='module/image')),
                ('stampdatetime', models.DateTimeField()),
                ('updatestampdatetime', models.DateTimeField()),
                ('status', models.IntegerField(default=1)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.usermaster')),
            ],
            options={
                'db_table': 'tbl_module_mstr',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='MenuUrlPermissionMaster',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('stampdatetime', models.DateTimeField()),
                ('updatestampdatetime', models.DateTimeField()),
                ('status', models.IntegerField(default=1)),
                ('menu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.menuurlmaster')),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.modulemaster')),
                ('role', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='system.rolemaster')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='system.usermaster')),
            ],
            options={
                'db_table': 'tbl_menu_url_permission_mstr',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='MenuUrlPermissionDetails',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('is_save', models.BooleanField(default=False)),
                ('is_update', models.BooleanField(default=False)),
                ('is_close', models.BooleanField(default=False)),
                ('is_list', models.BooleanField(default=True)),
                ('is_delete', models.BooleanField(default=False)),
                ('stampdatetime', models.DateTimeField()),
                ('updatestampdatetime', models.DateTimeField()),
                ('status', models.IntegerField(default=1)),
                ('permission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.menuurlpermissionmaster')),
            ],
            options={
                'db_table': 'tbl_menu_url_permission_dtls',
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='menuurlmaster',
            name='module',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.modulemaster', verbose_name='module'),
        ),
        migrations.AddField(
            model_name='menuurlmaster',
            name='parent_menu',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='system.menuurlmaster'),
        ),
        migrations.AddField(
            model_name='menuurlmaster',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.usermaster'),
        ),
    ]
