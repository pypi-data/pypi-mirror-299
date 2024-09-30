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

class InsightsApiModelsResponsesBalancingDatasetRowsBidOfferAcceptanceLevelDatasetResponse(object):
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
        'settlement_date': 'date',
        'settlement_period_from': 'int',
        'settlement_period_to': 'int',
        'time_from': 'datetime',
        'time_to': 'datetime',
        'level_from': 'int',
        'level_to': 'int',
        'acceptance_number': 'int',
        'acceptance_time': 'datetime',
        'deemed_bo_flag': 'bool',
        'so_flag': 'bool',
        'amendment_flag': 'str',
        'stor_flag': 'bool',
        'rr_flag': 'bool',
        'national_grid_bm_unit': 'str',
        'bm_unit': 'str'
    }

    attribute_map = {
        'dataset': 'dataset',
        'settlement_date': 'settlementDate',
        'settlement_period_from': 'settlementPeriodFrom',
        'settlement_period_to': 'settlementPeriodTo',
        'time_from': 'timeFrom',
        'time_to': 'timeTo',
        'level_from': 'levelFrom',
        'level_to': 'levelTo',
        'acceptance_number': 'acceptanceNumber',
        'acceptance_time': 'acceptanceTime',
        'deemed_bo_flag': 'deemedBoFlag',
        'so_flag': 'soFlag',
        'amendment_flag': 'amendmentFlag',
        'stor_flag': 'storFlag',
        'rr_flag': 'rrFlag',
        'national_grid_bm_unit': 'nationalGridBmUnit',
        'bm_unit': 'bmUnit'
    }

    def __init__(self, dataset=None, settlement_date=None, settlement_period_from=None, settlement_period_to=None, time_from=None, time_to=None, level_from=None, level_to=None, acceptance_number=None, acceptance_time=None, deemed_bo_flag=None, so_flag=None, amendment_flag=None, stor_flag=None, rr_flag=None, national_grid_bm_unit=None, bm_unit=None):  # noqa: E501
        """InsightsApiModelsResponsesBalancingDatasetRowsBidOfferAcceptanceLevelDatasetResponse - a model defined in Swagger"""  # noqa: E501
        self._dataset = None
        self._settlement_date = None
        self._settlement_period_from = None
        self._settlement_period_to = None
        self._time_from = None
        self._time_to = None
        self._level_from = None
        self._level_to = None
        self._acceptance_number = None
        self._acceptance_time = None
        self._deemed_bo_flag = None
        self._so_flag = None
        self._amendment_flag = None
        self._stor_flag = None
        self._rr_flag = None
        self._national_grid_bm_unit = None
        self._bm_unit = None
        self.discriminator = None
        if dataset is not None:
            self.dataset = dataset
        if settlement_date is not None:
            self.settlement_date = settlement_date
        if settlement_period_from is not None:
            self.settlement_period_from = settlement_period_from
        if settlement_period_to is not None:
            self.settlement_period_to = settlement_period_to
        if time_from is not None:
            self.time_from = time_from
        if time_to is not None:
            self.time_to = time_to
        if level_from is not None:
            self.level_from = level_from
        if level_to is not None:
            self.level_to = level_to
        if acceptance_number is not None:
            self.acceptance_number = acceptance_number
        if acceptance_time is not None:
            self.acceptance_time = acceptance_time
        if deemed_bo_flag is not None:
            self.deemed_bo_flag = deemed_bo_flag
        if so_flag is not None:
            self.so_flag = so_flag
        if amendment_flag is not None:
            self.amendment_flag = amendment_flag
        if stor_flag is not None:
            self.stor_flag = stor_flag
        if rr_flag is not None:
            self.rr_flag = rr_flag
        if national_grid_bm_unit is not None:
            self.national_grid_bm_unit = national_grid_bm_unit
        if bm_unit is not None:
            self.bm_unit = bm_unit

    @property
    def dataset(self):
        """Gets the dataset of this InsightsApiModelsResponsesBalancingDatasetRowsBidOfferAcceptanceLevelDatasetResponse.  # noqa: E501


        :return: The dataset of this InsightsApiModelsResponsesBalancingDatasetRowsBidOfferAcceptanceLevelDatasetResponse.  # noqa: E501
        :rtype: str
        """
        return self._dataset

    @dataset.setter
    def dataset(self, dataset):
        """Sets the dataset of this InsightsApiModelsResponsesBalancingDatasetRowsBidOfferAcceptanceLevelDatasetResponse.


        :param dataset: The dataset of this InsightsApiModelsResponsesBalancingDatasetRowsBidOfferAcceptanceLevelDatasetResponse.  # noqa: E501
        :type: str
        """

        self._dataset = dataset

    @property
    def settlement_date(self):
        """Gets the settlement_date of this InsightsApiModelsResponsesBalancingDatasetRowsBidOfferAcceptanceLevelDatasetResponse.  # noqa: E501


        :return: The settlement_date of this InsightsApiModelsResponsesBalancingDatasetRowsBidOfferAcceptanceLevelDatasetResponse.  # noqa: E501
        :rtype: date
        """
        return self._settlement_date

    @settlement_date.setter
    def settlement_date(self, settlement_date):
        """Sets the settlement_date of this InsightsApiModelsResponsesBalancingDatasetRowsBidOfferAcceptanceLevelDatasetResponse.


        :param settlement_date: The settlement_date of this InsightsApiModelsResponsesBalancingDatasetRowsBidOfferAcceptanceLevelDatasetResponse.  # noqa: E501
        :type: date
        """

        self._settlement_date = settlement_date

    @property
    def settlement_period_from(self):
        """Gets the settlement_period_from of this InsightsApiModelsResponsesBalancingDatasetRowsBidOfferAcceptanceLevelDatasetResponse.  # noqa: E501


        :return: The settlement_period_from of this InsightsApiModelsResponsesBalancingDatasetRowsBidOfferAcceptanceLevelDatasetResponse.  # noqa: E501
        :rtype: int
        """
        return self._settlement_period_from

    @settlement_period_from.setter
    def settlement_period_from(self, settlement_period_from):
        """Sets the settlement_period_from of this InsightsApiModelsResponsesBalancingDatasetRowsBidOfferAcceptanceLevelDatasetResponse.


        :param settlement_period_from: The settlement_period_from of this InsightsApiModelsResponsesBalancingDatasetRowsBidOfferAcceptanceLevelDatasetResponse.  # noqa: E501
        :type: int
        """

        self._settlement_period_from = settlement_period_from

    @property
    def settlement_period_to(self):
        """Gets the settlement_period_to of this InsightsApiModelsResponsesBalancingDatasetRowsBidOfferAcceptanceLevelDatasetResponse.  # noqa: E501


        :return: The settlement_period_to of this InsightsApiModelsResponsesBalancingDatasetRowsBidOfferAcceptanceLevelDatasetResponse.  # noqa: E501
        :rtype: int
        """
        return self._settlement_period_to

    @settlement_period_to.setter
    def settlement_period_to(self, settlement_period_to):
        """Sets the settlement_period_to of this InsightsApiModelsResponsesBalancingDatasetRowsBidOfferAcceptanceLevelDatasetResponse.


        :param settlement_period_to: The settlement_period_to of this InsightsApiModelsResponsesBalancingDatasetRowsBidOfferAcceptanceLevelDatasetResponse.  # noqa: E501
        :type: int
        """

        self._settlement_period_to = settlement_period_to

    @property
    def time_from(self):
        """Gets the time_from of this InsightsApiModelsResponsesBalancingDatasetRowsBidOfferAcceptanceLevelDatasetResponse.  # noqa: E501


        :return: The time_from of this InsightsApiModelsResponsesBalancingDatasetRowsBidOfferAcceptanceLevelDatasetResponse.  # noqa: E501
        :rtype: datetime
        """
        return self._time_from

    @time_from.setter
    def time_from(self, time_from):
        """Sets the time_from of this InsightsApiModelsResponsesBalancingDatasetRowsBidOfferAcceptanceLevelDatasetResponse.


        :param time_from: The time_from of this InsightsApiModelsResponsesBalancingDatasetRowsBidOfferAcceptanceLevelDatasetResponse.  # noqa: E501
        :type: datetime
        """

        self._time_from = time_from

    @property
    def time_to(self):
        """Gets the time_to of this InsightsApiModelsResponsesBalancingDatasetRowsBidOfferAcceptanceLevelDatasetResponse.  # noqa: E501


        :return: The time_to of this InsightsApiModelsResponsesBalancingDatasetRowsBidOfferAcceptanceLevelDatasetResponse.  # noqa: E501
        :rtype: datetime
        """
        return self._time_to

    @time_to.setter
    def time_to(self, time_to):
        """Sets the time_to of this InsightsApiModelsResponsesBalancingDatasetRowsBidOfferAcceptanceLevelDatasetResponse.


        :param time_to: The time_to of this InsightsApiModelsResponsesBalancingDatasetRowsBidOfferAcceptanceLevelDatasetResponse.  # noqa: E501
        :type: datetime
        """

        self._time_to = time_to

    @property
    def level_from(self):
        """Gets the level_from of this InsightsApiModelsResponsesBalancingDatasetRowsBidOfferAcceptanceLevelDatasetResponse.  # noqa: E501


        :return: The level_from of this InsightsApiModelsResponsesBalancingDatasetRowsBidOfferAcceptanceLevelDatasetResponse.  # noqa: E501
        :rtype: int
        """
        return self._level_from

    @level_from.setter
    def level_from(self, level_from):
        """Sets the level_from of this InsightsApiModelsResponsesBalancingDatasetRowsBidOfferAcceptanceLevelDatasetResponse.


        :param level_from: The level_from of this InsightsApiModelsResponsesBalancingDatasetRowsBidOfferAcceptanceLevelDatasetResponse.  # noqa: E501
        :type: int
        """

        self._level_from = level_from

    @property
    def level_to(self):
        """Gets the level_to of this InsightsApiModelsResponsesBalancingDatasetRowsBidOfferAcceptanceLevelDatasetResponse.  # noqa: E501


        :return: The level_to of this InsightsApiModelsResponsesBalancingDatasetRowsBidOfferAcceptanceLevelDatasetResponse.  # noqa: E501
        :rtype: int
        """
        return self._level_to

    @level_to.setter
    def level_to(self, level_to):
        """Sets the level_to of this InsightsApiModelsResponsesBalancingDatasetRowsBidOfferAcceptanceLevelDatasetResponse.


        :param level_to: The level_to of this InsightsApiModelsResponsesBalancingDatasetRowsBidOfferAcceptanceLevelDatasetResponse.  # noqa: E501
        :type: int
        """

        self._level_to = level_to

    @property
    def acceptance_number(self):
        """Gets the acceptance_number of this InsightsApiModelsResponsesBalancingDatasetRowsBidOfferAcceptanceLevelDatasetResponse.  # noqa: E501


        :return: The acceptance_number of this InsightsApiModelsResponsesBalancingDatasetRowsBidOfferAcceptanceLevelDatasetResponse.  # noqa: E501
        :rtype: int
        """
        return self._acceptance_number

    @acceptance_number.setter
    def acceptance_number(self, acceptance_number):
        """Sets the acceptance_number of this InsightsApiModelsResponsesBalancingDatasetRowsBidOfferAcceptanceLevelDatasetResponse.


        :param acceptance_number: The acceptance_number of this InsightsApiModelsResponsesBalancingDatasetRowsBidOfferAcceptanceLevelDatasetResponse.  # noqa: E501
        :type: int
        """

        self._acceptance_number = acceptance_number

    @property
    def acceptance_time(self):
        """Gets the acceptance_time of this InsightsApiModelsResponsesBalancingDatasetRowsBidOfferAcceptanceLevelDatasetResponse.  # noqa: E501


        :return: The acceptance_time of this InsightsApiModelsResponsesBalancingDatasetRowsBidOfferAcceptanceLevelDatasetResponse.  # noqa: E501
        :rtype: datetime
        """
        return self._acceptance_time

    @acceptance_time.setter
    def acceptance_time(self, acceptance_time):
        """Sets the acceptance_time of this InsightsApiModelsResponsesBalancingDatasetRowsBidOfferAcceptanceLevelDatasetResponse.


        :param acceptance_time: The acceptance_time of this InsightsApiModelsResponsesBalancingDatasetRowsBidOfferAcceptanceLevelDatasetResponse.  # noqa: E501
        :type: datetime
        """

        self._acceptance_time = acceptance_time

    @property
    def deemed_bo_flag(self):
        """Gets the deemed_bo_flag of this InsightsApiModelsResponsesBalancingDatasetRowsBidOfferAcceptanceLevelDatasetResponse.  # noqa: E501


        :return: The deemed_bo_flag of this InsightsApiModelsResponsesBalancingDatasetRowsBidOfferAcceptanceLevelDatasetResponse.  # noqa: E501
        :rtype: bool
        """
        return self._deemed_bo_flag

    @deemed_bo_flag.setter
    def deemed_bo_flag(self, deemed_bo_flag):
        """Sets the deemed_bo_flag of this InsightsApiModelsResponsesBalancingDatasetRowsBidOfferAcceptanceLevelDatasetResponse.


        :param deemed_bo_flag: The deemed_bo_flag of this InsightsApiModelsResponsesBalancingDatasetRowsBidOfferAcceptanceLevelDatasetResponse.  # noqa: E501
        :type: bool
        """

        self._deemed_bo_flag = deemed_bo_flag

    @property
    def so_flag(self):
        """Gets the so_flag of this InsightsApiModelsResponsesBalancingDatasetRowsBidOfferAcceptanceLevelDatasetResponse.  # noqa: E501


        :return: The so_flag of this InsightsApiModelsResponsesBalancingDatasetRowsBidOfferAcceptanceLevelDatasetResponse.  # noqa: E501
        :rtype: bool
        """
        return self._so_flag

    @so_flag.setter
    def so_flag(self, so_flag):
        """Sets the so_flag of this InsightsApiModelsResponsesBalancingDatasetRowsBidOfferAcceptanceLevelDatasetResponse.


        :param so_flag: The so_flag of this InsightsApiModelsResponsesBalancingDatasetRowsBidOfferAcceptanceLevelDatasetResponse.  # noqa: E501
        :type: bool
        """

        self._so_flag = so_flag

    @property
    def amendment_flag(self):
        """Gets the amendment_flag of this InsightsApiModelsResponsesBalancingDatasetRowsBidOfferAcceptanceLevelDatasetResponse.  # noqa: E501


        :return: The amendment_flag of this InsightsApiModelsResponsesBalancingDatasetRowsBidOfferAcceptanceLevelDatasetResponse.  # noqa: E501
        :rtype: str
        """
        return self._amendment_flag

    @amendment_flag.setter
    def amendment_flag(self, amendment_flag):
        """Sets the amendment_flag of this InsightsApiModelsResponsesBalancingDatasetRowsBidOfferAcceptanceLevelDatasetResponse.


        :param amendment_flag: The amendment_flag of this InsightsApiModelsResponsesBalancingDatasetRowsBidOfferAcceptanceLevelDatasetResponse.  # noqa: E501
        :type: str
        """

        self._amendment_flag = amendment_flag

    @property
    def stor_flag(self):
        """Gets the stor_flag of this InsightsApiModelsResponsesBalancingDatasetRowsBidOfferAcceptanceLevelDatasetResponse.  # noqa: E501


        :return: The stor_flag of this InsightsApiModelsResponsesBalancingDatasetRowsBidOfferAcceptanceLevelDatasetResponse.  # noqa: E501
        :rtype: bool
        """
        return self._stor_flag

    @stor_flag.setter
    def stor_flag(self, stor_flag):
        """Sets the stor_flag of this InsightsApiModelsResponsesBalancingDatasetRowsBidOfferAcceptanceLevelDatasetResponse.


        :param stor_flag: The stor_flag of this InsightsApiModelsResponsesBalancingDatasetRowsBidOfferAcceptanceLevelDatasetResponse.  # noqa: E501
        :type: bool
        """

        self._stor_flag = stor_flag

    @property
    def rr_flag(self):
        """Gets the rr_flag of this InsightsApiModelsResponsesBalancingDatasetRowsBidOfferAcceptanceLevelDatasetResponse.  # noqa: E501


        :return: The rr_flag of this InsightsApiModelsResponsesBalancingDatasetRowsBidOfferAcceptanceLevelDatasetResponse.  # noqa: E501
        :rtype: bool
        """
        return self._rr_flag

    @rr_flag.setter
    def rr_flag(self, rr_flag):
        """Sets the rr_flag of this InsightsApiModelsResponsesBalancingDatasetRowsBidOfferAcceptanceLevelDatasetResponse.


        :param rr_flag: The rr_flag of this InsightsApiModelsResponsesBalancingDatasetRowsBidOfferAcceptanceLevelDatasetResponse.  # noqa: E501
        :type: bool
        """

        self._rr_flag = rr_flag

    @property
    def national_grid_bm_unit(self):
        """Gets the national_grid_bm_unit of this InsightsApiModelsResponsesBalancingDatasetRowsBidOfferAcceptanceLevelDatasetResponse.  # noqa: E501


        :return: The national_grid_bm_unit of this InsightsApiModelsResponsesBalancingDatasetRowsBidOfferAcceptanceLevelDatasetResponse.  # noqa: E501
        :rtype: str
        """
        return self._national_grid_bm_unit

    @national_grid_bm_unit.setter
    def national_grid_bm_unit(self, national_grid_bm_unit):
        """Sets the national_grid_bm_unit of this InsightsApiModelsResponsesBalancingDatasetRowsBidOfferAcceptanceLevelDatasetResponse.


        :param national_grid_bm_unit: The national_grid_bm_unit of this InsightsApiModelsResponsesBalancingDatasetRowsBidOfferAcceptanceLevelDatasetResponse.  # noqa: E501
        :type: str
        """

        self._national_grid_bm_unit = national_grid_bm_unit

    @property
    def bm_unit(self):
        """Gets the bm_unit of this InsightsApiModelsResponsesBalancingDatasetRowsBidOfferAcceptanceLevelDatasetResponse.  # noqa: E501


        :return: The bm_unit of this InsightsApiModelsResponsesBalancingDatasetRowsBidOfferAcceptanceLevelDatasetResponse.  # noqa: E501
        :rtype: str
        """
        return self._bm_unit

    @bm_unit.setter
    def bm_unit(self, bm_unit):
        """Sets the bm_unit of this InsightsApiModelsResponsesBalancingDatasetRowsBidOfferAcceptanceLevelDatasetResponse.


        :param bm_unit: The bm_unit of this InsightsApiModelsResponsesBalancingDatasetRowsBidOfferAcceptanceLevelDatasetResponse.  # noqa: E501
        :type: str
        """

        self._bm_unit = bm_unit

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
        if issubclass(InsightsApiModelsResponsesBalancingDatasetRowsBidOfferAcceptanceLevelDatasetResponse, dict):
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
        if not isinstance(other, InsightsApiModelsResponsesBalancingDatasetRowsBidOfferAcceptanceLevelDatasetResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
