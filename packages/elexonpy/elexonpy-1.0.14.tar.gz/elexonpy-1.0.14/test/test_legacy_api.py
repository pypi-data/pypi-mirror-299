# coding: utf-8

"""
    Insights.Api

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: 1.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import unittest

import elexonpy
from elexonpy.api.legacy_api import LegacyApi  # noqa: E501
from elexonpy.rest import ApiException


class TestLegacyApi(unittest.TestCase):
    """LegacyApi unit test stubs"""

    def setUp(self):
        self.api = LegacyApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_interop_message_detail_retrieval_get(self):
        """Test case for interop_message_detail_retrieval_get

        This endpoint is obsolete, and this location may be removed with no further notice. Use /remit/* or /datasets/REMIT endpoints instead.  # noqa: E501
        """
        pass

    def test_interop_message_list_retrieval_get(self):
        """Test case for interop_message_list_retrieval_get

        This endpoint is obsolete, and this location may be removed with no further notice. Use /remit/* or /datasets/REMIT endpoints instead.  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
