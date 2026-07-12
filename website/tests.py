from django.contrib.auth.models import Group, User
from django.test import TestCase
from django.urls import reverse

from .forms import AddRecordForm
from .models import Record


def make_record(**kwargs):
    defaults = {
        'first_name': 'Juan',
        'last_name': 'Pérez',
        'email': 'juan@example.com',
        'phone': '+56912345678',
        'address': 'Calle Falsa 123',
        'city': 'Santiago',
    }
    defaults.update(kwargs)
    return Record.objects.create(**defaults)


class PublicViewsTest(TestCase):
    def test_home_responde(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_register_responde(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_login_valido(self):
        User.objects.create_user(username='vale', password='clave-segura-123')
        response = self.client.post(reverse('home'), {'username': 'vale', 'password': 'clave-segura-123'})
        self.assertRedirects(response, reverse('home'))

    def test_login_invalido_redirige_a_home(self):
        response = self.client.post(reverse('home'), {'username': 'nadie', 'password': 'mala'})
        self.assertRedirects(response, reverse('home'))


class ClientesViewTest(TestCase):
    """La lista de clientes vive en /clientes/ (home ahora es landing)."""

    def setUp(self):
        self.record = make_record()
        User.objects.create_user(username='vale', password='clave-segura-123')

    def test_clientes_requiere_login(self):
        response = self.client.get(reverse('clientes'))
        self.assertEqual(response.status_code, 302)

    def test_clientes_muestra_registros(self):
        self.client.login(username='vale', password='clave-segura-123')
        response = self.client.get(reverse('clientes'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Juan')


class AuthRequiredTest(TestCase):
    """Las vistas protegidas deben redirigir a home si no hay sesión."""

    def setUp(self):
        self.record = make_record()

    def test_record_requiere_login(self):
        response = self.client.get(reverse('record', args=[self.record.pk]))
        self.assertEqual(response.status_code, 302)

    def test_dashboard_requiere_login(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)

    def test_calendar_requiere_login(self):
        response = self.client.get(reverse('calendar'))
        self.assertEqual(response.status_code, 302)


class PermissionsTest(TestCase):
    def setUp(self):
        self.record = make_record()
        # Los grupos Admin/Viewer los crea el signal post_migrate
        self.admin = User.objects.create_user(username='admin1', password='clave-segura-123')
        self.admin.groups.add(Group.objects.get(name='Admin'))
        self.viewer = User.objects.create_user(username='viewer1', password='clave-segura-123')
        self.viewer.groups.add(Group.objects.get(name='Viewer'))

    def test_viewer_no_puede_borrar(self):
        self.client.login(username='viewer1', password='clave-segura-123')
        response = self.client.post(reverse('delete_record', args=[self.record.pk]))
        self.assertRedirects(response, reverse('record', args=[self.record.pk]))
        self.assertTrue(Record.objects.filter(pk=self.record.pk).exists())

    def test_admin_puede_borrar(self):
        self.client.login(username='admin1', password='clave-segura-123')
        response = self.client.post(reverse('delete_record', args=[self.record.pk]))
        self.assertRedirects(response, reverse('home'))
        self.assertFalse(Record.objects.filter(pk=self.record.pk).exists())

    def test_borrar_por_get_no_permitido(self):
        self.client.login(username='admin1', password='clave-segura-123')
        response = self.client.get(reverse('delete_record', args=[self.record.pk]))
        self.assertEqual(response.status_code, 405)
        self.assertTrue(Record.objects.filter(pk=self.record.pk).exists())

    def test_admin_puede_editar(self):
        self.client.login(username='admin1', password='clave-segura-123')
        response = self.client.post(reverse('update_record', args=[self.record.pk]), {
            'first_name': 'Juana',
            'last_name': 'Pérez',
            'email': 'juana@example.com',
            'phone': '+56912345678',
            'address': 'Calle Falsa 123',
            'city': 'Santiago',
        })
        self.assertRedirects(response, reverse('record', args=[self.record.pk]))
        self.record.refresh_from_db()
        self.assertEqual(self.record.first_name, 'Juana')

    def test_viewer_no_puede_agregar(self):
        self.client.login(username='viewer1', password='clave-segura-123')
        response = self.client.get(reverse('add_record'))
        self.assertRedirects(response, reverse('home'))


class FormsTest(TestCase):
    def test_email_invalido_rechazado(self):
        form = AddRecordForm(data={
            'first_name': 'Juan',
            'last_name': 'Pérez',
            'email': 'esto-no-es-un-email',
            'phone': '+56912345678',
            'address': 'Calle Falsa 123',
            'city': 'Santiago',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_telefono_invalido_rechazado(self):
        form = AddRecordForm(data={
            'first_name': 'Juan',
            'last_name': 'Pérez',
            'email': 'juan@example.com',
            'phone': 'abc',
            'address': 'Calle Falsa 123',
            'city': 'Santiago',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('phone', form.errors)
