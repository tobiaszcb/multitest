from bokeh.models import HoverTool, ColumnDataSource
from bokeh.plotting import figure

from mongoengine.queryset import QuerySet
import numpy as np
import logging

logger = logging.getLogger(__name__)


class BokehService:

    def feedTestSuite(self, TestSuite: dict):
        self.test_suit = TestSuite
        self.tests = self.test_suit['tests']

    def _createData(self):
        """
        Extracts info about each test from given test suit.
        """
        t_durations_sec = [test['duration'] for test in self.tests]
        t_durations_mins = [round((secs / 60), 2) for secs in t_durations_sec]
        t_durations_tuples = [
            divmod(int(t_duration), 60) for t_duration in t_durations_sec
        ]

        data = {
            't_names': [test['name'] for test in self.tests],
            't_durations': t_durations_mins,
            't_durations_output': ["{}min {}s".format(m, s) for m, s in t_durations_tuples],
            't_did_pass': [True if len(test['err']) == 0 else False for test in self.tests],
            't_outs': [test['out'] for test in self.tests]
        }
        self.data = data

    def _createColumnDataSource(self) -> ColumnDataSource:
        """
        :return ColumnDataSource (bokeh) from data.
        """
        return ColumnDataSource(self.data)

    def _createFigure(self):
        """
        Creates bokeh figure with basic configuration.
        """
        fig = figure(
            x_range=self.data['t_names'],
            y_range=(0, 8),
            title="Test Suit: {}".format(self.test_suit['created']),
            toolbar_location=None,
            tools=""
        )
        self.figure = fig

    def _configureVbar(self):
        self.figure.vbar(
            source=self._createColumnDataSource(),
            x='t_names',
            width=0.5,
            top='t_durations',
            bottom=0,
            legend='Test duration'
        )

    def _createAndAddTooltips(self):
        tooltips = [
            ('TEST NAME', '@t_names'),
            ('TEST DURATION', '@t_durations_output'),
            ('TEST ERRORS', '@t_did_pass')
        ]
        self.figure.add_tools(HoverTool(tooltips=tooltips))

    def getFigure(self):
        try:
            self._createData()
            self._createFigure()
            self._configureVbar()
            self._createAndAddTooltips()
            # make some adjustments
            self.figure.legend.location = 'top_left'
            self.figure.xaxis.major_label_orientation = 1
            return self.figure
        except Exception as e:
            logger.debug("Exception in bokeh_service occured: {}".format(e))

    ############ METHODS FOR CREATING CHART FOR COMPARING ALL CUMSUMS FROM TestSuiteS ############

    def getCompareChartDict(self, queryset: QuerySet) -> dict:
        ts_dict = {}  # dict containg info about every test suit

        # loop through TestSuite objects in mongoengine Queryset result
        for TestSuite in queryset:
            numOfErrs = 0
            for test in TestSuite.tests:  # count number of errors in TestSuite
                if len(test.err) != 0:
                    numOfErrs += 1

            # for each TestSuite, we create a dict containing info about:
            # created date, duration of TS, all the tests (temporary) and number of errors
            ts_dict[TestSuite.testSuiteId] = {
                'created': TestSuite.created,
                'TestSuiteDuration': self._toMinutes(TestSuite.duration),
                'tests': TestSuite.tests,
                'numOfErrs': numOfErrs,
                'testNames': [t['name'] for t in TestSuite.tests]
            }

        for testSuiteId, TestSuiteDict in ts_dict.items():
            minutesArray = [self._toMinutes(d['duration']) for d in TestSuiteDict['tests']]  # also convert to minutes
            TestSuiteDict.update({'cumulativeSum': self._cumulativeSum(minutesArray)})
            del TestSuiteDict['tests']  # no need for Test object(db). We got all info we wanted from it.
        logger.info("Dict from getCompareChartDict")
        logger.info(ts_dict)
        return ts_dict

    def _toMinutes(self, seconds):
        try:
            return round(seconds / 60, 2)
        except TypeError: # if failed to add test suit duration to DB
            pass

    def _cumulativeSum(self, array):
        s = 0
        result = []
        for i in range(len(array)):
            s += array[i]
            result.append(s)
        return result

    def generateBokeh(self, ts_dict: dict):

        id_keys = list(ts_dict.keys())  # get all keys of ts_dict (testSuiteId)
        plot = figure(
            plot_width=800,
            plot_height=300,
            x_axis_label='Test index',
            y_axis_label='Test duration',
            x_minor_ticks=None,
        )

        sourceDict = {}  # store unique source for each test suit
        for s in range(len(ts_dict.items())):
            sourceDict.update({
                s: ColumnDataSource(data={
                    't_range': list(range(len(ts_dict[id_keys[s]]['testNames']))),
                    id_keys[s]: ts_dict[id_keys[s]]['cumulativeSum'],
                    't_names': ts_dict[id_keys[s]]['testNames']
                })
            })

        plotDict = {}  # create and store plot.line() for each test suit
        for i in range(len(ts_dict.keys())):
            plotDict.update({
                i: plot.line(x='t_range', y='{}'.format(id_keys[i]), source=sourceDict[i])
            })

        for index, (key, glyphRenderer) in enumerate(plotDict.items()):  # add hover tool for each line
            plot.add_tools(HoverTool(
                renderers=[glyphRenderer],
                tooltips=[
                    ('Cumulative duration', '@{}'.format(id_keys[index])),
                    ('Test', '@t_names')
                ],
                mode='vline'
            ))
        return plot
