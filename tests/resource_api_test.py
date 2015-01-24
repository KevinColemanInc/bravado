#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Copyright (c) 2014, Yelp, Inc.
#

"""Swagger client tests to validate 'resource api's

A sample 'resource api' is listed in the "apis" list below.
{

    "apiVersion": "1.0.0",
    "swaggerVersion": "1.2",
    "basePath": "http://petstore.swagger.wordnik.com/api",
    ...
    "apis": [
        {
            "path": "/user/{username}",
            "operations": [...]
        }
    ]
    ...
}
"""

from bravado.compat import json
import unittest

import httpretty

from bravado.client import SwaggerClient
from bravado.exception import SwaggerError


class ResourceApiTest(unittest.TestCase):

    def setUp(self):
        parameter = {
            "paramType": "query",
            "name": "test_param",
            "type": "string"
        }
        operation = {
            "method": "GET",
            "nickname": "testHTTP",
            "type": "void",
            "parameters": [parameter]
        }
        api = {
            "path": "/test_http",
            "operations": [operation]
        }
        self.response = {
            "swaggerVersion": "1.2",
            "basePath": "/",
            "apis": [api]
        }

    def register_urls(self):
        httpretty.register_uri(
            httpretty.GET, "http://localhost/api-docs",
            body=json.dumps({
                "swaggerVersion": "1.2",
                "apis": [{
                    "path": "/api_test"
                }]
            }))
        httpretty.register_uri(
            httpretty.GET, "http://localhost/api-docs/api_test",
            body=json.dumps(self.response))

    @httpretty.activate
    def test_error_on_missing_attr(self):
        def iterate_test(field):
            self.response["apis"][0].pop(field)
            self.register_urls()
            self.assertRaises(SwaggerError, SwaggerClient.from_url,
                              u'http://localhost/api-docs')

        for field in ('path', 'operations'):
            iterate_test(field)


if __name__ == '__main__':
    unittest.main()
