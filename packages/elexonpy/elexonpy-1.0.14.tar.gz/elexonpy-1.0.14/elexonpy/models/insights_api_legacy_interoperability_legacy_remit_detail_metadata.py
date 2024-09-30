# coding: utf-8

"""
    Insights.Api

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: 1.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class InsightsApiLegacyInteroperabilityLegacyRemitDetailMetadata(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'http_code': 'int',
        'error_type': 'str',
        'description': 'str',
        'query_string': 'str'
    }

    attribute_map = {
        'http_code': 'httpCode',
        'error_type': 'errorType',
        'description': 'description',
        'query_string': 'queryString'
    }

    def __init__(self, http_code=None, error_type=None, description=None, query_string=None):  # noqa: E501
        """InsightsApiLegacyInteroperabilityLegacyRemitDetailMetadata - a model defined in Swagger"""  # noqa: E501
        self._http_code = None
        self._error_type = None
        self._description = None
        self._query_string = None
        self.discriminator = None
        if http_code is not None:
            self.http_code = http_code
        if error_type is not None:
            self.error_type = error_type
        if description is not None:
            self.description = description
        if query_string is not None:
            self.query_string = query_string

    @property
    def http_code(self):
        """Gets the http_code of this InsightsApiLegacyInteroperabilityLegacyRemitDetailMetadata.  # noqa: E501


        :return: The http_code of this InsightsApiLegacyInteroperabilityLegacyRemitDetailMetadata.  # noqa: E501
        :rtype: int
        """
        return self._http_code

    @http_code.setter
    def http_code(self, http_code):
        """Sets the http_code of this InsightsApiLegacyInteroperabilityLegacyRemitDetailMetadata.


        :param http_code: The http_code of this InsightsApiLegacyInteroperabilityLegacyRemitDetailMetadata.  # noqa: E501
        :type: int
        """

        self._http_code = http_code

    @property
    def error_type(self):
        """Gets the error_type of this InsightsApiLegacyInteroperabilityLegacyRemitDetailMetadata.  # noqa: E501


        :return: The error_type of this InsightsApiLegacyInteroperabilityLegacyRemitDetailMetadata.  # noqa: E501
        :rtype: str
        """
        return self._error_type

    @error_type.setter
    def error_type(self, error_type):
        """Sets the error_type of this InsightsApiLegacyInteroperabilityLegacyRemitDetailMetadata.


        :param error_type: The error_type of this InsightsApiLegacyInteroperabilityLegacyRemitDetailMetadata.  # noqa: E501
        :type: str
        """

        self._error_type = error_type

    @property
    def description(self):
        """Gets the description of this InsightsApiLegacyInteroperabilityLegacyRemitDetailMetadata.  # noqa: E501


        :return: The description of this InsightsApiLegacyInteroperabilityLegacyRemitDetailMetadata.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this InsightsApiLegacyInteroperabilityLegacyRemitDetailMetadata.


        :param description: The description of this InsightsApiLegacyInteroperabilityLegacyRemitDetailMetadata.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def query_string(self):
        """Gets the query_string of this InsightsApiLegacyInteroperabilityLegacyRemitDetailMetadata.  # noqa: E501


        :return: The query_string of this InsightsApiLegacyInteroperabilityLegacyRemitDetailMetadata.  # noqa: E501
        :rtype: str
        """
        return self._query_string

    @query_string.setter
    def query_string(self, query_string):
        """Sets the query_string of this InsightsApiLegacyInteroperabilityLegacyRemitDetailMetadata.


        :param query_string: The query_string of this InsightsApiLegacyInteroperabilityLegacyRemitDetailMetadata.  # noqa: E501
        :type: str
        """

        self._query_string = query_string

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(InsightsApiLegacyInteroperabilityLegacyRemitDetailMetadata, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, InsightsApiLegacyInteroperabilityLegacyRemitDetailMetadata):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
