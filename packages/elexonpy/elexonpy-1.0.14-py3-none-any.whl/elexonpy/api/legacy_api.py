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


class LegacyApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def interop_message_detail_retrieval_get(self, message_id, **kwargs):  # noqa: E501
        """This endpoint is obsolete, and this location may be removed with no further notice. Use /remit/* or /datasets/REMIT endpoints instead.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.interop_message_detail_retrieval_get(message_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str message_id: (required)
        :return: InsightsApiLegacyInteroperabilityLegacyRemitDetailResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.interop_message_detail_retrieval_get_with_http_info(message_id, **kwargs)  # noqa: E501
        else:
            (data) = self.interop_message_detail_retrieval_get_with_http_info(message_id, **kwargs)  # noqa: E501
            return data

    def interop_message_detail_retrieval_get_with_http_info(self, message_id, **kwargs):  # noqa: E501
        """This endpoint is obsolete, and this location may be removed with no further notice. Use /remit/* or /datasets/REMIT endpoints instead.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.interop_message_detail_retrieval_get_with_http_info(message_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str message_id: (required)
        :return: InsightsApiLegacyInteroperabilityLegacyRemitDetailResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['message_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method interop_message_detail_retrieval_get" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'message_id' is set
        if ('message_id' not in params or
                params['message_id'] is None):
            raise ValueError("Missing the required parameter `message_id` when calling `interop_message_detail_retrieval_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'message_id' in params:
            query_params.append(('messageId', params['message_id']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/xml'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/interop/MessageDetailRetrieval', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='InsightsApiLegacyInteroperabilityLegacyRemitDetailResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def interop_message_list_retrieval_get(self, event_start, event_end, **kwargs):  # noqa: E501
        """This endpoint is obsolete, and this location may be removed with no further notice. Use /remit/* or /datasets/REMIT endpoints instead.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.interop_message_list_retrieval_get(event_start, event_end, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param datetime event_start: (required)
        :param datetime event_end: (required)
        :return: InsightsApiLegacyInteroperabilityLegacyRemitListResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.interop_message_list_retrieval_get_with_http_info(event_start, event_end, **kwargs)  # noqa: E501
        else:
            (data) = self.interop_message_list_retrieval_get_with_http_info(event_start, event_end, **kwargs)  # noqa: E501
            return data

    def interop_message_list_retrieval_get_with_http_info(self, event_start, event_end, **kwargs):  # noqa: E501
        """This endpoint is obsolete, and this location may be removed with no further notice. Use /remit/* or /datasets/REMIT endpoints instead.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.interop_message_list_retrieval_get_with_http_info(event_start, event_end, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param datetime event_start: (required)
        :param datetime event_end: (required)
        :return: InsightsApiLegacyInteroperabilityLegacyRemitListResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['event_start', 'event_end']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method interop_message_list_retrieval_get" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'event_start' is set
        if ('event_start' not in params or
                params['event_start'] is None):
            raise ValueError("Missing the required parameter `event_start` when calling `interop_message_list_retrieval_get`")  # noqa: E501
        # verify the required parameter 'event_end' is set
        if ('event_end' not in params or
                params['event_end'] is None):
            raise ValueError("Missing the required parameter `event_end` when calling `interop_message_list_retrieval_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'event_start' in params:
            query_params.append(('eventStart', params['event_start']))  # noqa: E501
        if 'event_end' in params:
            query_params.append(('eventEnd', params['event_end']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/xml'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/interop/MessageListRetrieval', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='InsightsApiLegacyInteroperabilityLegacyRemitListResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
