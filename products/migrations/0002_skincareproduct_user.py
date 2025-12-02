# Generated manually
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def assign_products_to_admin(apps, schema_editor):
    """Assign all existing products to admin user"""
    SkincareProduct = apps.get_model('products', 'SkincareProduct')
    User = apps.get_model('auth', 'User')
    
    try:
        admin_user = User.objects.get(username='admin')
        SkincareProduct.objects.filter(user__isnull=True).update(user=admin_user)
    except User.DoesNotExist:
        # If admin doesn't exist, create it
        admin_user = User.objects.create_user(
            username='admin',
            password='admin123',
            email='admin@fyne.com',
            is_staff=True,
            is_superuser=True
        )
        SkincareProduct.objects.filter(user__isnull=True).update(user=admin_user)


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='skincareproduct',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to=settings.AUTH_USER_MODEL),
        ),
        migrations.RunPython(assign_products_to_admin),
        migrations.AlterField(
            model_name='skincareproduct',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to=settings.AUTH_USER_MODEL),
        ),
    ]

