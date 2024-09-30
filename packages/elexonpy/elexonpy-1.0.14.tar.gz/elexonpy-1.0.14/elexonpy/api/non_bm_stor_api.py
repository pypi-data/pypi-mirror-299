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


class NonBMSTORApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def balancing_nonbm_stor_events_get(self, count, **kwargs):  # noqa: E501
        """Non-BM STOR events (NONBM)  # noqa: E501

        This endpoint provides data about the start of NGESO Short Term Operating Reserves (STOR) events. This is  activity that is outside of the Balancing Mechanism and takes place to meet the need to  increase generation or decrease demand. Each result has a non-zero generation value which was preceded by a zero  generation value.                By default, the before parameter filters the data by start time. If the settlementPeriodBefore parameter is  provided, the before parameter instead filters on settlement date, allowing for searching by start time or  settlement date & settlement period.  Note: When filtering via settlement date, before is treated as a Date only, with the time being ignored. For  example, 2022-06-01T00:00Z and 2022-06-01T11:11Z are both treated as the settlement date 2022-06-01.                All Dates and DateTimes should be expressed as defined within  <a href=\"https://datatracker.ietf.org/doc/html/rfc3339#section-5.6\" target=\"_blank\">RFC 3339</a>.                Some examples of date parameter combinations are shown below.                Filtering latest 3 events:                    /balancing/nonbm/stor/events?count=3                Filtering latest 3 events before start time:                    /balancing/nonbm/stor/events?before=2022-08-01T00:00Z&count=3                Filtering latest 3 events before settlement date and settlement period:                    /balancing/nonbm/stor/events?before=2022-08-01T00:00Z&settlementPeriodBefore=48&count=3  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.balancing_nonbm_stor_events_get(count, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int count: The number of events to return. (required)
        :param datetime before: If specified, filters events to those with a start time before or at the date, or a settlement date before the date if  settlementPeriodBefore is also specified.  If omitted, latest events are returned.
        :param int settlement_period_before: Filters events to those with a settlement period before or at the value.  Before parameter must be specified if this is specified.
        :param str format: Response data format. Use json/xml to include metadata.
        :return: InsightsApiModelsResponsesResponseWithMetadata1InsightsApiModelsResponsesBalancingNonBmStorResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.balancing_nonbm_stor_events_get_with_http_info(count, **kwargs)  # noqa: E501
        else:
            (data) = self.balancing_nonbm_stor_events_get_with_http_info(count, **kwargs)  # noqa: E501
            return data

    def balancing_nonbm_stor_events_get_with_http_info(self, count, **kwargs):  # noqa: E501
        """Non-BM STOR events (NONBM)  # noqa: E501

        This endpoint provides data about the start of NGESO Short Term Operating Reserves (STOR) events. This is  activity that is outside of the Balancing Mechanism and takes place to meet the need to  increase generation or decrease demand. Each result has a non-zero generation value which was preceded by a zero  generation value.                By default, the before parameter filters the data by start time. If the settlementPeriodBefore parameter is  provided, the before parameter instead filters on settlement date, allowing for searching by start time or  settlement date & settlement period.  Note: When filtering via settlement date, before is treated as a Date only, with the time being ignored. For  example, 2022-06-01T00:00Z and 2022-06-01T11:11Z are both treated as the settlement date 2022-06-01.                All Dates and DateTimes should be expressed as defined within  <a href=\"https://datatracker.ietf.org/doc/html/rfc3339#section-5.6\" target=\"_blank\">RFC 3339</a>.                Some examples of date parameter combinations are shown below.                Filtering latest 3 events:                    /balancing/nonbm/stor/events?count=3                Filtering latest 3 events before start time:                    /balancing/nonbm/stor/events?before=2022-08-01T00:00Z&count=3                Filtering latest 3 events before settlement date and settlement period:                    /balancing/nonbm/stor/events?before=2022-08-01T00:00Z&settlementPeriodBefore=48&count=3  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.balancing_nonbm_stor_events_get_with_http_info(count, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int count: The number of events to return. (required)
        :param datetime before: If specified, filters events to those with a start time before or at the date, or a settlement date before the date if  settlementPeriodBefore is also specified.  If omitted, latest events are returned.
        :param int settlement_period_before: Filters events to those with a settlement period before or at the value.  Before parameter must be specified if this is specified.
        :param str format: Response data format. Use json/xml to include metadata.
        :return: InsightsApiModelsResponsesResponseWithMetadata1InsightsApiModelsResponsesBalancingNonBmStorResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['count', 'before', 'settlement_period_before', 'format']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method balancing_nonbm_stor_events_get" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'count' is set
        if ('count' not in params or
                params['count'] is None):
            raise ValueError("Missing the required parameter `count` when calling `balancing_nonbm_stor_events_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'count' in params:
            query_params.append(('count', params['count']))  # noqa: E501
        if 'before' in params:
            query_params.append(('before', params['before']))  # noqa: E501
        if 'settlement_period_before' in params:
            query_params.append(('settlementPeriodBefore', params['settlement_period_before']))  # noqa: E501
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
            '/balancing/nonbm/stor/events', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='InsightsApiModelsResponsesResponseWithMetadata1InsightsApiModelsResponsesBalancingNonBmStorResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def balancing_nonbm_stor_get(self, _from, to, **kwargs):  # noqa: E501
        """Non-BM STOR time series (NONBM)  # noqa: E501

        This endpoint provides data about the Short Term Operating Reserves (STOR) that have been made use of  by NGESO. This is activity that is outside of the Balancing Mechanism and takes place to meet the need to  increase generation or decrease demand.                By default, the from and to parameters filter the data by time inclusively. If the settlementPeriodFrom or  settlementPeriodTo parameters are provided, the corresponding from or to parameter instead filters on settlement  date, allowing for searching by a combination of time and/or settlement date & settlement period.  Note: When filtering via settlement date, from/to are treated as Dates only, with the time being ignored. For  example, 2022-06-01T00:00Z and 2022-06-01T11:11Z are both treated as the settlement date 2022-06-01.                All Dates and DateTimes should be expressed as defined within  <a href=\"https://datatracker.ietf.org/doc/html/rfc3339#section-5.6\" target=\"_blank\">RFC 3339</a>.                Some examples of date parameter combinations are shown below.                Filtering from start time to start time:                    /balancing/nonbm/stor?from=2022-06-01T00:00Z&to=2022-07-01T00:00Z                Filtering from start time to settlement date and period:                    /balancing/nonbm/stor?from=2022-06-01T00:00Z&to=2022-07-01T00:00Z&settlementPeriodTo=1                Filtering from settlement date and period to start time:                    /balancing/nonbm/stor?from=2022-06-01T00:00Z&to=2022-07-01T00:00Z&settlementPeriodFrom=1                Filtering from settlement date and period to settlement date and period:                    /balancing/nonbm/stor?from=2022-06-01T00:00Z&to=2022-07-01T00:00Z&settlementPeriodFrom=1&settlementPeriodTo=1  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.balancing_nonbm_stor_get(_from, to, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param datetime _from: The \"from\" start time or settlement date for the filter. (required)
        :param datetime to: The \"to\" start time or settlement date for the filter. (required)
        :param int settlement_period_from: The \"from\" settlement period for the filter. This should be an integer from 1-50 inclusive.
        :param int settlement_period_to: The \"to\" settlement period for the filter. This should be an integer from 1-50 inclusive.
        :param bool include_zero: Include data points with a generation of zero.
        :param str format: Response data format. Use json/xml to include metadata.
        :return: InsightsApiModelsResponsesResponseWithMetadata1InsightsApiModelsResponsesBalancingNonBmStorResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.balancing_nonbm_stor_get_with_http_info(_from, to, **kwargs)  # noqa: E501
        else:
            (data) = self.balancing_nonbm_stor_get_with_http_info(_from, to, **kwargs)  # noqa: E501
            return data

    def balancing_nonbm_stor_get_with_http_info(self, _from, to, **kwargs):  # noqa: E501
        """Non-BM STOR time series (NONBM)  # noqa: E501

        This endpoint provides data about the Short Term Operating Reserves (STOR) that have been made use of  by NGESO. This is activity that is outside of the Balancing Mechanism and takes place to meet the need to  increase generation or decrease demand.                By default, the from and to parameters filter the data by time inclusively. If the settlementPeriodFrom or  settlementPeriodTo parameters are provided, the corresponding from or to parameter instead filters on settlement  date, allowing for searching by a combination of time and/or settlement date & settlement period.  Note: When filtering via settlement date, from/to are treated as Dates only, with the time being ignored. For  example, 2022-06-01T00:00Z and 2022-06-01T11:11Z are both treated as the settlement date 2022-06-01.                All Dates and DateTimes should be expressed as defined within  <a href=\"https://datatracker.ietf.org/doc/html/rfc3339#section-5.6\" target=\"_blank\">RFC 3339</a>.                Some examples of date parameter combinations are shown below.                Filtering from start time to start time:                    /balancing/nonbm/stor?from=2022-06-01T00:00Z&to=2022-07-01T00:00Z                Filtering from start time to settlement date and period:                    /balancing/nonbm/stor?from=2022-06-01T00:00Z&to=2022-07-01T00:00Z&settlementPeriodTo=1                Filtering from settlement date and period to start time:                    /balancing/nonbm/stor?from=2022-06-01T00:00Z&to=2022-07-01T00:00Z&settlementPeriodFrom=1                Filtering from settlement date and period to settlement date and period:                    /balancing/nonbm/stor?from=2022-06-01T00:00Z&to=2022-07-01T00:00Z&settlementPeriodFrom=1&settlementPeriodTo=1  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.balancing_nonbm_stor_get_with_http_info(_from, to, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param datetime _from: The \"from\" start time or settlement date for the filter. (required)
        :param datetime to: The \"to\" start time or settlement date for the filter. (required)
        :param int settlement_period_from: The \"from\" settlement period for the filter. This should be an integer from 1-50 inclusive.
        :param int settlement_period_to: The \"to\" settlement period for the filter. This should be an integer from 1-50 inclusive.
        :param bool include_zero: Include data points with a generation of zero.
        :param str format: Response data format. Use json/xml to include metadata.
        :return: InsightsApiModelsResponsesResponseWithMetadata1InsightsApiModelsResponsesBalancingNonBmStorResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['_from', 'to', 'settlement_period_from', 'settlement_period_to', 'include_zero', 'format']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method balancing_nonbm_stor_get" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter '_from' is set
        if ('_from' not in params or
                params['_from'] is None):
            raise ValueError("Missing the required parameter `_from` when calling `balancing_nonbm_stor_get`")  # noqa: E501
        # verify the required parameter 'to' is set
        if ('to' not in params or
                params['to'] is None):
            raise ValueError("Missing the required parameter `to` when calling `balancing_nonbm_stor_get`")  # noqa: E501

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
        if 'include_zero' in params:
            query_params.append(('includeZero', params['include_zero']))  # noqa: E501
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
            '/balancing/nonbm/stor', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='InsightsApiModelsResponsesResponseWithMetadata1InsightsApiModelsResponsesBalancingNonBmStorResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
