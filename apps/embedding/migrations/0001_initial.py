# Generated by Django 4.1.10 on 2023-10-09 06:33

import common.field.vector_field
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('dataset', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Embedding',
            fields=[
                ('id', models.CharField(max_length=128, primary_key=True, serialize=False, verbose_name='主键id')),
                ('source_id', models.CharField(max_length=128, verbose_name='资源id')),
                ('source_type', models.CharField(choices=[('0', '问题'), ('1', '段落')], default='0', max_length=1, verbose_name='资源类型')),
                ('embedding', common.field.vector_field.VectorField(verbose_name='向量')),
                ('dataset', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='dataset.dataset', verbose_name='数据集关联')),
            ],
            options={
                'db_table': 'embedding',
            },
        ),
    ]
