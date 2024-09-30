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

class InsightsApiModelsResponsesBalancingCreditDefaultNoticeResponse(object):
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
        'participant_id': 'str',
        'participant_name': 'str',
        'credit_default_level': 'int',
        'entered_default_settlement_date': 'date',
        'entered_default_settlement_period': 'int',
        'cleared_default_settlement_date': 'date',
        'cleared_default_settlement_period': 'int',
        'cleared_default_text': 'str'
    }

    attribute_map = {
        'participant_id': 'participantId',
        'participant_name': 'participantName',
        'credit_default_level': 'creditDefaultLevel',
        'entered_default_settlement_date': 'enteredDefaultSettlementDate',
        'entered_default_settlement_period': 'enteredDefaultSettlementPeriod',
        'cleared_default_settlement_date': 'clearedDefaultSettlementDate',
        'cleared_default_settlement_period': 'clearedDefaultSettlementPeriod',
        'cleared_default_text': 'clearedDefaultText'
    }

    def __init__(self, participant_id=None, participant_name=None, credit_default_level=None, entered_default_settlement_date=None, entered_default_settlement_period=None, cleared_default_settlement_date=None, cleared_default_settlement_period=None, cleared_default_text=None):  # noqa: E501
        """InsightsApiModelsResponsesBalancingCreditDefaultNoticeResponse - a model defined in Swagger"""  # noqa: E501
        self._participant_id = None
        self._participant_name = None
        self._credit_default_level = None
        self._entered_default_settlement_date = None
        self._entered_default_settlement_period = None
        self._cleared_default_settlement_date = None
        self._cleared_default_settlement_period = None
        self._cleared_default_text = None
        self.discriminator = None
        if participant_id is not None:
            self.participant_id = participant_id
        if participant_name is not None:
            self.participant_name = participant_name
        if credit_default_level is not None:
            self.credit_default_level = credit_default_level
        if entered_default_settlement_date is not None:
            self.entered_default_settlement_date = entered_default_settlement_date
        if entered_default_settlement_period is not None:
            self.entered_default_settlement_period = entered_default_settlement_period
        if cleared_default_settlement_date is not None:
            self.cleared_default_settlement_date = cleared_default_settlement_date
        if cleared_default_settlement_period is not None:
            self.cleared_default_settlement_period = cleared_default_settlement_period
        if cleared_default_text is not None:
            self.cleared_default_text = cleared_default_text

    @property
    def participant_id(self):
        """Gets the participant_id of this InsightsApiModelsResponsesBalancingCreditDefaultNoticeResponse.  # noqa: E501


        :return: The participant_id of this InsightsApiModelsResponsesBalancingCreditDefaultNoticeResponse.  # noqa: E501
        :rtype: str
        """
        return self._participant_id

    @participant_id.setter
    def participant_id(self, participant_id):
        """Sets the participant_id of this InsightsApiModelsResponsesBalancingCreditDefaultNoticeResponse.


        :param participant_id: The participant_id of this InsightsApiModelsResponsesBalancingCreditDefaultNoticeResponse.  # noqa: E501
        :type: str
        """

        self._participant_id = participant_id

    @property
    def participant_name(self):
        """Gets the participant_name of this InsightsApiModelsResponsesBalancingCreditDefaultNoticeResponse.  # noqa: E501


        :return: The participant_name of this InsightsApiModelsResponsesBalancingCreditDefaultNoticeResponse.  # noqa: E501
        :rtype: str
        """
        return self._participant_name

    @participant_name.setter
    def participant_name(self, participant_name):
        """Sets the participant_name of this InsightsApiModelsResponsesBalancingCreditDefaultNoticeResponse.


        :param participant_name: The participant_name of this InsightsApiModelsResponsesBalancingCreditDefaultNoticeResponse.  # noqa: E501
        :type: str
        """

        self._participant_name = participant_name

    @property
    def credit_default_level(self):
        """Gets the credit_default_level of this InsightsApiModelsResponsesBalancingCreditDefaultNoticeResponse.  # noqa: E501


        :return: The credit_default_level of this InsightsApiModelsResponsesBalancingCreditDefaultNoticeResponse.  # noqa: E501
        :rtype: int
        """
        return self._credit_default_level

    @credit_default_level.setter
    def credit_default_level(self, credit_default_level):
        """Sets the credit_default_level of this InsightsApiModelsResponsesBalancingCreditDefaultNoticeResponse.


        :param credit_default_level: The credit_default_level of this InsightsApiModelsResponsesBalancingCreditDefaultNoticeResponse.  # noqa: E501
        :type: int
        """

        self._credit_default_level = credit_default_level

    @property
    def entered_default_settlement_date(self):
        """Gets the entered_default_settlement_date of this InsightsApiModelsResponsesBalancingCreditDefaultNoticeResponse.  # noqa: E501


        :return: The entered_default_settlement_date of this InsightsApiModelsResponsesBalancingCreditDefaultNoticeResponse.  # noqa: E501
        :rtype: date
        """
        return self._entered_default_settlement_date

    @entered_default_settlement_date.setter
    def entered_default_settlement_date(self, entered_default_settlement_date):
        """Sets the entered_default_settlement_date of this InsightsApiModelsResponsesBalancingCreditDefaultNoticeResponse.


        :param entered_default_settlement_date: The entered_default_settlement_date of this InsightsApiModelsResponsesBalancingCreditDefaultNoticeResponse.  # noqa: E501
        :type: date
        """

        self._entered_default_settlement_date = entered_default_settlement_date

    @property
    def entered_default_settlement_period(self):
        """Gets the entered_default_settlement_period of this InsightsApiModelsResponsesBalancingCreditDefaultNoticeResponse.  # noqa: E501


        :return: The entered_default_settlement_period of this InsightsApiModelsResponsesBalancingCreditDefaultNoticeResponse.  # noqa: E501
        :rtype: int
        """
        return self._entered_default_settlement_period

    @entered_default_settlement_period.setter
    def entered_default_settlement_period(self, entered_default_settlement_period):
        """Sets the entered_default_settlement_period of this InsightsApiModelsResponsesBalancingCreditDefaultNoticeResponse.


        :param entered_default_settlement_period: The entered_default_settlement_period of this InsightsApiModelsResponsesBalancingCreditDefaultNoticeResponse.  # noqa: E501
        :type: int
        """

        self._entered_default_settlement_period = entered_default_settlement_period

    @property
    def cleared_default_settlement_date(self):
        """Gets the cleared_default_settlement_date of this InsightsApiModelsResponsesBalancingCreditDefaultNoticeResponse.  # noqa: E501


        :return: The cleared_default_settlement_date of this InsightsApiModelsResponsesBalancingCreditDefaultNoticeResponse.  # noqa: E501
        :rtype: date
        """
        return self._cleared_default_settlement_date

    @cleared_default_settlement_date.setter
    def cleared_default_settlement_date(self, cleared_default_settlement_date):
        """Sets the cleared_default_settlement_date of this InsightsApiModelsResponsesBalancingCreditDefaultNoticeResponse.


        :param cleared_default_settlement_date: The cleared_default_settlement_date of this InsightsApiModelsResponsesBalancingCreditDefaultNoticeResponse.  # noqa: E501
        :type: date
        """

        self._cleared_default_settlement_date = cleared_default_settlement_date

    @property
    def cleared_default_settlement_period(self):
        """Gets the cleared_default_settlement_period of this InsightsApiModelsResponsesBalancingCreditDefaultNoticeResponse.  # noqa: E501


        :return: The cleared_default_settlement_period of this InsightsApiModelsResponsesBalancingCreditDefaultNoticeResponse.  # noqa: E501
        :rtype: int
        """
        return self._cleared_default_settlement_period

    @cleared_default_settlement_period.setter
    def cleared_default_settlement_period(self, cleared_default_settlement_period):
        """Sets the cleared_default_settlement_period of this InsightsApiModelsResponsesBalancingCreditDefaultNoticeResponse.


        :param cleared_default_settlement_period: The cleared_default_settlement_period of this InsightsApiModelsResponsesBalancingCreditDefaultNoticeResponse.  # noqa: E501
        :type: int
        """

        self._cleared_default_settlement_period = cleared_default_settlement_period

    @property
    def cleared_default_text(self):
        """Gets the cleared_default_text of this InsightsApiModelsResponsesBalancingCreditDefaultNoticeResponse.  # noqa: E501


        :return: The cleared_default_text of this InsightsApiModelsResponsesBalancingCreditDefaultNoticeResponse.  # noqa: E501
        :rtype: str
        """
        return self._cleared_default_text

    @cleared_default_text.setter
    def cleared_default_text(self, cleared_default_text):
        """Sets the cleared_default_text of this InsightsApiModelsResponsesBalancingCreditDefaultNoticeResponse.


        :param cleared_default_text: The cleared_default_text of this InsightsApiModelsResponsesBalancingCreditDefaultNoticeResponse.  # noqa: E501
        :type: str
        """

        self._cleared_default_text = cleared_default_text

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
        if issubclass(InsightsApiModelsResponsesBalancingCreditDefaultNoticeResponse, dict):
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
        if not isinstance(other, InsightsApiModelsResponsesBalancingCreditDefaultNoticeResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
