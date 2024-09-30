# coding: utf-8

"""
    Insights.Api

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: 1.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from elexonpy.api_client import ApiClient


class BalancingServicesAdjustmentDisaggregatedApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def balancing_nonbm_disbsad_details_get(self, settlement_date, settlement_period, **kwargs):  # noqa: E501
        """Disaggregated balancing services adjustment per settlement period (DISBSAD)  # noqa: E501

        This endpoint provides disaggregated balancing services adjustment data for a single settlement period. The  response includes all the buying and selling actions that occurred during that settlement period.                Date parameter must be provided in the exact format yyyy-MM-dd.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.balancing_nonbm_disbsad_details_get(settlement_date, settlement_period, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param date settlement_date: The settlement date to query. (required)
        :param int settlement_period: The settlement period to query. This should be an integer from 1-50 inclusive. (required)
        :param str format: Response data format. Use json/xml to include metadata.
        :return: InsightsApiModelsResponsesResponseWithMetadata1InsightsApiModelsResponsesBalancingDisaggregatedBalancingServicesAdjustmentDetailsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.balancing_nonbm_disbsad_details_get_with_http_info(settlement_date, settlement_period, **kwargs)  # noqa: E501
        else:
            (data) = self.balancing_nonbm_disbsad_details_get_with_http_info(settlement_date, settlement_period, **kwargs)  # noqa: E501
            return data

    def balancing_nonbm_disbsad_details_get_with_http_info(self, settlement_date, settlement_period, **kwargs):  # noqa: E501
        """Disaggregated balancing services adjustment per settlement period (DISBSAD)  # noqa: E501

        This endpoint provides disaggregated balancing services adjustment data for a single settlement period. The  response includes all the buying and selling actions that occurred during that settlement period.                Date parameter must be provided in the exact format yyyy-MM-dd.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.balancing_nonbm_disbsad_details_get_with_http_info(settlement_date, settlement_period, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param date settlement_date: The settlement date to query. (required)
        :param int settlement_period: The settlement period to query. This should be an integer from 1-50 inclusive. (required)
        :param str format: Response data format. Use json/xml to include metadata.
        :return: InsightsApiModelsResponsesResponseWithMetadata1InsightsApiModelsResponsesBalancingDisaggregatedBalancingServicesAdjustmentDetailsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['settlement_date', 'settlement_period', 'format']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method balancing_nonbm_disbsad_details_get" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'settlement_date' is set
        if ('settlement_date' not in params or
                params['settlement_date'] is None):
            raise ValueError("Missing the required parameter `settlement_date` when calling `balancing_nonbm_disbsad_details_get`")  # noqa: E501
        # verify the required parameter 'settlement_period' is set
        if ('settlement_period' not in params or
                params['settlement_period'] is None):
            raise ValueError("Missing the required parameter `settlement_period` when calling `balancing_nonbm_disbsad_details_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'settlement_date' in params:
            query_params.append(('settlementDate', params['settlement_date']))  # noqa: E501
        if 'settlement_period' in params:
            query_params.append(('settlementPeriod', params['settlement_period']))  # noqa: E501
        if 'format' in params:
            query_params.append(('format', params['format']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['text/plain', 'application/json', 'text/json', 'application/xml', 'text/xml', 'text/csv'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/balancing/nonbm/disbsad/details', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='InsightsApiModelsResponsesResponseWithMetadata1InsightsApiModelsResponsesBalancingDisaggregatedBalancingServicesAdjustmentDetailsResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def balancing_nonbm_disbsad_summary_get(self, _from, to, **kwargs):  # noqa: E501
        """Disaggregated balancing services adjustment time series (DISBSAD)  # noqa: E501

        This endpoint provides disaggregated balancing services adjustment data batched by settlement period. Each  batch in the time series contains a summary of all records for that settlement period, detailing the number of  buy and sell actions, price information and volume information.    By default, the from and to parameters filter the data by start time inclusively. If the settlementPeriodFrom or  settlementPeriodTo parameters are provided, the corresponding from or to parameter instead filters on settlement  date, allowing for searching by a combination of start time and/or settlement date & settlement period.  Note: When filtering via settlement date, from/to are treated as Dates only, with the time being ignored. For  example, 2022-06-01T00:00Z and 2022-06-01T11:11Z are both treated as the settlement date 2022-06-01.                All Dates and DateTimes should be expressed as defined within  <a href=\"https://datatracker.ietf.org/doc/html/rfc3339#section-5.6\" target=\"_blank\">RFC 3339</a>.                Some examples of date parameter combinations are shown below.                Filtering from start time to start time:                    /balancing/nonbm/disbsad/summary?from=2022-06-01T00:00Z&to=2022-07-01T00:00Z                Filtering from start time to settlement date and period:                    /balancing/nonbm/disbsad/summary?from=2022-06-01T00:00Z&to=2022-07-01T00:00Z&settlementPeriodTo=1                Filtering from settlement date and period to start time:                    /balancing/nonbm/disbsad/summary?from=2022-06-01T00:00Z&to=2022-07-01T00:00Z&settlementPeriodFrom=1                Filtering from settlement date and period to settlement date and period:                    /balancing/nonbm/disbsad/summary?from=2022-06-01T00:00Z&to=2022-07-01T00:00Z&settlementPeriodFrom=1&settlementPeriodTo=1  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.balancing_nonbm_disbsad_summary_get(_from, to, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param datetime _from: The \"from\" start time or settlement date for the filter. (required)
        :param datetime to: The \"to\" start time or settlement date for the filter. (required)
        :param int settlement_period_from: The \"from\" settlement period for the filter. This should be an integer from 1-50 inclusive.
        :param int settlement_period_to: The \"to\" settlement period for the filter. This should be an integer from 1-50 inclusive.
        :param str format: Response data format. Use json/xml to include metadata.
        :return: InsightsApiModelsResponsesResponseWithMetadata1InsightsApiModelsResponsesBalancingDisaggregatedBalancingServicesAdjustmentSummaryResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.balancing_nonbm_disbsad_summary_get_with_http_info(_from, to, **kwargs)  # noqa: E501
        else:
            (data) = self.balancing_nonbm_disbsad_summary_get_with_http_info(_from, to, **kwargs)  # noqa: E501
            return data

    def balancing_nonbm_disbsad_summary_get_with_http_info(self, _from, to, **kwargs):  # noqa: E501
        """Disaggregated balancing services adjustment time series (DISBSAD)  # noqa: E501

        This endpoint provides disaggregated balancing services adjustment data batched by settlement period. Each  batch in the time series contains a summary of all records for that settlement period, detailing the number of  buy and sell actions, price information and volume information.    By default, the from and to parameters filter the data by start time inclusively. If the settlementPeriodFrom or  settlementPeriodTo parameters are provided, the corresponding from or to parameter instead filters on settlement  date, allowing for searching by a combination of start time and/or settlement date & settlement period.  Note: When filtering via settlement date, from/to are treated as Dates only, with the time being ignored. For  example, 2022-06-01T00:00Z and 2022-06-01T11:11Z are both treated as the settlement date 2022-06-01.                All Dates and DateTimes should be expressed as defined within  <a href=\"https://datatracker.ietf.org/doc/html/rfc3339#section-5.6\" target=\"_blank\">RFC 3339</a>.                Some examples of date parameter combinations are shown below.                Filtering from start time to start time:                    /balancing/nonbm/disbsad/summary?from=2022-06-01T00:00Z&to=2022-07-01T00:00Z                Filtering from start time to settlement date and period:                    /balancing/nonbm/disbsad/summary?from=2022-06-01T00:00Z&to=2022-07-01T00:00Z&settlementPeriodTo=1                Filtering from settlement date and period to start time:                    /balancing/nonbm/disbsad/summary?from=2022-06-01T00:00Z&to=2022-07-01T00:00Z&settlementPeriodFrom=1                Filtering from settlement date and period to settlement date and period:                    /balancing/nonbm/disbsad/summary?from=2022-06-01T00:00Z&to=2022-07-01T00:00Z&settlementPeriodFrom=1&settlementPeriodTo=1  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.balancing_nonbm_disbsad_summary_get_with_http_info(_from, to, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param datetime _from: The \"from\" start time or settlement date for the filter. (required)
        :param datetime to: The \"to\" start time or settlement date for the filter. (required)
        :param int settlement_period_from: The \"from\" settlement period for the filter. This should be an integer from 1-50 inclusive.
        :param int settlement_period_to: The \"to\" settlement period for the filter. This should be an integer from 1-50 inclusive.
        :param str format: Response data format. Use json/xml to include metadata.
        :return: InsightsApiModelsResponsesResponseWithMetadata1InsightsApiModelsResponsesBalancingDisaggregatedBalancingServicesAdjustmentSummaryResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['_from', 'to', 'settlement_period_from', 'settlement_period_to', 'format']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method balancing_nonbm_disbsad_summary_get" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter '_from' is set
        if ('_from' not in params or
                params['_from'] is None):
            raise ValueError("Missing the required parameter `_from` when calling `balancing_nonbm_disbsad_summary_get`")  # noqa: E501
        # verify the required parameter 'to' is set
        if ('to' not in params or
                params['to'] is None):
            raise ValueError("Missing the required parameter `to` when calling `balancing_nonbm_disbsad_summary_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []
        if '_from' in params:
            query_params.append(('from', params['_from']))  # noqa: E501
        if 'to' in params:
            query_params.append(('to', params['to']))  # noqa: E501
        if 'settlement_period_from' in params:
            query_params.append(('settlementPeriodFrom', params['settlement_period_from']))  # noqa: E501
        if 'settlement_period_to' in params:
            query_params.append(('settlementPeriodTo', params['settlement_period_to']))  # noqa: E501
        if 'format' in params:
            query_params.append(('format', params['format']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['text/plain', 'application/json', 'text/json', 'application/xml', 'text/xml', 'text/csv'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/balancing/nonbm/disbsad/summary', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='InsightsApiModelsResponsesResponseWithMetadata1InsightsApiModelsResponsesBalancingDisaggregatedBalancingServicesAdjustmentSummaryResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
