# Generated by Django 5.0.6 on 2024-05-25 02:39

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoriaProducto',
            fields=[
                ('id_categoria_prod', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_categoria_prod', models.CharField(max_length=255)),
                ('slug', models.SlugField(blank=True, max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Inventario',
            fields=[
                ('id_inventario', models.AutoField(primary_key=True, serialize=False)),
                ('stock_sucursal', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Sucursal',
            fields=[
                ('id_sucursal', models.AutoField(primary_key=True, serialize=False)),
                ('nomb_sucursal', models.CharField(max_length=255)),
                ('direccion_sucursal', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='TipoProducto',
            fields=[
                ('id_tp_producto', models.AutoField(primary_key=True, serialize=False)),
                ('nomb_tp_producto', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('vendedor', models.BooleanField(default=False)),
                ('especialidad', models.CharField(max_length=50)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='ChatConsulta',
            fields=[
                ('id_consulta', models.AutoField(primary_key=True, serialize=False)),
                ('asunto', models.CharField(max_length=255)),
                ('mensaje', models.TextField()),
                ('respuesta', models.TextField(blank=True, null=True)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Pago',
            fields=[
                ('id_pago', models.AutoField(primary_key=True, serialize=False)),
                ('fec_pago', models.DateTimeField()),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id_producto', models.AutoField(primary_key=True, serialize=False)),
                ('nomb_producto', models.CharField(max_length=255)),
                ('descrip_producto', models.TextField()),
                ('precio_producto', models.DecimalField(decimal_places=2, max_digits=10)),
                ('marca_producto', models.CharField(max_length=255)),
                ('modelo_producto', models.CharField(max_length=255)),
                ('stock_total', models.IntegerField()),
                ('categoria_producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appModelosDB.categoriaproducto')),
                ('inventario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appModelosDB.inventario')),
                ('tipo_producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appModelosDB.tipoproducto')),
            ],
        ),
        migrations.CreateModel(
            name='HistorialPrecio',
            fields=[
                ('id_historial', models.AutoField(primary_key=True, serialize=False)),
                ('precio_antiguo', models.DecimalField(decimal_places=2, max_digits=10)),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appModelosDB.producto')),
            ],
        ),
        migrations.CreateModel(
            name='DetalleBoleta',
            fields=[
                ('id_boleta', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_boleta', models.DateField()),
                ('total_boleta', models.DecimalField(decimal_places=2, max_digits=10)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('productos', models.ManyToManyField(to='appModelosDB.producto')),
            ],
        ),
        migrations.CreateModel(
            name='Promocion',
            fields=[
                ('codigo_promocion', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_promocion', models.CharField(max_length=255)),
                ('fecha_inicio', models.DateField()),
                ('fecha_termino', models.DateField()),
                ('productos', models.ManyToManyField(to='appModelosDB.producto')),
            ],
        ),
        migrations.AddField(
            model_name='inventario',
            name='sucursal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appModelosDB.sucursal'),
        ),
    ]