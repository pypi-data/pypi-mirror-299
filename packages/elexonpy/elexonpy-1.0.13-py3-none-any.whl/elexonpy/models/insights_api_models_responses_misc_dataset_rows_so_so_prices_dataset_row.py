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

class InsightsApiModelsResponsesMiscDatasetRowsSoSoPricesDatasetRow(object):
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
        'dataset': 'str',
        'publish_time': 'datetime',
        'sender_identification': 'str',
        'receiver_identification': 'str',
        'contract_identification': 'str',
        'resource_provider': 'str',
        'trade_direction': 'str',
        'trade_quantity': 'float',
        'trade_price': 'float',
        'trader_unit': 'str',
        'start_time': 'datetime',
        'end_time': 'datetime',
        'settlement_date': 'date'
    }

    attribute_map = {
        'dataset': 'dataset',
        'publish_time': 'publishTime',
        'sender_identification': 'senderIdentification',
        'receiver_identification': 'receiverIdentification',
        'contract_identification': 'contractIdentification',
        'resource_provider': 'resourceProvider',
        'trade_direction': 'tradeDirection',
        'trade_quantity': 'tradeQuantity',
        'trade_price': 'tradePrice',
        'trader_unit': 'traderUnit',
        'start_time': 'startTime',
        'end_time': 'endTime',
        'settlement_date': 'settlementDate'
    }

    def __init__(self, dataset=None, publish_time=None, sender_identification=None, receiver_identification=None, contract_identification=None, resource_provider=None, trade_direction=None, trade_quantity=None, trade_price=None, trader_unit=None, start_time=None, end_time=None, settlement_date=None):  # noqa: E501
        """InsightsApiModelsResponsesMiscDatasetRowsSoSoPricesDatasetRow - a model defined in Swagger"""  # noqa: E501
        self._dataset = None
        self._publish_time = None
        self._sender_identification = None
        self._receiver_identification = None
        self._contract_identification = None
        self._resource_provider = None
        self._trade_direction = None
        self._trade_quantity = None
        self._trade_price = None
        self._trader_unit = None
        self._start_time = None
        self._end_time = None
        self._settlement_date = None
        self.discriminator = None
        if dataset is not None:
            self.dataset = dataset
        if publish_time is not None:
            self.publish_time = publish_time
        if sender_identification is not None:
            self.sender_identification = sender_identification
        if receiver_identification is not None:
            self.receiver_identification = receiver_identification
        if contract_identification is not None:
            self.contract_identification = contract_identification
        if resource_provider is not None:
            self.resource_provider = resource_provider
        if trade_direction is not None:
            self.trade_direction = trade_direction
        if trade_quantity is not None:
            self.trade_quantity = trade_quantity
        if trade_price is not None:
            self.trade_price = trade_price
        if trader_unit is not None:
            self.trader_unit = trader_unit
        if start_time is not None:
            self.start_time = start_time
        if end_time is not None:
            self.end_time = end_time
        if settlement_date is not None:
            self.settlement_date = settlement_date

    @property
    def dataset(self):
        """Gets the dataset of this InsightsApiModelsResponsesMiscDatasetRowsSoSoPricesDatasetRow.  # noqa: E501


        :return: The dataset of this InsightsApiModelsResponsesMiscDatasetRowsSoSoPricesDatasetRow.  # noqa: E501
        :rtype: str
        """
        return self._dataset

    @dataset.setter
    def dataset(self, dataset):
        """Sets the dataset of this InsightsApiModelsResponsesMiscDatasetRowsSoSoPricesDatasetRow.


        :param dataset: The dataset of this InsightsApiModelsResponsesMiscDatasetRowsSoSoPricesDatasetRow.  # noqa: E501
        :type: str
        """

        self._dataset = dataset

    @property
    def publish_time(self):
        """Gets the publish_time of this InsightsApiModelsResponsesMiscDatasetRowsSoSoPricesDatasetRow.  # noqa: E501


        :return: The publish_time of this InsightsApiModelsResponsesMiscDatasetRowsSoSoPricesDatasetRow.  # noqa: E501
        :rtype: datetime
        """
        return self._publish_time

    @publish_time.setter
    def publish_time(self, publish_time):
        """Sets the publish_time of this InsightsApiModelsResponsesMiscDatasetRowsSoSoPricesDatasetRow.


        :param publish_time: The publish_time of this InsightsApiModelsResponsesMiscDatasetRowsSoSoPricesDatasetRow.  # noqa: E501
        :type: datetime
        """

        self._publish_time = publish_time

    @property
    def sender_identification(self):
        """Gets the sender_identification of this InsightsApiModelsResponsesMiscDatasetRowsSoSoPricesDatasetRow.  # noqa: E501


        :return: The sender_identification of this InsightsApiModelsResponsesMiscDatasetRowsSoSoPricesDatasetRow.  # noqa: E501
        :rtype: str
        """
        return self._sender_identification

    @sender_identification.setter
    def sender_identification(self, sender_identification):
        """Sets the sender_identification of this InsightsApiModelsResponsesMiscDatasetRowsSoSoPricesDatasetRow.


        :param sender_identification: The sender_identification of this InsightsApiModelsResponsesMiscDatasetRowsSoSoPricesDatasetRow.  # noqa: E501
        :type: str
        """

        self._sender_identification = sender_identification

    @property
    def receiver_identification(self):
        """Gets the receiver_identification of this InsightsApiModelsResponsesMiscDatasetRowsSoSoPricesDatasetRow.  # noqa: E501


        :return: The receiver_identification of this InsightsApiModelsResponsesMiscDatasetRowsSoSoPricesDatasetRow.  # noqa: E501
        :rtype: str
        """
        return self._receiver_identification

    @receiver_identification.setter
    def receiver_identification(self, receiver_identification):
        """Sets the receiver_identification of this InsightsApiModelsResponsesMiscDatasetRowsSoSoPricesDatasetRow.


        :param receiver_identification: The receiver_identification of this InsightsApiModelsResponsesMiscDatasetRowsSoSoPricesDatasetRow.  # noqa: E501
        :type: str
        """

        self._receiver_identification = receiver_identification

    @property
    def contract_identification(self):
        """Gets the contract_identification of this InsightsApiModelsResponsesMiscDatasetRowsSoSoPricesDatasetRow.  # noqa: E501


        :return: The contract_identification of this InsightsApiModelsResponsesMiscDatasetRowsSoSoPricesDatasetRow.  # noqa: E501
        :rtype: str
        """
        return self._contract_identification

    @contract_identification.setter
    def contract_identification(self, contract_identification):
        """Sets the contract_identification of this InsightsApiModelsResponsesMiscDatasetRowsSoSoPricesDatasetRow.


        :param contract_identification: The contract_identification of this InsightsApiModelsResponsesMiscDatasetRowsSoSoPricesDatasetRow.  # noqa: E501
        :type: str
        """

        self._contract_identification = contract_identification

    @property
    def resource_provider(self):
        """Gets the resource_provider of this InsightsApiModelsResponsesMiscDatasetRowsSoSoPricesDatasetRow.  # noqa: E501


        :return: The resource_provider of this InsightsApiModelsResponsesMiscDatasetRowsSoSoPricesDatasetRow.  # noqa: E501
        :rtype: str
        """
        return self._resource_provider

    @resource_provider.setter
    def resource_provider(self, resource_provider):
        """Sets the resource_provider of this InsightsApiModelsResponsesMiscDatasetRowsSoSoPricesDatasetRow.


        :param resource_provider: The resource_provider of this InsightsApiModelsResponsesMiscDatasetRowsSoSoPricesDatasetRow.  # noqa: E501
        :type: str
        """

        self._resource_provider = resource_provider

    @property
    def trade_direction(self):
        """Gets the trade_direction of this InsightsApiModelsResponsesMiscDatasetRowsSoSoPricesDatasetRow.  # noqa: E501


        :return: The trade_direction of this InsightsApiModelsResponsesMiscDatasetRowsSoSoPricesDatasetRow.  # noqa: E501
        :rtype: str
        """
        return self._trade_direction

    @trade_direction.setter
    def trade_direction(self, trade_direction):
        """Sets the trade_direction of this InsightsApiModelsResponsesMiscDatasetRowsSoSoPricesDatasetRow.


        :param trade_direction: The trade_direction of this InsightsApiModelsResponsesMiscDatasetRowsSoSoPricesDatasetRow.  # noqa: E501
        :type: str
        """

        self._trade_direction = trade_direction

    @property
    def trade_quantity(self):
        """Gets the trade_quantity of this InsightsApiModelsResponsesMiscDatasetRowsSoSoPricesDatasetRow.  # noqa: E501


        :return: The trade_quantity of this InsightsApiModelsResponsesMiscDatasetRowsSoSoPricesDatasetRow.  # noqa: E501
        :rtype: float
        """
        return self._trade_quantity

    @trade_quantity.setter
    def trade_quantity(self, trade_quantity):
        """Sets the trade_quantity of this InsightsApiModelsResponsesMiscDatasetRowsSoSoPricesDatasetRow.


        :param trade_quantity: The trade_quantity of this InsightsApiModelsResponsesMiscDatasetRowsSoSoPricesDatasetRow.  # noqa: E501
        :type: float
        """

        self._trade_quantity = trade_quantity

    @property
    def trade_price(self):
        """Gets the trade_price of this InsightsApiModelsResponsesMiscDatasetRowsSoSoPricesDatasetRow.  # noqa: E501


        :return: The trade_price of this InsightsApiModelsResponsesMiscDatasetRowsSoSoPricesDatasetRow.  # noqa: E501
        :rtype: float
        """
        return self._trade_price

    @trade_price.setter
    def trade_price(self, trade_price):
        """Sets the trade_price of this InsightsApiModelsResponsesMiscDatasetRowsSoSoPricesDatasetRow.


        :param trade_price: The trade_price of this InsightsApiModelsResponsesMiscDatasetRowsSoSoPricesDatasetRow.  # noqa: E501
        :type: float
        """

        self._trade_price = trade_price

    @property
    def trader_unit(self):
        """Gets the trader_unit of this InsightsApiModelsResponsesMiscDatasetRowsSoSoPricesDatasetRow.  # noqa: E501


        :return: The trader_unit of this InsightsApiModelsResponsesMiscDatasetRowsSoSoPricesDatasetRow.  # noqa: E501
        :rtype: str
        """
        return self._trader_unit

    @trader_unit.setter
    def trader_unit(self, trader_unit):
        """Sets the trader_unit of this InsightsApiModelsResponsesMiscDatasetRowsSoSoPricesDatasetRow.


        :param trader_unit: The trader_unit of this InsightsApiModelsResponsesMiscDatasetRowsSoSoPricesDatasetRow.  # noqa: E501
        :type: str
        """

        self._trader_unit = trader_unit

    @property
    def start_time(self):
        """Gets the start_time of this InsightsApiModelsResponsesMiscDatasetRowsSoSoPricesDatasetRow.  # noqa: E501


        :return: The start_time of this InsightsApiModelsResponsesMiscDatasetRowsSoSoPricesDatasetRow.  # noqa: E501
        :rtype: datetime
        """
        return self._start_time

    @start_time.setter
    def start_time(self, start_time):
        """Sets the start_time of this InsightsApiModelsResponsesMiscDatasetRowsSoSoPricesDatasetRow.


        :param start_time: The start_time of this InsightsApiModelsResponsesMiscDatasetRowsSoSoPricesDatasetRow.  # noqa: E501
        :type: datetime
        """

        self._start_time = start_time

    @property
    def end_time(self):
        """Gets the end_time of this InsightsApiModelsResponsesMiscDatasetRowsSoSoPricesDatasetRow.  # noqa: E501


        :return: The end_time of this InsightsApiModelsResponsesMiscDatasetRowsSoSoPricesDatasetRow.  # noqa: E501
        :rtype: datetime
        """
        return self._end_time

    @end_time.setter
    def end_time(self, end_time):
        """Sets the end_time of this InsightsApiModelsResponsesMiscDatasetRowsSoSoPricesDatasetRow.


        :param end_time: The end_time of this InsightsApiModelsResponsesMiscDatasetRowsSoSoPricesDatasetRow.  # noqa: E501
        :type: datetime
        """

        self._end_time = end_time

    @property
    def settlement_date(self):
        """Gets the settlement_date of this InsightsApiModelsResponsesMiscDatasetRowsSoSoPricesDatasetRow.  # noqa: E501


        :return: The settlement_date of this InsightsApiModelsResponsesMiscDatasetRowsSoSoPricesDatasetRow.  # noqa: E501
        :rtype: date
        """
        return self._settlement_date

    @settlement_date.setter
    def settlement_date(self, settlement_date):
        """Sets the settlement_date of this InsightsApiModelsResponsesMiscDatasetRowsSoSoPricesDatasetRow.


        :param settlement_date: The settlement_date of this InsightsApiModelsResponsesMiscDatasetRowsSoSoPricesDatasetRow.  # noqa: E501
        :type: date
        """

        self._settlement_date = settlement_date

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
        if issubclass(InsightsApiModelsResponsesMiscDatasetRowsSoSoPricesDatasetRow, dict):
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
        if not isinstance(other, InsightsApiModelsResponsesMiscDatasetRowsSoSoPricesDatasetRow):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
