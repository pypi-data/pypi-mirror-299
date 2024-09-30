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

class InsightsApiModelsResponsesBalancingSettlementSettlementSummaryPrice(object):
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
        'cost': 'float',
        'volume': 'float',
        'value': 'float'
    }

    attribute_map = {
        'cost': 'cost',
        'volume': 'volume',
        'value': 'value'
    }

    def __init__(self, cost=None, volume=None, value=None):  # noqa: E501
        """InsightsApiModelsResponsesBalancingSettlementSettlementSummaryPrice - a model defined in Swagger"""  # noqa: E501
        self._cost = None
        self._volume = None
        self._value = None
        self.discriminator = None
        if cost is not None:
            self.cost = cost
        if volume is not None:
            self.volume = volume
        if value is not None:
            self.value = value

    @property
    def cost(self):
        """Gets the cost of this InsightsApiModelsResponsesBalancingSettlementSettlementSummaryPrice.  # noqa: E501


        :return: The cost of this InsightsApiModelsResponsesBalancingSettlementSettlementSummaryPrice.  # noqa: E501
        :rtype: float
        """
        return self._cost

    @cost.setter
    def cost(self, cost):
        """Sets the cost of this InsightsApiModelsResponsesBalancingSettlementSettlementSummaryPrice.


        :param cost: The cost of this InsightsApiModelsResponsesBalancingSettlementSettlementSummaryPrice.  # noqa: E501
        :type: float
        """

        self._cost = cost

    @property
    def volume(self):
        """Gets the volume of this InsightsApiModelsResponsesBalancingSettlementSettlementSummaryPrice.  # noqa: E501


        :return: The volume of this InsightsApiModelsResponsesBalancingSettlementSettlementSummaryPrice.  # noqa: E501
        :rtype: float
        """
        return self._volume

    @volume.setter
    def volume(self, volume):
        """Sets the volume of this InsightsApiModelsResponsesBalancingSettlementSettlementSummaryPrice.


        :param volume: The volume of this InsightsApiModelsResponsesBalancingSettlementSettlementSummaryPrice.  # noqa: E501
        :type: float
        """

        self._volume = volume

    @property
    def value(self):
        """Gets the value of this InsightsApiModelsResponsesBalancingSettlementSettlementSummaryPrice.  # noqa: E501


        :return: The value of this InsightsApiModelsResponsesBalancingSettlementSettlementSummaryPrice.  # noqa: E501
        :rtype: float
        """
        return self._value

    @value.setter
    def value(self, value):
        """Sets the value of this InsightsApiModelsResponsesBalancingSettlementSettlementSummaryPrice.


        :param value: The value of this InsightsApiModelsResponsesBalancingSettlementSettlementSummaryPrice.  # noqa: E501
        :type: float
        """

        self._value = value

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
        if issubclass(InsightsApiModelsResponsesBalancingSettlementSettlementSummaryPrice, dict):
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
        if not isinstance(other, InsightsApiModelsResponsesBalancingSettlementSettlementSummaryPrice):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
