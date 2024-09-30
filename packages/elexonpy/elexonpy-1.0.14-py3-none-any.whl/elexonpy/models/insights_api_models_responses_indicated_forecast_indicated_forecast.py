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

class InsightsApiModelsResponsesIndicatedForecastIndicatedForecast(object):
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
        'publish_time': 'datetime',
        'start_time': 'datetime',
        'settlement_date': 'date',
        'settlement_period': 'int',
        'boundary': 'str',
        'indicated_generation': 'int',
        'indicated_demand': 'int',
        'indicated_margin': 'int',
        'indicated_imbalance': 'int'
    }

    attribute_map = {
        'publish_time': 'publishTime',
        'start_time': 'startTime',
        'settlement_date': 'settlementDate',
        'settlement_period': 'settlementPeriod',
        'boundary': 'boundary',
        'indicated_generation': 'indicatedGeneration',
        'indicated_demand': 'indicatedDemand',
        'indicated_margin': 'indicatedMargin',
        'indicated_imbalance': 'indicatedImbalance'
    }

    def __init__(self, publish_time=None, start_time=None, settlement_date=None, settlement_period=None, boundary=None, indicated_generation=None, indicated_demand=None, indicated_margin=None, indicated_imbalance=None):  # noqa: E501
        """InsightsApiModelsResponsesIndicatedForecastIndicatedForecast - a model defined in Swagger"""  # noqa: E501
        self._publish_time = None
        self._start_time = None
        self._settlement_date = None
        self._settlement_period = None
        self._boundary = None
        self._indicated_generation = None
        self._indicated_demand = None
        self._indicated_margin = None
        self._indicated_imbalance = None
        self.discriminator = None
        if publish_time is not None:
            self.publish_time = publish_time
        if start_time is not None:
            self.start_time = start_time
        if settlement_date is not None:
            self.settlement_date = settlement_date
        if settlement_period is not None:
            self.settlement_period = settlement_period
        if boundary is not None:
            self.boundary = boundary
        if indicated_generation is not None:
            self.indicated_generation = indicated_generation
        if indicated_demand is not None:
            self.indicated_demand = indicated_demand
        if indicated_margin is not None:
            self.indicated_margin = indicated_margin
        if indicated_imbalance is not None:
            self.indicated_imbalance = indicated_imbalance

    @property
    def publish_time(self):
        """Gets the publish_time of this InsightsApiModelsResponsesIndicatedForecastIndicatedForecast.  # noqa: E501


        :return: The publish_time of this InsightsApiModelsResponsesIndicatedForecastIndicatedForecast.  # noqa: E501
        :rtype: datetime
        """
        return self._publish_time

    @publish_time.setter
    def publish_time(self, publish_time):
        """Sets the publish_time of this InsightsApiModelsResponsesIndicatedForecastIndicatedForecast.


        :param publish_time: The publish_time of this InsightsApiModelsResponsesIndicatedForecastIndicatedForecast.  # noqa: E501
        :type: datetime
        """

        self._publish_time = publish_time

    @property
    def start_time(self):
        """Gets the start_time of this InsightsApiModelsResponsesIndicatedForecastIndicatedForecast.  # noqa: E501


        :return: The start_time of this InsightsApiModelsResponsesIndicatedForecastIndicatedForecast.  # noqa: E501
        :rtype: datetime
        """
        return self._start_time

    @start_time.setter
    def start_time(self, start_time):
        """Sets the start_time of this InsightsApiModelsResponsesIndicatedForecastIndicatedForecast.


        :param start_time: The start_time of this InsightsApiModelsResponsesIndicatedForecastIndicatedForecast.  # noqa: E501
        :type: datetime
        """

        self._start_time = start_time

    @property
    def settlement_date(self):
        """Gets the settlement_date of this InsightsApiModelsResponsesIndicatedForecastIndicatedForecast.  # noqa: E501


        :return: The settlement_date of this InsightsApiModelsResponsesIndicatedForecastIndicatedForecast.  # noqa: E501
        :rtype: date
        """
        return self._settlement_date

    @settlement_date.setter
    def settlement_date(self, settlement_date):
        """Sets the settlement_date of this InsightsApiModelsResponsesIndicatedForecastIndicatedForecast.


        :param settlement_date: The settlement_date of this InsightsApiModelsResponsesIndicatedForecastIndicatedForecast.  # noqa: E501
        :type: date
        """

        self._settlement_date = settlement_date

    @property
    def settlement_period(self):
        """Gets the settlement_period of this InsightsApiModelsResponsesIndicatedForecastIndicatedForecast.  # noqa: E501


        :return: The settlement_period of this InsightsApiModelsResponsesIndicatedForecastIndicatedForecast.  # noqa: E501
        :rtype: int
        """
        return self._settlement_period

    @settlement_period.setter
    def settlement_period(self, settlement_period):
        """Sets the settlement_period of this InsightsApiModelsResponsesIndicatedForecastIndicatedForecast.


        :param settlement_period: The settlement_period of this InsightsApiModelsResponsesIndicatedForecastIndicatedForecast.  # noqa: E501
        :type: int
        """

        self._settlement_period = settlement_period

    @property
    def boundary(self):
        """Gets the boundary of this InsightsApiModelsResponsesIndicatedForecastIndicatedForecast.  # noqa: E501


        :return: The boundary of this InsightsApiModelsResponsesIndicatedForecastIndicatedForecast.  # noqa: E501
        :rtype: str
        """
        return self._boundary

    @boundary.setter
    def boundary(self, boundary):
        """Sets the boundary of this InsightsApiModelsResponsesIndicatedForecastIndicatedForecast.


        :param boundary: The boundary of this InsightsApiModelsResponsesIndicatedForecastIndicatedForecast.  # noqa: E501
        :type: str
        """

        self._boundary = boundary

    @property
    def indicated_generation(self):
        """Gets the indicated_generation of this InsightsApiModelsResponsesIndicatedForecastIndicatedForecast.  # noqa: E501


        :return: The indicated_generation of this InsightsApiModelsResponsesIndicatedForecastIndicatedForecast.  # noqa: E501
        :rtype: int
        """
        return self._indicated_generation

    @indicated_generation.setter
    def indicated_generation(self, indicated_generation):
        """Sets the indicated_generation of this InsightsApiModelsResponsesIndicatedForecastIndicatedForecast.


        :param indicated_generation: The indicated_generation of this InsightsApiModelsResponsesIndicatedForecastIndicatedForecast.  # noqa: E501
        :type: int
        """

        self._indicated_generation = indicated_generation

    @property
    def indicated_demand(self):
        """Gets the indicated_demand of this InsightsApiModelsResponsesIndicatedForecastIndicatedForecast.  # noqa: E501


        :return: The indicated_demand of this InsightsApiModelsResponsesIndicatedForecastIndicatedForecast.  # noqa: E501
        :rtype: int
        """
        return self._indicated_demand

    @indicated_demand.setter
    def indicated_demand(self, indicated_demand):
        """Sets the indicated_demand of this InsightsApiModelsResponsesIndicatedForecastIndicatedForecast.


        :param indicated_demand: The indicated_demand of this InsightsApiModelsResponsesIndicatedForecastIndicatedForecast.  # noqa: E501
        :type: int
        """

        self._indicated_demand = indicated_demand

    @property
    def indicated_margin(self):
        """Gets the indicated_margin of this InsightsApiModelsResponsesIndicatedForecastIndicatedForecast.  # noqa: E501


        :return: The indicated_margin of this InsightsApiModelsResponsesIndicatedForecastIndicatedForecast.  # noqa: E501
        :rtype: int
        """
        return self._indicated_margin

    @indicated_margin.setter
    def indicated_margin(self, indicated_margin):
        """Sets the indicated_margin of this InsightsApiModelsResponsesIndicatedForecastIndicatedForecast.


        :param indicated_margin: The indicated_margin of this InsightsApiModelsResponsesIndicatedForecastIndicatedForecast.  # noqa: E501
        :type: int
        """

        self._indicated_margin = indicated_margin

    @property
    def indicated_imbalance(self):
        """Gets the indicated_imbalance of this InsightsApiModelsResponsesIndicatedForecastIndicatedForecast.  # noqa: E501


        :return: The indicated_imbalance of this InsightsApiModelsResponsesIndicatedForecastIndicatedForecast.  # noqa: E501
        :rtype: int
        """
        return self._indicated_imbalance

    @indicated_imbalance.setter
    def indicated_imbalance(self, indicated_imbalance):
        """Sets the indicated_imbalance of this InsightsApiModelsResponsesIndicatedForecastIndicatedForecast.


        :param indicated_imbalance: The indicated_imbalance of this InsightsApiModelsResponsesIndicatedForecastIndicatedForecast.  # noqa: E501
        :type: int
        """

        self._indicated_imbalance = indicated_imbalance

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
        if issubclass(InsightsApiModelsResponsesIndicatedForecastIndicatedForecast, dict):
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
        if not isinstance(other, InsightsApiModelsResponsesIndicatedForecastIndicatedForecast):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
