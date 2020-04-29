from bookstore_statistics.models import Book, Publisher
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Avg, Max, Min, Count, FloatField, Q


@api_view(['GET'])
def bookstore_summary(request, flag):

    if request.method == 'GET' and flag == 'all':
        total_number_of_books = Book.objects.count()
        total_number_of_books_publisher_name = Book.objects.filter(publisher__name='Publisher1').count()
        books = Book.objects.all()
        books_price_statistics = books.aggregate(
            Min('price'), Max('price'), Avg('price'), price_diff=Max(
                'price', output_field=FloatField()) - Avg('price', output_field=FloatField())
        )
        publishers_num_books_q = Publisher.objects.annotate(num_books=Count('book')).values('name', 'num_books')
        above_2 = Count('book', filter=Q(book__rating__gt=2))
        below_2 = Count('book', filter=Q(book__rating__lte=2))
        publisher_ranks = Publisher.objects.annotate(below_2=below_2).annotate(above_2=above_2)
        top_2_publishers = Publisher.objects.annotate(num_books=Count('book')).order_by('-num_books')[:2]

        return Response({
            'total_number_of_books': total_number_of_books,
            'total_number_of_books_publisher_name': total_number_of_books_publisher_name,
            'books_price_statistics': books_price_statistics,
            'publisher_num_books': {x['name']: x['num_books'] for x in publishers_num_books_q},
            'books_rank_below_2': {x.name: x.below_2 for x in publisher_ranks},
            'books_rank_above_2': {x.name: x.above_2 for x in publisher_ranks},
            'top_2_publishers_number_of_books': {x.name: x.num_books for x in top_2_publishers},
        })
