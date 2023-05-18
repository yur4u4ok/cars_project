import math

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class PagePagination(PageNumberPagination):
    page_size = 10

    def get_paginated_response(self, data):
        count = self.page.paginator.count
        total_pages = math.ceil(count / self.get_page_size(self.request))
        return Response({
            "total_items": count,
            "total_pages": total_pages,
            "previous_page": self.get_previous_link(),
            "next_page": self.get_next_link(),
            "data": data
        })
