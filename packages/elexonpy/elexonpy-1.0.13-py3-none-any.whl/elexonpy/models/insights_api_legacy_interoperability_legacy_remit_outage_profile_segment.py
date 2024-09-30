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

class InsightsApiLegacyInteroperabilityLegacyRemitOutageProfileSegment(object):
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
        'segment_start_string': 'str',
        'segment_end_string': 'str',
        'segment_capacity': 'int'
    }

    attribute_map = {
        'segment_start_string': 'segmentStartString',
        'segment_end_string': 'segmentEndString',
        'segment_capacity': 'segmentCapacity'
    }

    def __init__(self, segment_start_string=None, segment_end_string=None, segment_capacity=None):  # noqa: E501
        """InsightsApiLegacyInteroperabilityLegacyRemitOutageProfileSegment - a model defined in Swagger"""  # noqa: E501
        self._segment_start_string = None
        self._segment_end_string = None
        self._segment_capacity = None
        self.discriminator = None
        if segment_start_string is not None:
            self.segment_start_string = segment_start_string
        if segment_end_string is not None:
            self.segment_end_string = segment_end_string
        if segment_capacity is not None:
            self.segment_capacity = segment_capacity

    @property
    def segment_start_string(self):
        """Gets the segment_start_string of this InsightsApiLegacyInteroperabilityLegacyRemitOutageProfileSegment.  # noqa: E501


        :return: The segment_start_string of this InsightsApiLegacyInteroperabilityLegacyRemitOutageProfileSegment.  # noqa: E501
        :rtype: str
        """
        return self._segment_start_string

    @segment_start_string.setter
    def segment_start_string(self, segment_start_string):
        """Sets the segment_start_string of this InsightsApiLegacyInteroperabilityLegacyRemitOutageProfileSegment.


        :param segment_start_string: The segment_start_string of this InsightsApiLegacyInteroperabilityLegacyRemitOutageProfileSegment.  # noqa: E501
        :type: str
        """

        self._segment_start_string = segment_start_string

    @property
    def segment_end_string(self):
        """Gets the segment_end_string of this InsightsApiLegacyInteroperabilityLegacyRemitOutageProfileSegment.  # noqa: E501


        :return: The segment_end_string of this InsightsApiLegacyInteroperabilityLegacyRemitOutageProfileSegment.  # noqa: E501
        :rtype: str
        """
        return self._segment_end_string

    @segment_end_string.setter
    def segment_end_string(self, segment_end_string):
        """Sets the segment_end_string of this InsightsApiLegacyInteroperabilityLegacyRemitOutageProfileSegment.


        :param segment_end_string: The segment_end_string of this InsightsApiLegacyInteroperabilityLegacyRemitOutageProfileSegment.  # noqa: E501
        :type: str
        """

        self._segment_end_string = segment_end_string

    @property
    def segment_capacity(self):
        """Gets the segment_capacity of this InsightsApiLegacyInteroperabilityLegacyRemitOutageProfileSegment.  # noqa: E501


        :return: The segment_capacity of this InsightsApiLegacyInteroperabilityLegacyRemitOutageProfileSegment.  # noqa: E501
        :rtype: int
        """
        return self._segment_capacity

    @segment_capacity.setter
    def segment_capacity(self, segment_capacity):
        """Sets the segment_capacity of this InsightsApiLegacyInteroperabilityLegacyRemitOutageProfileSegment.


        :param segment_capacity: The segment_capacity of this InsightsApiLegacyInteroperabilityLegacyRemitOutageProfileSegment.  # noqa: E501
        :type: int
        """

        self._segment_capacity = segment_capacity

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
        if issubclass(InsightsApiLegacyInteroperabilityLegacyRemitOutageProfileSegment, dict):
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
        if not isinstance(other, InsightsApiLegacyInteroperabilityLegacyRemitOutageProfileSegment):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
