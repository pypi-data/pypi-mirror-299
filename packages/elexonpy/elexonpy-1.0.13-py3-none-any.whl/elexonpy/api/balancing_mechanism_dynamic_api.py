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


class BalancingMechanismDynamicApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def balancing_dynamic_all_get(self, settlement_date, settlement_period, **kwargs):  # noqa: E501
        """Market-wide dynamic data (SEL, SIL, MZT, MNZT, MDV, MDP, NTB, NTO, NDZ)  # noqa: E501

        This endpoint provides the dynamic data for multiple requested BMUs or all BMUs, excluding dynamic rate data.  It returns the data valid for a single settlement period. This includes a snapshot of data valid at the start  of the settlement period, and any changes published during that settlement period.                By default, all of the relevant datasets are returned: SIL, SEL, NDZ, NTB, NTO, MZT, MNZT, MDV & MDP.  The results from each dataset are transformed to a common response model, with the common integer field *Value*  mapped from the fields *Level*, *Period*, *Volume* or *Notice* in the original dataset, as relevant.                The settlement period must be specified as a date and settlement period. The date parameter must be provided in the exact format yyyy-MM-dd.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.balancing_dynamic_all_get(settlement_date, settlement_period, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param date settlement_date: The settlement date or datetime to filter. (required)
        :param int settlement_period: The settlement period to filter. This should be an integer from 1-50 inclusive. (required)
        :param list[str] bm_unit: The BM Units to query. Elexon or NGC BMU IDs can be used. If omitted, results for all BM units will be returned.
        :param list[str] dataset: Datasets to filter. If omitted, all datasets will be returned.
        :param str format: Response data format. Use json/xml to include metadata.
        :return: InsightsApiModelsResponsesResponseWithMetadata1InsightsApiModelsResponsesBalancingDynamicDynamicData
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.balancing_dynamic_all_get_with_http_info(settlement_date, settlement_period, **kwargs)  # noqa: E501
        else:
            (data) = self.balancing_dynamic_all_get_with_http_info(settlement_date, settlement_period, **kwargs)  # noqa: E501
            return data

    def balancing_dynamic_all_get_with_http_info(self, settlement_date, settlement_period, **kwargs):  # noqa: E501
        """Market-wide dynamic data (SEL, SIL, MZT, MNZT, MDV, MDP, NTB, NTO, NDZ)  # noqa: E501

        This endpoint provides the dynamic data for multiple requested BMUs or all BMUs, excluding dynamic rate data.  It returns the data valid for a single settlement period. This includes a snapshot of data valid at the start  of the settlement period, and any changes published during that settlement period.                By default, all of the relevant datasets are returned: SIL, SEL, NDZ, NTB, NTO, MZT, MNZT, MDV & MDP.  The results from each dataset are transformed to a common response model, with the common integer field *Value*  mapped from the fields *Level*, *Period*, *Volume* or *Notice* in the original dataset, as relevant.                The settlement period must be specified as a date and settlement period. The date parameter must be provided in the exact format yyyy-MM-dd.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.balancing_dynamic_all_get_with_http_info(settlement_date, settlement_period, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param date settlement_date: The settlement date or datetime to filter. (required)
        :param int settlement_period: The settlement period to filter. This should be an integer from 1-50 inclusive. (required)
        :param list[str] bm_unit: The BM Units to query. Elexon or NGC BMU IDs can be used. If omitted, results for all BM units will be returned.
        :param list[str] dataset: Datasets to filter. If omitted, all datasets will be returned.
        :param str format: Response data format. Use json/xml to include metadata.
        :return: InsightsApiModelsResponsesResponseWithMetadata1InsightsApiModelsResponsesBalancingDynamicDynamicData
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['settlement_date', 'settlement_period', 'bm_unit', 'dataset', 'format']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method balancing_dynamic_all_get" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'settlement_date' is set
        if ('settlement_date' not in params or
                params['settlement_date'] is None):
            raise ValueError("Missing the required parameter `settlement_date` when calling `balancing_dynamic_all_get`")  # noqa: E501
        # verify the required parameter 'settlement_period' is set
        if ('settlement_period' not in params or
                params['settlement_period'] is None):
            raise ValueError("Missing the required parameter `settlement_period` when calling `balancing_dynamic_all_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'settlement_date' in params:
            query_params.append(('settlementDate', params['settlement_date']))  # noqa: E501
        if 'settlement_period' in params:
            query_params.append(('settlementPeriod', params['settlement_period']))  # noqa: E501
        if 'bm_unit' in params:
            query_params.append(('bmUnit', params['bm_unit']))  # noqa: E501
            collection_formats['bmUnit'] = 'multi'  # noqa: E501
        if 'dataset' in params:
            query_params.append(('dataset', params['dataset']))  # noqa: E501
            collection_formats['dataset'] = 'multi'  # noqa: E501
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
            '/balancing/dynamic/all', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='InsightsApiModelsResponsesResponseWithMetadata1InsightsApiModelsResponsesBalancingDynamicDynamicData',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def balancing_dynamic_get(self, bm_unit, snapshot_at, **kwargs):  # noqa: E501
        """Dynamic data per BMU (SEL, SIL, MZT, MNZT, MDV, MDP, NTB, NTO, NDZ)  # noqa: E501

        This endpoint provides the dynamic data for a requested BMU, excluding physical rate data.  It returns a \"snapshot\" of data valid at a given time, and optionally a time series of changes over a requested interval.                By default, all of the relevant datasets are returned: SIL, SEL, NDZ, NTB, NTO, MZT, MNZT, MDV, MDP.  The results from each dataset are transformed to a common response model, with the common integer field *Value*  mapped from the fields *Level*, *Period*, *Volume* or *Notice* in the original dataset, as relevant.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.balancing_dynamic_get(bm_unit, snapshot_at, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str bm_unit: The BM Unit to query. (required)
        :param datetime snapshot_at: When to retrieve a snapshot of data at.  That is, the latest datapoint before this time will be returned for each dataset. (required)
        :param datetime until: When to retrieve data until.  Data from the snapshot until this time will be returned.
        :param int snapshot_at_settlement_period: The settlement period to retrieve a snapshot of data at.  If provided, the time part of SnapshotAt will be ignored.
        :param int until_settlement_period: The settlement period to retrieve data until.  If provided, the time part of Until will be ignored.
        :param list[str] dataset: Datasets to filter. If omitted, all datasets will be returned.
        :param str format: Response data format. Use json/xml to include metadata.
        :return: InsightsApiModelsResponsesResponseWithMetadata1InsightsApiModelsResponsesBalancingDynamicDynamicData
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.balancing_dynamic_get_with_http_info(bm_unit, snapshot_at, **kwargs)  # noqa: E501
        else:
            (data) = self.balancing_dynamic_get_with_http_info(bm_unit, snapshot_at, **kwargs)  # noqa: E501
            return data

    def balancing_dynamic_get_with_http_info(self, bm_unit, snapshot_at, **kwargs):  # noqa: E501
        """Dynamic data per BMU (SEL, SIL, MZT, MNZT, MDV, MDP, NTB, NTO, NDZ)  # noqa: E501

        This endpoint provides the dynamic data for a requested BMU, excluding physical rate data.  It returns a \"snapshot\" of data valid at a given time, and optionally a time series of changes over a requested interval.                By default, all of the relevant datasets are returned: SIL, SEL, NDZ, NTB, NTO, MZT, MNZT, MDV, MDP.  The results from each dataset are transformed to a common response model, with the common integer field *Value*  mapped from the fields *Level*, *Period*, *Volume* or *Notice* in the original dataset, as relevant.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.balancing_dynamic_get_with_http_info(bm_unit, snapshot_at, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str bm_unit: The BM Unit to query. (required)
        :param datetime snapshot_at: When to retrieve a snapshot of data at.  That is, the latest datapoint before this time will be returned for each dataset. (required)
        :param datetime until: When to retrieve data until.  Data from the snapshot until this time will be returned.
        :param int snapshot_at_settlement_period: The settlement period to retrieve a snapshot of data at.  If provided, the time part of SnapshotAt will be ignored.
        :param int until_settlement_period: The settlement period to retrieve data until.  If provided, the time part of Until will be ignored.
        :param list[str] dataset: Datasets to filter. If omitted, all datasets will be returned.
        :param str format: Response data format. Use json/xml to include metadata.
        :return: InsightsApiModelsResponsesResponseWithMetadata1InsightsApiModelsResponsesBalancingDynamicDynamicData
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['bm_unit', 'snapshot_at', 'until', 'snapshot_at_settlement_period', 'until_settlement_period', 'dataset', 'format']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method balancing_dynamic_get" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'bm_unit' is set
        if ('bm_unit' not in params or
                params['bm_unit'] is None):
            raise ValueError("Missing the required parameter `bm_unit` when calling `balancing_dynamic_get`")  # noqa: E501
        # verify the required parameter 'snapshot_at' is set
        if ('snapshot_at' not in params or
                params['snapshot_at'] is None):
            raise ValueError("Missing the required parameter `snapshot_at` when calling `balancing_dynamic_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'bm_unit' in params:
            query_params.append(('bmUnit', params['bm_unit']))  # noqa: E501
        if 'snapshot_at' in params:
            query_params.append(('snapshotAt', params['snapshot_at']))  # noqa: E501
        if 'until' in params:
            query_params.append(('until', params['until']))  # noqa: E501
        if 'snapshot_at_settlement_period' in params:
            query_params.append(('snapshotAtSettlementPeriod', params['snapshot_at_settlement_period']))  # noqa: E501
        if 'until_settlement_period' in params:
            query_params.append(('untilSettlementPeriod', params['until_settlement_period']))  # noqa: E501
        if 'dataset' in params:
            query_params.append(('dataset', params['dataset']))  # noqa: E501
            collection_formats['dataset'] = 'multi'  # noqa: E501
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
            '/balancing/dynamic', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='InsightsApiModelsResponsesResponseWithMetadata1InsightsApiModelsResponsesBalancingDynamicDynamicData',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def balancing_dynamic_rates_all_get(self, settlement_date, settlement_period, **kwargs):  # noqa: E501
        """Market-wide rate data (RDRE, RURE, RDRI, RURI)  # noqa: E501

        This endpoint provides market-wide physical rate data, for all BMUs or a requested set of multiple BMUs.  It returns the data valid for a given settlement period. This includes a snapshot of data valid at the start  of the settlement period, and any changes published during that settlement period.                The settlement period to query can be specified as a date and settlement period. The settlement date must be provided in the format yyyy-MM-dd.    By default, all of the relevant datasets are returned: RDRE, RURE, RDRI, RURI.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.balancing_dynamic_rates_all_get(settlement_date, settlement_period, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param date settlement_date: The settlement date to filter. (required)
        :param int settlement_period: The settlement period to filter. This should be an integer from 1-50 inclusive. (required)
        :param list[str] bm_unit: The BM Units to query. Elexon or NGC BMU IDs can be used. If omitted, results for all BM units will be returned.
        :param list[str] dataset: Datasets to return. If omitted, all datasets will be returned.
        :param str format: Response data format. Use json/xml to include metadata.
        :return: InsightsApiModelsResponsesResponseWithMetadata1InsightsApiModelsResponsesBalancingDynamicRateData
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.balancing_dynamic_rates_all_get_with_http_info(settlement_date, settlement_period, **kwargs)  # noqa: E501
        else:
            (data) = self.balancing_dynamic_rates_all_get_with_http_info(settlement_date, settlement_period, **kwargs)  # noqa: E501
            return data

    def balancing_dynamic_rates_all_get_with_http_info(self, settlement_date, settlement_period, **kwargs):  # noqa: E501
        """Market-wide rate data (RDRE, RURE, RDRI, RURI)  # noqa: E501

        This endpoint provides market-wide physical rate data, for all BMUs or a requested set of multiple BMUs.  It returns the data valid for a given settlement period. This includes a snapshot of data valid at the start  of the settlement period, and any changes published during that settlement period.                The settlement period to query can be specified as a date and settlement period. The settlement date must be provided in the format yyyy-MM-dd.    By default, all of the relevant datasets are returned: RDRE, RURE, RDRI, RURI.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.balancing_dynamic_rates_all_get_with_http_info(settlement_date, settlement_period, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param date settlement_date: The settlement date to filter. (required)
        :param int settlement_period: The settlement period to filter. This should be an integer from 1-50 inclusive. (required)
        :param list[str] bm_unit: The BM Units to query. Elexon or NGC BMU IDs can be used. If omitted, results for all BM units will be returned.
        :param list[str] dataset: Datasets to return. If omitted, all datasets will be returned.
        :param str format: Response data format. Use json/xml to include metadata.
        :return: InsightsApiModelsResponsesResponseWithMetadata1InsightsApiModelsResponsesBalancingDynamicRateData
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['settlement_date', 'settlement_period', 'bm_unit', 'dataset', 'format']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method balancing_dynamic_rates_all_get" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'settlement_date' is set
        if ('settlement_date' not in params or
                params['settlement_date'] is None):
            raise ValueError("Missing the required parameter `settlement_date` when calling `balancing_dynamic_rates_all_get`")  # noqa: E501
        # verify the required parameter 'settlement_period' is set
        if ('settlement_period' not in params or
                params['settlement_period'] is None):
            raise ValueError("Missing the required parameter `settlement_period` when calling `balancing_dynamic_rates_all_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'settlement_date' in params:
            query_params.append(('settlementDate', params['settlement_date']))  # noqa: E501
        if 'settlement_period' in params:
            query_params.append(('settlementPeriod', params['settlement_period']))  # noqa: E501
        if 'bm_unit' in params:
            query_params.append(('bmUnit', params['bm_unit']))  # noqa: E501
            collection_formats['bmUnit'] = 'multi'  # noqa: E501
        if 'dataset' in params:
            query_params.append(('dataset', params['dataset']))  # noqa: E501
            collection_formats['dataset'] = 'multi'  # noqa: E501
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
            '/balancing/dynamic/rates/all', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='InsightsApiModelsResponsesResponseWithMetadata1InsightsApiModelsResponsesBalancingDynamicRateData',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def balancing_dynamic_rates_get(self, bm_unit, snapshot_at, **kwargs):  # noqa: E501
        """Rate data per BMU (RDRE, RURE, RDRI, RURI)  # noqa: E501

        This endpoint provides the physical rate data for a requested BMU.  It returns a \"snapshot\" of data valid at a given time, and optionally a time series of changes over a requested interval.                By default, all of the relevant datasets are returned: RDRE, RURE, RDRI, RURI.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.balancing_dynamic_rates_get(bm_unit, snapshot_at, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str bm_unit: The BM Unit to query. (required)
        :param datetime snapshot_at: When to retrieve a snapshot of data at.  That is, the latest datapoint before this time will be returned for each dataset. (required)
        :param datetime until: When to retrieve data until.  Data from the snapshot until this time will be returned.
        :param int snapshot_at_settlement_period: The settlement period to retrieve a snapshot of data at.  If provided, the time part of SnapshotAt will be ignored.
        :param int until_settlement_period: The settlement period to retrieve data until.  If provided, the time part of Until will be ignored.
        :param list[str] dataset: Datasets to filter. If empty, all datasets will be returned.
        :param str format: Response data format. Use json/xml to include metadata.
        :return: InsightsApiModelsResponsesResponseWithMetadata1InsightsApiModelsResponsesBalancingDynamicRateData
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.balancing_dynamic_rates_get_with_http_info(bm_unit, snapshot_at, **kwargs)  # noqa: E501
        else:
            (data) = self.balancing_dynamic_rates_get_with_http_info(bm_unit, snapshot_at, **kwargs)  # noqa: E501
            return data

    def balancing_dynamic_rates_get_with_http_info(self, bm_unit, snapshot_at, **kwargs):  # noqa: E501
        """Rate data per BMU (RDRE, RURE, RDRI, RURI)  # noqa: E501

        This endpoint provides the physical rate data for a requested BMU.  It returns a \"snapshot\" of data valid at a given time, and optionally a time series of changes over a requested interval.                By default, all of the relevant datasets are returned: RDRE, RURE, RDRI, RURI.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.balancing_dynamic_rates_get_with_http_info(bm_unit, snapshot_at, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str bm_unit: The BM Unit to query. (required)
        :param datetime snapshot_at: When to retrieve a snapshot of data at.  That is, the latest datapoint before this time will be returned for each dataset. (required)
        :param datetime until: When to retrieve data until.  Data from the snapshot until this time will be returned.
        :param int snapshot_at_settlement_period: The settlement period to retrieve a snapshot of data at.  If provided, the time part of SnapshotAt will be ignored.
        :param int until_settlement_period: The settlement period to retrieve data until.  If provided, the time part of Until will be ignored.
        :param list[str] dataset: Datasets to filter. If empty, all datasets will be returned.
        :param str format: Response data format. Use json/xml to include metadata.
        :return: InsightsApiModelsResponsesResponseWithMetadata1InsightsApiModelsResponsesBalancingDynamicRateData
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['bm_unit', 'snapshot_at', 'until', 'snapshot_at_settlement_period', 'until_settlement_period', 'dataset', 'format']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method balancing_dynamic_rates_get" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'bm_unit' is set
        if ('bm_unit' not in params or
                params['bm_unit'] is None):
            raise ValueError("Missing the required parameter `bm_unit` when calling `balancing_dynamic_rates_get`")  # noqa: E501
        # verify the required parameter 'snapshot_at' is set
        if ('snapshot_at' not in params or
                params['snapshot_at'] is None):
            raise ValueError("Missing the required parameter `snapshot_at` when calling `balancing_dynamic_rates_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'bm_unit' in params:
            query_params.append(('bmUnit', params['bm_unit']))  # noqa: E501
        if 'snapshot_at' in params:
            query_params.append(('snapshotAt', params['snapshot_at']))  # noqa: E501
        if 'until' in params:
            query_params.append(('until', params['until']))  # noqa: E501
        if 'snapshot_at_settlement_period' in params:
            query_params.append(('snapshotAtSettlementPeriod', params['snapshot_at_settlement_period']))  # noqa: E501
        if 'until_settlement_period' in params:
            query_params.append(('untilSettlementPeriod', params['until_settlement_period']))  # noqa: E501
        if 'dataset' in params:
            query_params.append(('dataset', params['dataset']))  # noqa: E501
            collection_formats['dataset'] = 'multi'  # noqa: E501
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
            '/balancing/dynamic/rates', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='InsightsApiModelsResponsesResponseWithMetadata1InsightsApiModelsResponsesBalancingDynamicRateData',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
