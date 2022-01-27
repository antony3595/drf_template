from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class AppPagination(PageNumberPagination):
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current': self.page.number,
            'results': data
        })
