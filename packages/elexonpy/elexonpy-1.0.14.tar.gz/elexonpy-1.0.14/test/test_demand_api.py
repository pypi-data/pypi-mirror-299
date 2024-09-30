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
from elexonpy.api.demand_api import DemandApi  # noqa: E501
from elexonpy.rest import ApiException


class TestDemandApi(unittest.TestCase):
    """DemandApi unit test stubs"""

    def setUp(self):
        self.api = DemandApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_demand_actual_total_get(self):
        """Test case for demand_actual_total_get

        Actual total load (ATL/B0610)  # noqa: E501
        """
        pass

    def test_demand_get(self):
        """Test case for demand_get

        This endpoint is obsolete, and this location may be removed with no further notice.   # noqa: E501
        """
        pass

    def test_demand_outturn_daily_get(self):
        """Test case for demand_outturn_daily_get

        Initial National Demand outturn per day (INDOD)  # noqa: E501
        """
        pass

    def test_demand_outturn_daily_stream_get(self):
        """Test case for demand_outturn_daily_stream_get

        Initial National Demand outturn per day (INDOD) stream  # noqa: E501
        """
        pass

    def test_demand_outturn_get(self):
        """Test case for demand_outturn_get

        Initial National Demand outturn (INDO)  # noqa: E501
        """
        pass

    def test_demand_outturn_stream_get(self):
        """Test case for demand_outturn_stream_get

        Initial National Demand outturn (INDO) stream  # noqa: E501
        """
        pass

    def test_demand_outturn_summary_get(self):
        """Test case for demand_outturn_summary_get

        System demand summary (FUELINST)  # noqa: E501
        """
        pass

    def test_demand_peak_get(self):
        """Test case for demand_peak_get

        Peak demand per day (ITSDO)  # noqa: E501
        """
        pass

    def test_demand_peak_indicative_get(self):
        """Test case for demand_peak_indicative_get

        Indicative peak demand per day (S0142, ITSDO, FUELHH)  # noqa: E501
        """
        pass

    def test_demand_peak_indicative_operational_triad_season_get(self):
        """Test case for demand_peak_indicative_operational_triad_season_get

        Operational data demand peaks for a Triad season (ITSDO, FUELHH)  # noqa: E501
        """
        pass

    def test_demand_peak_indicative_settlement_triad_season_get(self):
        """Test case for demand_peak_indicative_settlement_triad_season_get

        Settlement data demand peaks for a Triad season (S0142)  # noqa: E501
        """
        pass

    def test_demand_peak_triad_get(self):
        """Test case for demand_peak_triad_get

        Triad demand peaks (S0142, ITSDO, FUELHH)  # noqa: E501
        """
        pass

    def test_demand_rolling_system_demand_get(self):
        """Test case for demand_rolling_system_demand_get

        This endpoint is obsolete, and this location may be removed with no further notice.   # noqa: E501
        """
        pass

    def test_demand_stream_get(self):
        """Test case for demand_stream_get

        This endpoint is obsolete, and this location may be removed with no further notice.   # noqa: E501
        """
        pass

    def test_demand_summary_get(self):
        """Test case for demand_summary_get

        This endpoint is obsolete, and this location may be removed with no further notice.   # noqa: E501
        """
        pass

    def test_demand_total_actual_get(self):
        """Test case for demand_total_actual_get

        This endpoint is obsolete, and this location may be removed with no further notice.   # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
