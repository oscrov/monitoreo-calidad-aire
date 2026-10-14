from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from .importer import import_csv_text
from .models import Lectura, Sensor

CSV = """sensor,fecha_hora,pm1,pm25,pm4,pm10,co2\nG3,2025-11-23T12:00:00,17.81,20.69,22.38,23.17,452.96\nG4,2025-11-23T12:00:00,17.96,20.68,22.26,22.99,443.27\n"""


class MVPTests(TestCase):
    def setUp(self):
        import_csv_text(CSV)

    def test_importa_dos_sensores_y_dos_lecturas(self):
        self.assertEqual(Sensor.objects.count(), 2)
        self.assertEqual(Lectura.objects.count(), 2)

    def test_sensor_fecha_es_unico_y_reimportar_actualiza(self):
        result = import_csv_text(CSV)
        self.assertEqual(result["imported"], 0)
        self.assertEqual(result["updated"], 2)
        self.assertEqual(Lectura.objects.count(), 2)

    def test_dashboard_filtra_por_sensor(self):
        response = self.client.get(reverse("dashboard"), {"sensor": "G3", "parametro": "pm25"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "20,69")
        self.assertNotContains(response, "443,27")

    def test_importacion_web_rechaza_csv_incompleto(self):
        bad = SimpleUploadedFile("bad.csv", b"sensor,fecha_hora\nG3,2025-11-23T12:00:00\n", content_type="text/csv")
        response = self.client.post(reverse("importar_csv"), {"archivo": bad}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Faltan columnas")

    def test_health(self):
        response = self.client.get(reverse("health"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["lecturas"], 2)
