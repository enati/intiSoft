from django.core.paginator import Page
from jinja2 import nodes
from jinja2.ext import Extension
from jinja2.exceptions import TemplateSyntaxError, TemplateError

from .. import pagination, error_messages as errors


class PaginationExtension(Extension):
    tags = {'paginate'}

    def parse(self, parser):
        lineno = next(parser.stream).lineno

        request = nodes.Name('request', 'load')

        args = [request]

        try:
            page_obj = parser.parse_expression()
            args.append(page_obj)
        except TemplateSyntaxError:
            raise TemplateSyntaxError(errors.MISSING_FIRST_ARG, lineno)

        try:
            num_links = parser.parse_expression()
            args.append(num_links)
        except TemplateSyntaxError:
            raise TemplateSyntaxError(errors.MISSING_SECOND_ARG, lineno)

        try:
            var_name = parser.parse_expression().name
        except TemplateSyntaxError:
            raise TemplateSyntaxError(errors.MISSING_THIRD_ARG, lineno)

        try:
            page_kwarg = parser.parse_expression()
            args.append(page_kwarg)
        except TemplateSyntaxError:
            pass

        call_node = self.call_method('_make_paginator', args)
        body = parser.parse_statements(['name:endpaginate'], drop_needle=True)
        body.insert(0, nodes.Assign(nodes.Name(var_name, 'store'), call_node))
        return body

    @staticmethod
    def _make_paginator(request, page_obj, num_links, page_kwarg=None):
        if not isinstance(page_obj, Page):
            raise TemplateError(errors.WRONG_FIRST_ARG)

        if not isinstance(num_links, int):
            raise TemplateError(errors.WRONG_SECOND_ARG)

        paginator = pagination.make_paginator(page_obj, num_links)
        query = pagination.process_querystring(request, page_kwarg) if request else None

        if query:
            paginator.query = query

        return paginator
