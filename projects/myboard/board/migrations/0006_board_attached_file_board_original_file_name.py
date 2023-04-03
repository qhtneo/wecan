# Generated by Django 4.1.7 on 2023-04-03 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("board", "0005_rename_board_reply_board_obj"),
    ]

    operations = [
        migrations.AddField(
            model_name="board",
            name="attached_file",
            field=models.FileField(null=True, upload_to="board/%Y-%m-%d/"),
        ),
        migrations.AddField(
            model_name="board",
            name="original_file_name",
            field=models.CharField(max_length=260, null=True),
        ),
    ]