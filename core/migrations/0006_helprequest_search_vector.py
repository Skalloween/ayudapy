# Generated by Django 2.2.12 on 2020-04-10 20:53

import django.contrib.postgres.search
from django.contrib.postgres.search import SearchVector
from django.db import migrations


def populate_search_vector(apps, schema_editor):
    HelpRequest = apps.get_model("core", "HelpRequest")
    vector = SearchVector("title", weight="A", config='spanish') + SearchVector("message", weight="B", config='spanish')
    HelpRequest.objects.update(search_vector=vector)


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_add_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='helprequest',
            name='search_vector',
            field=django.contrib.postgres.search.SearchVectorField(null=True),
        ),
        migrations.RunPython(populate_search_vector),
        migrations.AlterField(
            model_name="helprequest", name="search_vector", field=django.contrib.postgres.search.SearchVectorField()
        ),
        migrations.RunSQL(
            sql="""
            CREATE FUNCTION help_request_search_vector_update_trigger() RETURNS trigger AS $$
            begin
            new.search_vector :=
                setweight(to_tsvector('pg_catalog.spanish', coalesce(new.title,'')), 'A') ||
                setweight(to_tsvector('pg_catalog.spanish', coalesce(new.message,'')), 'B');
            return new;
            end
            $$ LANGUAGE plpgsql;

            CREATE TRIGGER tsvectorupdate BEFORE INSERT OR UPDATE
            ON core_helprequest FOR EACH ROW EXECUTE PROCEDURE help_request_search_vector_update_trigger();
            """,
            reverse_sql="""
            DROP TRIGGER IF EXISTS tsvectorupdate
            ON core_helprequest;
            """,
        ),
    ]