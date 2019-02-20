from django import forms
from core.models.test_dao import TestDAO
from django.forms import SelectDateWidget

import logging

testDAO = TestDAO()
logger = logging.getLogger(__name__)

TEST_SUIT_CHOICES = (1,2)

try:
    all_test_suits = testDAO.getAllTestSuites()
    test_suit_ids_lst = [(t.testSuiteId, t.created) for t in all_test_suits]
    TEST_SUIT_CHOICES = tuple(test_suit_ids_lst)
except Exception as e:
    logger.error("Error in stats/forms while getting test suits: %s" % e)
    pass

class TestSuiteIdForm(forms.Form):
    test_id = forms.ChoiceField(choices=TEST_SUIT_CHOICES)


class DatesToCompareForm(forms.Form):
    start_date = forms.DateField(
        widget=SelectDateWidget(years=range(2018,2020))
    )
    end_date = forms.DateField(
        widget=SelectDateWidget(
            years=range(2018, 2020),attrs={'class':'dateWidgetClass'}
        )
    )
