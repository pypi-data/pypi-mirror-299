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
from elexonpy.api.balancing_mechanism_dynamic_api import BalancingMechanismDynamicApi  # noqa: E501
from elexonpy.rest import ApiException


class TestBalancingMechanismDynamicApi(unittest.TestCase):
    """BalancingMechanismDynamicApi unit test stubs"""

    def setUp(self):
        self.api = BalancingMechanismDynamicApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_balancing_dynamic_all_get(self):
        """Test case for balancing_dynamic_all_get

        Market-wide dynamic data (SEL, SIL, MZT, MNZT, MDV, MDP, NTB, NTO, NDZ)  # noqa: E501
        """
        pass

    def test_balancing_dynamic_get(self):
        """Test case for balancing_dynamic_get

        Dynamic data per BMU (SEL, SIL, MZT, MNZT, MDV, MDP, NTB, NTO, NDZ)  # noqa: E501
        """
        pass

    def test_balancing_dynamic_rates_all_get(self):
        """Test case for balancing_dynamic_rates_all_get

        Market-wide rate data (RDRE, RURE, RDRI, RURI)  # noqa: E501
        """
        pass

    def test_balancing_dynamic_rates_get(self):
        """Test case for balancing_dynamic_rates_get

        Rate data per BMU (RDRE, RURE, RDRI, RURI)  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
