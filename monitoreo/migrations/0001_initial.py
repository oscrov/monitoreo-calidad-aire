from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="Sensor",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("codigo", models.CharField(max_length=50, unique=True)),
                ("nombre", models.CharField(blank=True, max_length=120)),
                ("ubicacion", models.CharField(blank=True, max_length=200)),
                ("activo", models.BooleanField(default=True)),
            ],
            options={"ordering": ["codigo"]},
        ),
        migrations.CreateModel(
            name="Lectura",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("fecha_hora", models.DateTimeField()),
                ("pm1", models.FloatField()),
                ("pm25", models.FloatField()),
                ("pm4", models.FloatField()),
                ("pm10", models.FloatField()),
                ("co2", models.FloatField()),
                ("sensor", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="lecturas", to="monitoreo.sensor")),
            ],
            options={"ordering": ["fecha_hora"]},
        ),
        migrations.AddConstraint(
            model_name="lectura",
            constraint=models.UniqueConstraint(fields=("sensor", "fecha_hora"), name="lectura_sensor_fecha_unica"),
        ),
    ]
