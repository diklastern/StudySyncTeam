# Generated by Django 5.2 on 2025-04-17 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_groupavailability_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='degree_program',
            field=models.CharField(choices=[('is', 'Information Systems'), ('cs', 'Computer Science'), ('se', 'Software Engineering'), ('ba', 'Business Administration')], max_length=50),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='university',
            field=models.CharField(choices=[('tel_aviv', 'Tel Aviv University'), ('hebrew', 'Hebrew University of Jerusalem'), ('technion', 'Technion – Israel Institute of Technology'), ('haifa', 'University of Haifa'), ('ben_gurion', 'Ben-Gurion University'), ('open', 'Open University'), ('bar_ilan', 'Bar-Ilan University'), ('yafo', 'The Academic College of Tel Aviv–Yaffo'), ('sapir', 'Sapir Academic College'), ('college_management', 'College of Management'), ('shenkar', 'Shenkar College of Engineering, Design and Art'), ('beit_berl', 'Beit Berl College'), ('ruppin', 'Ruppin Academic Center'), ('emek_yizrael', 'Jezreel Valley College')], max_length=50),
        ),
    ]
