# Generated by Django 2.2.5 on 2021-02-22 06:22

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Block',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField()),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField()),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CampaignStage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField()),
                ('description', models.TextField()),
                ('position', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('slug', models.SlugField()),
                ('type_of_field', models.CharField(choices=[('boolean', 'Boolean'), ('date', 'Date'), ('text', 'Text'), ('file', 'File')], max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Query',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('description', models.TextField()),
                ('max_responses', models.PositiveIntegerField(default=0)),
                ('required', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='QueryResponse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('query', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Query')),
            ],
        ),
        migrations.CreateModel(
            name='ResponseTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='FormBlock',
            fields=[
                ('block_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='api.Block')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('response_accept_ends_at', models.DateTimeField(blank=True, null=True)),
                ('response_accept_starts_at', models.DateTimeField(blank=True, null=True)),
                ('created_by_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            bases=('api.block',),
        ),
        migrations.CreateModel(
            name='ResponseTemplateField',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('required', models.BooleanField(default=False)),
                ('field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Field')),
                ('response_template', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.ResponseTemplate')),
            ],
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', django.contrib.postgres.fields.jsonb.JSONField(default=dict)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('response_template', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.ResponseTemplate')),
            ],
        ),
        migrations.CreateModel(
            name='QueryResponseThrough',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.PositiveIntegerField(default=0)),
                ('query_response', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.QueryResponse')),
                ('response', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Response')),
            ],
        ),
        migrations.AddField(
            model_name='queryresponse',
            name='responses',
            field=models.ManyToManyField(through='api.QueryResponseThrough', to='api.Response'),
        ),
        migrations.AddField(
            model_name='query',
            name='response_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.ResponseTemplate'),
        ),
        migrations.CreateModel(
            name='CampaignStageBlockThrough',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.PositiveIntegerField(default=0)),
                ('block', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Block')),
                ('campaign_stage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.CampaignStage')),
            ],
        ),
        migrations.AddField(
            model_name='campaignstage',
            name='blocks',
            field=models.ManyToManyField(through='api.CampaignStageBlockThrough', to='api.Block'),
        ),
        migrations.AddField(
            model_name='campaignstage',
            name='campaign',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Campaign'),
        ),
        migrations.CreateModel(
            name='FormQueryThrough',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.PositiveIntegerField(default=0)),
                ('query', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Query')),
                ('form_block', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.FormBlock')),
            ],
        ),
        migrations.AddField(
            model_name='formblock',
            name='queries',
            field=models.ManyToManyField(through='api.FormQueryThrough', to='api.Query'),
        ),
    ]
