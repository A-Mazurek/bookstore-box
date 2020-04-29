import csv
import pytz
import dateutil.parser
from django.core.management.base import BaseCommand
from bookstore_statistics.models import Author, Publisher, Book, Store


class Command(BaseCommand):
    help = 'Script to automatically load the CSV \
        data into a relational database'

    def add_arguments(self, parser):
        parser.add_argument(
            'all_csv',
            type=str,
            help='csv name to load into database'
        )

    def handle(self, *args, **options):
        all_csv = options['all_csv']

        if all_csv:
            stores_csv = 'data/stores.csv'
            books_csv = 'data/books.csv'
            publishers_csv = 'data/publishers.csv'
            authors_csv = 'data/authors.csv'

        Author.objects.all().delete()
        Publisher.objects.all().delete()
        Book.objects.all().delete()
        Store.objects.all().delete()


        with open(authors_csv) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            authors = []

            for row in csv_reader:
                line_count += 1
                if line_count > 1:
                    authors.append(Author(
                        id=row[0],
                        name=row[1],
                        age=int(row[2])
                    ))
            Author.objects.bulk_create(authors)


        with open(publishers_csv) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            publishers = []

            for row in csv_reader:
                line_count += 1
                if line_count > 1:
                    publishers.append(Publisher(
                        id=row[0],
                        name=row[1]
                    ))
            Publisher.objects.bulk_create(publishers)


        with open(books_csv) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0

            for row in csv_reader:
                line_count += 1
                if line_count > 1:
                    book = Book.objects.create(
                        id=row[0],
                        name=row[1],
                        pages=row[2],
                        price=row[3],
                        rating=row[4],
                        publisher=Publisher.objects.get(id=int(row[6])),
                        pubdate=dateutil.parser.parse(row[7]).astimezone(pytz.UTC)
                    )
                    book.authors.all().delete()
                    book.authors.add(Author.objects.get(id=int(row[5])))
                    book.save()


        with open(stores_csv) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            stores = []

            for row in csv_reader:
                line_count += 1
                if line_count > 1:
                    stores.append(Store(
                        id=row[0],
                        name=row[0]
                    ))
            Store.objects.bulk_create(stores)

        return 'All products added to database!'
