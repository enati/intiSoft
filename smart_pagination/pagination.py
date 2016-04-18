import math, sys
import django
from django.http import QueryDict

PYTHON_2 = sys.version_info < (3,)
DJANGO_GTE_18 = django.VERSION >= (1, 8)


class Page:
    def __init__(self, current_page, page_number):
        self.is_current = current_page == page_number
        self.number = page_number


class Paginator:
    def __init__(self, first_page, prev_page, page_range, next_page, last_page, current_page):
        pages = list()
        for page_number in page_range:
            pages.append(Page(current_page, page_number))

        self.first = Page(current_page, first_page) if first_page is not None else None
        self.prev = Page(current_page, prev_page) if prev_page is not None else None
        self.pages = pages
        self.next = Page(current_page, next_page) if next_page is not None else None
        self.last = Page(current_page, last_page) if last_page is not None else None


def make_paginator(page_obj, num_links):
    number = page_obj.number
    page_count = len(page_obj.paginator.page_range)

    prev_page = page_obj.previous_page_number() if page_obj.has_previous() else None
    next_page = page_obj.next_page_number() if page_obj.has_next() else None

    # Try to play nice with Python 2
    # Force float division before math.ceil
    middle_point = math.ceil(num_links / 2.0)
    if PYTHON_2:
        # Convert float to int
        middle_point = int(middle_point)

    first_page = page_obj.paginator.page_range[0] if page_count > num_links and number > middle_point else None

    last_page = page_obj.paginator.page_range[-1]

    if num_links % 2 == 1:
        not_last_section = number <= (last_page - middle_point)
    else:
        not_last_section = number < (last_page - middle_point)

    last_page = last_page if page_count > num_links and not_last_section else None

    if first_page is None:
        page_range = page_obj.paginator.page_range[:num_links]
    elif last_page is None:
        page_range = page_obj.paginator.page_range[-num_links:]
    else:
        start = number - (middle_point - 1) - 1  # zero indexed
        end = number + middle_point - 1  # zero indexed

        # fix for even number of links
        if num_links % 2 == 0:
            end += 1

        page_range = page_obj.paginator.page_range[start:end]

    return Paginator(first_page, prev_page, page_range, next_page, last_page, number)


def process_querystring(request, page_kwarg):
    if page_kwarg and (len(request.GET) > 0):
        qs = request.GET.copy()

        if DJANGO_GTE_18 or not isinstance(qs, QueryDict):
            new_qs = QueryDict('', mutable=True)
            new_qs.update(qs)
            qs = new_qs

        if page_kwarg in qs:
            qs.pop(page_kwarg)

        return qs.urlencode()

    return ''
