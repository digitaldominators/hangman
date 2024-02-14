import argparse

from django.core.management.base import BaseCommand, CommandError
from category.models import Phrase, Category


class Command(BaseCommand):
    help = "Adds list of words to a category"

    def add_arguments(self, parser):
        parser.add_argument("file", nargs="+", type=argparse.FileType("r"))
        parser.add_argument(
            "--id",
            type=int,
            help="Use the id of the category",
        )
        parser.add_argument(
            "--category",
            type=str,
            help="Use the category name or create a new category if it doesn't exist to add the words",
        )

    def handle(self, *args, **options):
        created = False
        if options.get("id") is None and options.get("category") is None:
            raise CommandError("Need to specify a category or id")
        elif options.get("id") and options.get("category"):
            raise CommandError("Can only specify a category or id")
        elif options.get("category"):
            category, created = Category.objects.get_or_create(
                name=options.get("category")
            )
        elif options.get("id"):
            try:
                category = Category.objects.get(id=options.get("id"))
            except Category.DoesNotExist:
                raise CommandError(f"No Category found with id {options.get('id')}")

        if created:
            self.stdout.write(
                self.style.SUCCESS(f"Created new category '{category.name}'")
            )

        with options["file"][0] as file:
            words = file.readlines()

        words = [word.strip() for word in words if word.strip() != ""]
        self.stdout.write(self.style.SUCCESS(f"Found {len(words)} words"))

        phrases = []
        for word in words:
            phrase = Phrase(phrase=word, category=category)
            phrases.append(phrase)

        phrase_objects = Phrase.objects.bulk_create(phrases, ignore_conflicts=True)

        self.stdout.write(
            self.style.SUCCESS(f"Created the phrases in category '{category.name}'")
        )
