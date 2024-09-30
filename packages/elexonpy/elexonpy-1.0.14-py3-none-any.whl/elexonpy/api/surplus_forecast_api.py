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


class SurplusForecastApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def forecast_surplus_daily_evolution_get(self, forecast_date, **kwargs):  # noqa: E501
        """Evolution daily surplus forecast (OCNMFD)  # noqa: E501

        This endpoint provides the daily evolution Generating Plant Operating Surplus covering 2 days ahead to 14 days ahead in MW values.  The Daily API outputs the latest published data for daily surplus forecast for D+2 to D+14.                Date parameter must be provided in the exact format yyyy-MM-dd.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.forecast_surplus_daily_evolution_get(forecast_date, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param date forecast_date: The forecast date for the filter. This must be in the format yyyy-MM-dd. (required)
        :param str format: Response data format. Use json/xml to include metadata.
        :return: InsightsApiModelsResponsesResponseWithMetadata1InsightsApiModelsResponsesForecastSurplusForecastSurplusDaily
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.forecast_surplus_daily_evolution_get_with_http_info(forecast_date, **kwargs)  # noqa: E501
        else:
            (data) = self.forecast_surplus_daily_evolution_get_with_http_info(forecast_date, **kwargs)  # noqa: E501
            return data

    def forecast_surplus_daily_evolution_get_with_http_info(self, forecast_date, **kwargs):  # noqa: E501
        """Evolution daily surplus forecast (OCNMFD)  # noqa: E501

        This endpoint provides the daily evolution Generating Plant Operating Surplus covering 2 days ahead to 14 days ahead in MW values.  The Daily API outputs the latest published data for daily surplus forecast for D+2 to D+14.                Date parameter must be provided in the exact format yyyy-MM-dd.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.forecast_surplus_daily_evolution_get_with_http_info(forecast_date, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param date forecast_date: The forecast date for the filter. This must be in the format yyyy-MM-dd. (required)
        :param str format: Response data format. Use json/xml to include metadata.
        :return: InsightsApiModelsResponsesResponseWithMetadata1InsightsApiModelsResponsesForecastSurplusForecastSurplusDaily
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['forecast_date', 'format']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method forecast_surplus_daily_evolution_get" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'forecast_date' is set
        if ('forecast_date' not in params or
                params['forecast_date'] is None):
            raise ValueError("Missing the required parameter `forecast_date` when calling `forecast_surplus_daily_evolution_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'forecast_date' in params:
            query_params.append(('forecastDate', params['forecast_date']))  # noqa: E501
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
            '/forecast/surplus/daily/evolution', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='InsightsApiModelsResponsesResponseWithMetadata1InsightsApiModelsResponsesForecastSurplusForecastSurplusDaily',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def forecast_surplus_daily_get(self, **kwargs):  # noqa: E501
        """Daily surplus forecast (OCNMFD)  # noqa: E501

        This endpoint provides the Generating Plant Operating Surplus covering 2 days ahead to 14 days ahead in MW values.  The Daily API outputs the latest published data for daily surplus forecast for D+2 t D+14  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.forecast_surplus_daily_get(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str format: Response data format. Use json/xml to include metadata.
        :return: InsightsApiModelsResponsesResponseWithMetadata1InsightsApiModelsResponsesForecastSurplusForecastSurplusDaily
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.forecast_surplus_daily_get_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.forecast_surplus_daily_get_with_http_info(**kwargs)  # noqa: E501
            return data

    def forecast_surplus_daily_get_with_http_info(self, **kwargs):  # noqa: E501
        """Daily surplus forecast (OCNMFD)  # noqa: E501

        This endpoint provides the Generating Plant Operating Surplus covering 2 days ahead to 14 days ahead in MW values.  The Daily API outputs the latest published data for daily surplus forecast for D+2 t D+14  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.forecast_surplus_daily_get_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str format: Response data format. Use json/xml to include metadata.
        :return: InsightsApiModelsResponsesResponseWithMetadata1InsightsApiModelsResponsesForecastSurplusForecastSurplusDaily
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['format']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method forecast_surplus_daily_get" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
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
            '/forecast/surplus/daily', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='InsightsApiModelsResponsesResponseWithMetadata1InsightsApiModelsResponsesForecastSurplusForecastSurplusDaily',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def forecast_surplus_daily_history_get(self, publish_time, **kwargs):  # noqa: E501
        """Historical daily surplus forecast (OCNMFD)  # noqa: E501

        This endpoint provides the historic Generating Plant Operating Surplus covering 2 days ahead to 14 days ahead in MW values.  The historic API outputs the latest published data for historic daily surplus forecast for D+2 to D+14  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.forecast_surplus_daily_history_get(publish_time, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param datetime publish_time: (required)
        :param str format: Response data format. Use json/xml to include metadata.
        :return: InsightsApiModelsResponsesResponseWithMetadata1InsightsApiModelsResponsesForecastSurplusForecastSurplusDaily
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.forecast_surplus_daily_history_get_with_http_info(publish_time, **kwargs)  # noqa: E501
        else:
            (data) = self.forecast_surplus_daily_history_get_with_http_info(publish_time, **kwargs)  # noqa: E501
            return data

    def forecast_surplus_daily_history_get_with_http_info(self, publish_time, **kwargs):  # noqa: E501
        """Historical daily surplus forecast (OCNMFD)  # noqa: E501

        This endpoint provides the historic Generating Plant Operating Surplus covering 2 days ahead to 14 days ahead in MW values.  The historic API outputs the latest published data for historic daily surplus forecast for D+2 to D+14  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.forecast_surplus_daily_history_get_with_http_info(publish_time, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param datetime publish_time: (required)
        :param str format: Response data format. Use json/xml to include metadata.
        :return: InsightsApiModelsResponsesResponseWithMetadata1InsightsApiModelsResponsesForecastSurplusForecastSurplusDaily
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['publish_time', 'format']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method forecast_surplus_daily_history_get" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'publish_time' is set
        if ('publish_time' not in params or
                params['publish_time'] is None):
            raise ValueError("Missing the required parameter `publish_time` when calling `forecast_surplus_daily_history_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'publish_time' in params:
            query_params.append(('publishTime', params['publish_time']))  # noqa: E501
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
            '/forecast/surplus/daily/history', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='InsightsApiModelsResponsesResponseWithMetadata1InsightsApiModelsResponsesForecastSurplusForecastSurplusDaily',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def forecast_surplus_weekly_evolution_get(self, year, week, **kwargs):  # noqa: E501
        """Evolution weekly surplus forecast (OCNMFW, OCNMF3Y)  # noqa: E501

        This endpoint provides the evolution Generating Plant Operating Surplus  covering 2 weeks ahead to 156 weeks ahead in MW values.  The weekly API outputs the latest published data for weekly surplus forecast for W+2 to W+156  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.forecast_surplus_weekly_evolution_get(year, week, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int year: (required)
        :param int week: (required)
        :param str range:
        :param str format: Response data format. Use json/xml to include metadata.
        :return: InsightsApiModelsResponsesResponseWithMetadata1InsightsApiModelsResponsesForecastSurplusForecastSurplusWeekly
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.forecast_surplus_weekly_evolution_get_with_http_info(year, week, **kwargs)  # noqa: E501
        else:
            (data) = self.forecast_surplus_weekly_evolution_get_with_http_info(year, week, **kwargs)  # noqa: E501
            return data

    def forecast_surplus_weekly_evolution_get_with_http_info(self, year, week, **kwargs):  # noqa: E501
        """Evolution weekly surplus forecast (OCNMFW, OCNMF3Y)  # noqa: E501

        This endpoint provides the evolution Generating Plant Operating Surplus  covering 2 weeks ahead to 156 weeks ahead in MW values.  The weekly API outputs the latest published data for weekly surplus forecast for W+2 to W+156  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.forecast_surplus_weekly_evolution_get_with_http_info(year, week, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int year: (required)
        :param int week: (required)
        :param str range:
        :param str format: Response data format. Use json/xml to include metadata.
        :return: InsightsApiModelsResponsesResponseWithMetadata1InsightsApiModelsResponsesForecastSurplusForecastSurplusWeekly
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['year', 'week', 'range', 'format']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method forecast_surplus_weekly_evolution_get" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'year' is set
        if ('year' not in params or
                params['year'] is None):
            raise ValueError("Missing the required parameter `year` when calling `forecast_surplus_weekly_evolution_get`")  # noqa: E501
        # verify the required parameter 'week' is set
        if ('week' not in params or
                params['week'] is None):
            raise ValueError("Missing the required parameter `week` when calling `forecast_surplus_weekly_evolution_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'year' in params:
            query_params.append(('year', params['year']))  # noqa: E501
        if 'week' in params:
            query_params.append(('week', params['week']))  # noqa: E501
        if 'range' in params:
            query_params.append(('range', params['range']))  # noqa: E501
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
            '/forecast/surplus/weekly/evolution', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='InsightsApiModelsResponsesResponseWithMetadata1InsightsApiModelsResponsesForecastSurplusForecastSurplusWeekly',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def forecast_surplus_weekly_get(self, **kwargs):  # noqa: E501
        """Weekly surplus forecast (OCNMFW, OCNMF3Y)  # noqa: E501

        This endpoint provides the Generating Plant Operating Surplus covering 2 weeks ahead to 156 weeks ahead in MW values.  The weekly API outputs the latest published data for weekly surplus forecast for W+2 to W+156  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.forecast_surplus_weekly_get(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str range:
        :param str format: Response data format. Use json/xml to include metadata.
        :return: InsightsApiModelsResponsesResponseWithMetadata1InsightsApiModelsResponsesForecastSurplusForecastSurplusWeekly
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.forecast_surplus_weekly_get_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.forecast_surplus_weekly_get_with_http_info(**kwargs)  # noqa: E501
            return data

    def forecast_surplus_weekly_get_with_http_info(self, **kwargs):  # noqa: E501
        """Weekly surplus forecast (OCNMFW, OCNMF3Y)  # noqa: E501

        This endpoint provides the Generating Plant Operating Surplus covering 2 weeks ahead to 156 weeks ahead in MW values.  The weekly API outputs the latest published data for weekly surplus forecast for W+2 to W+156  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.forecast_surplus_weekly_get_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str range:
        :param str format: Response data format. Use json/xml to include metadata.
        :return: InsightsApiModelsResponsesResponseWithMetadata1InsightsApiModelsResponsesForecastSurplusForecastSurplusWeekly
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['range', 'format']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method forecast_surplus_weekly_get" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'range' in params:
            query_params.append(('range', params['range']))  # noqa: E501
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
            '/forecast/surplus/weekly', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='InsightsApiModelsResponsesResponseWithMetadata1InsightsApiModelsResponsesForecastSurplusForecastSurplusWeekly',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def forecast_surplus_weekly_history_get(self, publish_time, **kwargs):  # noqa: E501
        """Historical weekly surplus forecast (OCNMFW, OCNMF3Y)  # noqa: E501

        This endpoint provides the historic Generating Plant Operating Surplus covering 2 weeks ahead to 156 weeks ahead in MW values.  The weekly API outputs the latest published data for weekly surplus forecast for W+2 to W+156.  Historical published data of weekly surplus forecasts for a given publish date in the 2-156 week dataset.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.forecast_surplus_weekly_history_get(publish_time, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param datetime publish_time: (required)
        :param str range:
        :param str format: Response data format. Use json/xml to include metadata.
        :return: InsightsApiModelsResponsesResponseWithMetadata1InsightsApiModelsResponsesForecastSurplusForecastSurplusWeekly
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.forecast_surplus_weekly_history_get_with_http_info(publish_time, **kwargs)  # noqa: E501
        else:
            (data) = self.forecast_surplus_weekly_history_get_with_http_info(publish_time, **kwargs)  # noqa: E501
            return data

    def forecast_surplus_weekly_history_get_with_http_info(self, publish_time, **kwargs):  # noqa: E501
        """Historical weekly surplus forecast (OCNMFW, OCNMF3Y)  # noqa: E501

        This endpoint provides the historic Generating Plant Operating Surplus covering 2 weeks ahead to 156 weeks ahead in MW values.  The weekly API outputs the latest published data for weekly surplus forecast for W+2 to W+156.  Historical published data of weekly surplus forecasts for a given publish date in the 2-156 week dataset.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.forecast_surplus_weekly_history_get_with_http_info(publish_time, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param datetime publish_time: (required)
        :param str range:
        :param str format: Response data format. Use json/xml to include metadata.
        :return: InsightsApiModelsResponsesResponseWithMetadata1InsightsApiModelsResponsesForecastSurplusForecastSurplusWeekly
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['publish_time', 'range', 'format']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method forecast_surplus_weekly_history_get" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'publish_time' is set
        if ('publish_time' not in params or
                params['publish_time'] is None):
            raise ValueError("Missing the required parameter `publish_time` when calling `forecast_surplus_weekly_history_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'publish_time' in params:
            query_params.append(('publishTime', params['publish_time']))  # noqa: E501
        if 'range' in params:
            query_params.append(('range', params['range']))  # noqa: E501
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
            '/forecast/surplus/weekly/history', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='InsightsApiModelsResponsesResponseWithMetadata1InsightsApiModelsResponsesForecastSurplusForecastSurplusWeekly',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
