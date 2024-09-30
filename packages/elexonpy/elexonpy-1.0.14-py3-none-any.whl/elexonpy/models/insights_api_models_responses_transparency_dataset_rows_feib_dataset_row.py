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

class InsightsApiModelsResponsesTransparencyDatasetRowsFeibDatasetRow(object):
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
        'document_id': 'str',
        'document_revision_number': 'int',
        'publish_time': 'datetime',
        'status': 'str',
        'year': 'int',
        'month': 'str',
        'amount': 'float',
        'price_direction': 'str'
    }

    attribute_map = {
        'dataset': 'dataset',
        'document_id': 'documentId',
        'document_revision_number': 'documentRevisionNumber',
        'publish_time': 'publishTime',
        'status': 'status',
        'year': 'year',
        'month': 'month',
        'amount': 'amount',
        'price_direction': 'priceDirection'
    }

    def __init__(self, dataset=None, document_id=None, document_revision_number=None, publish_time=None, status=None, year=None, month=None, amount=None, price_direction=None):  # noqa: E501
        """InsightsApiModelsResponsesTransparencyDatasetRowsFeibDatasetRow - a model defined in Swagger"""  # noqa: E501
        self._dataset = None
        self._document_id = None
        self._document_revision_number = None
        self._publish_time = None
        self._status = None
        self._year = None
        self._month = None
        self._amount = None
        self._price_direction = None
        self.discriminator = None
        if dataset is not None:
            self.dataset = dataset
        if document_id is not None:
            self.document_id = document_id
        if document_revision_number is not None:
            self.document_revision_number = document_revision_number
        if publish_time is not None:
            self.publish_time = publish_time
        if status is not None:
            self.status = status
        if year is not None:
            self.year = year
        if month is not None:
            self.month = month
        if amount is not None:
            self.amount = amount
        if price_direction is not None:
            self.price_direction = price_direction

    @property
    def dataset(self):
        """Gets the dataset of this InsightsApiModelsResponsesTransparencyDatasetRowsFeibDatasetRow.  # noqa: E501


        :return: The dataset of this InsightsApiModelsResponsesTransparencyDatasetRowsFeibDatasetRow.  # noqa: E501
        :rtype: str
        """
        return self._dataset

    @dataset.setter
    def dataset(self, dataset):
        """Sets the dataset of this InsightsApiModelsResponsesTransparencyDatasetRowsFeibDatasetRow.


        :param dataset: The dataset of this InsightsApiModelsResponsesTransparencyDatasetRowsFeibDatasetRow.  # noqa: E501
        :type: str
        """

        self._dataset = dataset

    @property
    def document_id(self):
        """Gets the document_id of this InsightsApiModelsResponsesTransparencyDatasetRowsFeibDatasetRow.  # noqa: E501


        :return: The document_id of this InsightsApiModelsResponsesTransparencyDatasetRowsFeibDatasetRow.  # noqa: E501
        :rtype: str
        """
        return self._document_id

    @document_id.setter
    def document_id(self, document_id):
        """Sets the document_id of this InsightsApiModelsResponsesTransparencyDatasetRowsFeibDatasetRow.


        :param document_id: The document_id of this InsightsApiModelsResponsesTransparencyDatasetRowsFeibDatasetRow.  # noqa: E501
        :type: str
        """

        self._document_id = document_id

    @property
    def document_revision_number(self):
        """Gets the document_revision_number of this InsightsApiModelsResponsesTransparencyDatasetRowsFeibDatasetRow.  # noqa: E501


        :return: The document_revision_number of this InsightsApiModelsResponsesTransparencyDatasetRowsFeibDatasetRow.  # noqa: E501
        :rtype: int
        """
        return self._document_revision_number

    @document_revision_number.setter
    def document_revision_number(self, document_revision_number):
        """Sets the document_revision_number of this InsightsApiModelsResponsesTransparencyDatasetRowsFeibDatasetRow.


        :param document_revision_number: The document_revision_number of this InsightsApiModelsResponsesTransparencyDatasetRowsFeibDatasetRow.  # noqa: E501
        :type: int
        """

        self._document_revision_number = document_revision_number

    @property
    def publish_time(self):
        """Gets the publish_time of this InsightsApiModelsResponsesTransparencyDatasetRowsFeibDatasetRow.  # noqa: E501


        :return: The publish_time of this InsightsApiModelsResponsesTransparencyDatasetRowsFeibDatasetRow.  # noqa: E501
        :rtype: datetime
        """
        return self._publish_time

    @publish_time.setter
    def publish_time(self, publish_time):
        """Sets the publish_time of this InsightsApiModelsResponsesTransparencyDatasetRowsFeibDatasetRow.


        :param publish_time: The publish_time of this InsightsApiModelsResponsesTransparencyDatasetRowsFeibDatasetRow.  # noqa: E501
        :type: datetime
        """

        self._publish_time = publish_time

    @property
    def status(self):
        """Gets the status of this InsightsApiModelsResponsesTransparencyDatasetRowsFeibDatasetRow.  # noqa: E501


        :return: The status of this InsightsApiModelsResponsesTransparencyDatasetRowsFeibDatasetRow.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this InsightsApiModelsResponsesTransparencyDatasetRowsFeibDatasetRow.


        :param status: The status of this InsightsApiModelsResponsesTransparencyDatasetRowsFeibDatasetRow.  # noqa: E501
        :type: str
        """

        self._status = status

    @property
    def year(self):
        """Gets the year of this InsightsApiModelsResponsesTransparencyDatasetRowsFeibDatasetRow.  # noqa: E501


        :return: The year of this InsightsApiModelsResponsesTransparencyDatasetRowsFeibDatasetRow.  # noqa: E501
        :rtype: int
        """
        return self._year

    @year.setter
    def year(self, year):
        """Sets the year of this InsightsApiModelsResponsesTransparencyDatasetRowsFeibDatasetRow.


        :param year: The year of this InsightsApiModelsResponsesTransparencyDatasetRowsFeibDatasetRow.  # noqa: E501
        :type: int
        """

        self._year = year

    @property
    def month(self):
        """Gets the month of this InsightsApiModelsResponsesTransparencyDatasetRowsFeibDatasetRow.  # noqa: E501


        :return: The month of this InsightsApiModelsResponsesTransparencyDatasetRowsFeibDatasetRow.  # noqa: E501
        :rtype: str
        """
        return self._month

    @month.setter
    def month(self, month):
        """Sets the month of this InsightsApiModelsResponsesTransparencyDatasetRowsFeibDatasetRow.


        :param month: The month of this InsightsApiModelsResponsesTransparencyDatasetRowsFeibDatasetRow.  # noqa: E501
        :type: str
        """

        self._month = month

    @property
    def amount(self):
        """Gets the amount of this InsightsApiModelsResponsesTransparencyDatasetRowsFeibDatasetRow.  # noqa: E501


        :return: The amount of this InsightsApiModelsResponsesTransparencyDatasetRowsFeibDatasetRow.  # noqa: E501
        :rtype: float
        """
        return self._amount

    @amount.setter
    def amount(self, amount):
        """Sets the amount of this InsightsApiModelsResponsesTransparencyDatasetRowsFeibDatasetRow.


        :param amount: The amount of this InsightsApiModelsResponsesTransparencyDatasetRowsFeibDatasetRow.  # noqa: E501
        :type: float
        """

        self._amount = amount

    @property
    def price_direction(self):
        """Gets the price_direction of this InsightsApiModelsResponsesTransparencyDatasetRowsFeibDatasetRow.  # noqa: E501


        :return: The price_direction of this InsightsApiModelsResponsesTransparencyDatasetRowsFeibDatasetRow.  # noqa: E501
        :rtype: str
        """
        return self._price_direction

    @price_direction.setter
    def price_direction(self, price_direction):
        """Sets the price_direction of this InsightsApiModelsResponsesTransparencyDatasetRowsFeibDatasetRow.


        :param price_direction: The price_direction of this InsightsApiModelsResponsesTransparencyDatasetRowsFeibDatasetRow.  # noqa: E501
        :type: str
        """

        self._price_direction = price_direction

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
        if issubclass(InsightsApiModelsResponsesTransparencyDatasetRowsFeibDatasetRow, dict):
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
        if not isinstance(other, InsightsApiModelsResponsesTransparencyDatasetRowsFeibDatasetRow):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
