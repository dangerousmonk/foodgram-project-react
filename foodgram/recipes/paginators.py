from rest_framework.pagination import PageNumberPagination


class CustomPageNumberPaginator(PageNumberPagination):
    page_size_query_param = 'limit'
