# Generated by Django 5.2 on 2025-04-18 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_userprofile_degree_program_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='degree_program',
            field=models.CharField(choices=[('is', 'Information Systems'), ('cs', 'Computer Science'), ('se', 'Software Engineering'), ('ba', 'Business Administration')], default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customuser',
            name='full_name',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customuser',
            name='university',
            field=models.CharField(choices=[('tel_aviv', 'Tel Aviv University'), ('hebrew', 'Hebrew University of Jerusalem'), ('technion', 'Technion – Israel Institute of Technology'), ('haifa', 'University of Haifa'), ('ben_gurion', 'Ben-Gurion University'), ('open', 'Open University'), ('bar_ilan', 'Bar-Ilan University'), ('yafo', 'The Academic College of Tel Aviv–Yaffo'), ('sapir', 'Sapir Academic College'), ('college_management', 'College of Management'), ('shenkar', 'Shenkar College of Engineering, Design and Art'), ('beit_berl', 'Beit Berl College'), ('ruppin', 'Ruppin Academic Center'), ('emek_yizrael', 'Jezreel Valley College')], default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customuser',
            name='year_of_study',
            field=models.CharField(choices=[(1, '1st Year'), (2, '2nd Year'), (3, '3rd Year'), (4, '4th Year'), (5, '5th+ Year')], default=1, max_length=20),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]
