import random
from django.core.paginator import Paginator
from category.models import Phrase
from rest_framework.exceptions import NotFound


def get_word_and_category(category=None):
    """returns the category, phrase"""
    # https://stackoverflow.com/a/76893630/14665310
    if category is None or category == "":
        paginator = Paginator(
            Phrase.objects.filter(active=True, category__active=True).order_by("pk"), 25
        )
    else:
        # if choose a category specifically then even if it is not active choose a word from it.
        paginator = Paginator(
            Phrase.objects.filter(category_id=category, active=True).order_by("pk"), 25
        )
    random_page = paginator.get_page(random.choice(paginator.page_range))
    try:
        random_sample = random.choice(random_page.object_list)
    except IndexError:
        raise NotFound("No terms found.")
    return random_sample.category.name, random_sample.phrase.lower()
