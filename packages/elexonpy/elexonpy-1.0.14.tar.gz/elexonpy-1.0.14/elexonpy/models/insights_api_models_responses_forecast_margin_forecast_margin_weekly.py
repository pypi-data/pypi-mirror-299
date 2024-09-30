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

class InsightsApiModelsResponsesForecastMarginForecastMarginWeekly(object):
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
        'margin': 'int',
        'week': 'int',
        'year': 'int',
        'week_start_date': 'date'
    }

    attribute_map = {
        'publish_time': 'publishTime',
        'margin': 'margin',
        'week': 'week',
        'year': 'year',
        'week_start_date': 'weekStartDate'
    }

    def __init__(self, publish_time=None, margin=None, week=None, year=None, week_start_date=None):  # noqa: E501
        """InsightsApiModelsResponsesForecastMarginForecastMarginWeekly - a model defined in Swagger"""  # noqa: E501
        self._publish_time = None
        self._margin = None
        self._week = None
        self._year = None
        self._week_start_date = None
        self.discriminator = None
        if publish_time is not None:
            self.publish_time = publish_time
        if margin is not None:
            self.margin = margin
        if week is not None:
            self.week = week
        if year is not None:
            self.year = year
        if week_start_date is not None:
            self.week_start_date = week_start_date

    @property
    def publish_time(self):
        """Gets the publish_time of this InsightsApiModelsResponsesForecastMarginForecastMarginWeekly.  # noqa: E501


        :return: The publish_time of this InsightsApiModelsResponsesForecastMarginForecastMarginWeekly.  # noqa: E501
        :rtype: datetime
        """
        return self._publish_time

    @publish_time.setter
    def publish_time(self, publish_time):
        """Sets the publish_time of this InsightsApiModelsResponsesForecastMarginForecastMarginWeekly.


        :param publish_time: The publish_time of this InsightsApiModelsResponsesForecastMarginForecastMarginWeekly.  # noqa: E501
        :type: datetime
        """

        self._publish_time = publish_time

    @property
    def margin(self):
        """Gets the margin of this InsightsApiModelsResponsesForecastMarginForecastMarginWeekly.  # noqa: E501


        :return: The margin of this InsightsApiModelsResponsesForecastMarginForecastMarginWeekly.  # noqa: E501
        :rtype: int
        """
        return self._margin

    @margin.setter
    def margin(self, margin):
        """Sets the margin of this InsightsApiModelsResponsesForecastMarginForecastMarginWeekly.


        :param margin: The margin of this InsightsApiModelsResponsesForecastMarginForecastMarginWeekly.  # noqa: E501
        :type: int
        """

        self._margin = margin

    @property
    def week(self):
        """Gets the week of this InsightsApiModelsResponsesForecastMarginForecastMarginWeekly.  # noqa: E501


        :return: The week of this InsightsApiModelsResponsesForecastMarginForecastMarginWeekly.  # noqa: E501
        :rtype: int
        """
        return self._week

    @week.setter
    def week(self, week):
        """Sets the week of this InsightsApiModelsResponsesForecastMarginForecastMarginWeekly.


        :param week: The week of this InsightsApiModelsResponsesForecastMarginForecastMarginWeekly.  # noqa: E501
        :type: int
        """

        self._week = week

    @property
    def year(self):
        """Gets the year of this InsightsApiModelsResponsesForecastMarginForecastMarginWeekly.  # noqa: E501


        :return: The year of this InsightsApiModelsResponsesForecastMarginForecastMarginWeekly.  # noqa: E501
        :rtype: int
        """
        return self._year

    @year.setter
    def year(self, year):
        """Sets the year of this InsightsApiModelsResponsesForecastMarginForecastMarginWeekly.


        :param year: The year of this InsightsApiModelsResponsesForecastMarginForecastMarginWeekly.  # noqa: E501
        :type: int
        """

        self._year = year

    @property
    def week_start_date(self):
        """Gets the week_start_date of this InsightsApiModelsResponsesForecastMarginForecastMarginWeekly.  # noqa: E501


        :return: The week_start_date of this InsightsApiModelsResponsesForecastMarginForecastMarginWeekly.  # noqa: E501
        :rtype: date
        """
        return self._week_start_date

    @week_start_date.setter
    def week_start_date(self, week_start_date):
        """Sets the week_start_date of this InsightsApiModelsResponsesForecastMarginForecastMarginWeekly.


        :param week_start_date: The week_start_date of this InsightsApiModelsResponsesForecastMarginForecastMarginWeekly.  # noqa: E501
        :type: date
        """

        self._week_start_date = week_start_date

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
        if issubclass(InsightsApiModelsResponsesForecastMarginForecastMarginWeekly, dict):
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
        if not isinstance(other, InsightsApiModelsResponsesForecastMarginForecastMarginWeekly):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
