from pathlib import Path
from django.core.management.base import BaseCommand, CommandError
from monitoreo.importer import import_csv_text


class Command(BaseCommand):
    help = "Carga o actualiza lecturas desde un CSV."

    def add_arguments(self, parser):
        parser.add_argument("archivo", type=str)

    def handle(self, *args, **options):
        path = Path(options["archivo"])
        if not path.exists():
            raise CommandError(f"No existe: {path}")
        result = import_csv_text(path.read_text(encoding="utf-8-sig"))
        self.stdout.write(self.style.SUCCESS(
            f"Nuevas: {result['imported']} | Actualizadas: {result['updated']} | Errores: {len(result['errors'])}"
        ))
        for error in result["errors"][:10]:
            self.stdout.write(self.style.WARNING(error))
