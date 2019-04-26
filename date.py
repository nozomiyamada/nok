# every 10 minute in one hour
time = []
for i in range(0,24):
    for j in range(0,6):
        time.append('{}:{}0:00'.format(i, j))
time.append('0:00:00')

# every 30 minute in one hour
time30 = []
for i in range(0,24):
    for j in range(0,2):
        time30.append('{}:{}0:00'.format(i, 3*j))
time30.append('0:00:00')


year2010 = ['2010-{}-1'.format(i) for i in range(1, 13)] + ['2011-1-1']
year2011 = ['2011-{}-1'.format(i) for i in range(1, 13)] + ['2012-1-1']
year2012 = ['2012-{}-1'.format(i) for i in range(1, 13)] + ['2013-1-1']
year2013 = ['2013-{}-1'.format(i) for i in range(1, 13)] + ['2014-1-1']
year2014 = ['2014-{}-1'.format(i) for i in range(1, 13)] + ['2015-1-1']
year2015 = ['2015-{}-1'.format(i) for i in range(1, 13)] + ['2016-1-1']
year2016 = ['2016-{}-1'.format(i) for i in range(1, 13)] + ['2017-1-1']
year2017 = ['2017-{}-1'.format(i) for i in range(1, 13)] + ['2018-1-1']
year2018 = ['2018-{}-1'.format(i) for i in range(1, 13)] + ['2019-1-1']

month2011_1 = ['2011-1-{}'.format(i) for i in range(1, 32)] + ['2011-2-1']
month2011_2 = ['2011-2-{}'.format(i) for i in range(1, 29)] + ['2011-3-1']
month2011_3 = ['2011-3-{}'.format(i) for i in range(1, 32)] + ['2011-4-1']
month2011_4 = ['2011-4-{}'.format(i) for i in range(1, 31)] + ['2011-5-1']
month2011_5 = ['2011-5-{}'.format(i) for i in range(1, 32)] + ['2011-6-1']
month2011_6 = ['2011-6-{}'.format(i) for i in range(1, 31)] + ['2011-7-1']
month2011_7 = ['2011-7-{}'.format(i) for i in range(1, 32)] + ['2011-8-1']
month2011_8 = ['2011-8-{}'.format(i) for i in range(1, 32)] + ['2011-9-1']
month2011_9 = ['2011-9-{}'.format(i) for i in range(1, 31)] + ['2011-10-1']
month2011_10 = ['2011-10-{}'.format(i) for i in range(1, 32)] + ['2011-11-1']
month2011_11 = ['2011-11-{}'.format(i) for i in range(1, 31)] + ['2011-12-1']
month2011_12 = ['2011-12-{}'.format(i) for i in range(1, 32)] + ['2012-1-1']

month2012_1 = ['2012-1-{}'.format(i) for i in range(1, 32)] + ['2012-2-1']
month2012_2 = ['2012-2-{}'.format(i) for i in range(1, 30)] + ['2012-3-1']
month2012_3 = ['2012-3-{}'.format(i) for i in range(1, 32)] + ['2012-4-1']
month2012_4 = ['2012-4-{}'.format(i) for i in range(1, 31)] + ['2012-5-1']
month2012_5 = ['2012-5-{}'.format(i) for i in range(1, 32)] + ['2012-6-1']
month2012_6 = ['2012-6-{}'.format(i) for i in range(1, 31)] + ['2012-7-1']
month2012_7 = ['2012-7-{}'.format(i) for i in range(1, 32)] + ['2012-8-1']
month2012_8 = ['2012-8-{}'.format(i) for i in range(1, 32)] + ['2012-9-1']
month2012_9 = ['2012-9-{}'.format(i) for i in range(1, 31)] + ['2012-10-1']
month2012_10 = ['2012-10-{}'.format(i) for i in range(1, 32)] + ['2012-11-1']
month2012_11 = ['2012-11-{}'.format(i) for i in range(1, 31)] + ['2012-12-1']
month2012_12 = ['2012-12-{}'.format(i) for i in range(1, 32)] + ['2013-1-1']

month2013_1 = ['2013-1-{}'.format(i) for i in range(1, 32)] + ['2013-2-1']
month2013_2 = ['2013-2-{}'.format(i) for i in range(1, 29)] + ['2013-3-1']
month2013_3 = ['2013-3-{}'.format(i) for i in range(1, 32)] + ['2013-4-1']
month2013_4 = ['2013-4-{}'.format(i) for i in range(1, 31)] + ['2013-5-1']
month2013_5 = ['2013-5-{}'.format(i) for i in range(1, 32)] + ['2013-6-1']
month2013_6 = ['2013-6-{}'.format(i) for i in range(1, 31)] + ['2013-7-1']
month2013_7 = ['2013-7-{}'.format(i) for i in range(1, 32)] + ['2013-8-1']
month2013_8 = ['2013-8-{}'.format(i) for i in range(1, 32)] + ['2013-9-1']
month2013_9 = ['2013-9-{}'.format(i) for i in range(1, 31)] + ['2013-10-1']
month2013_10 = ['2013-10-{}'.format(i) for i in range(1, 32)] + ['2013-11-1']
month2013_11 = ['2013-11-{}'.format(i) for i in range(1, 31)] + ['2013-12-1']
month2013_12 = ['2013-12-{}'.format(i) for i in range(1, 32)] + ['2014-1-1']

month2014_1 = ['2014-1-{}'.format(i) for i in range(1, 32)] + ['2014-2-1']
month2014_2 = ['2014-2-{}'.format(i) for i in range(1, 29)] + ['2014-3-1']
month2014_3 = ['2014-3-{}'.format(i) for i in range(1, 32)] + ['2014-4-1']
month2014_4 = ['2014-4-{}'.format(i) for i in range(1, 31)] + ['2014-5-1']
month2014_5 = ['2014-5-{}'.format(i) for i in range(1, 32)] + ['2014-6-1']
month2014_6 = ['2014-6-{}'.format(i) for i in range(1, 31)] + ['2014-7-1']
month2014_7 = ['2014-7-{}'.format(i) for i in range(1, 32)] + ['2014-8-1']
month2014_8 = ['2014-8-{}'.format(i) for i in range(1, 32)] + ['2014-9-1']
month2014_9 = ['2014-9-{}'.format(i) for i in range(1, 31)] + ['2014-10-1']
month2014_10 = ['2014-10-{}'.format(i) for i in range(1, 32)] + ['2014-11-1']
month2014_11 = ['2014-11-{}'.format(i) for i in range(1, 31)] + ['2014-12-1']
month2014_12 = ['2014-12-{}'.format(i) for i in range(1, 32)] + ['2015-1-1']

month2015_1 = ['2015-1-{}'.format(i) for i in range(1, 32)] + ['2015-2-1']
month2015_2 = ['2015-2-{}'.format(i) for i in range(1, 29)] + ['2015-3-1']
month2015_3 = ['2015-3-{}'.format(i) for i in range(1, 32)] + ['2015-4-1']
month2015_4 = ['2015-4-{}'.format(i) for i in range(1, 31)] + ['2015-5-1']
month2015_5 = ['2015-5-{}'.format(i) for i in range(1, 32)] + ['2015-6-1']
month2015_6 = ['2015-6-{}'.format(i) for i in range(1, 31)] + ['2015-7-1']
month2015_7 = ['2015-7-{}'.format(i) for i in range(1, 32)] + ['2015-8-1']
month2015_8 = ['2015-8-{}'.format(i) for i in range(1, 32)] + ['2015-9-1']
month2015_9 = ['2015-9-{}'.format(i) for i in range(1, 31)] + ['2015-10-1']
month2015_10 = ['2015-10-{}'.format(i) for i in range(1, 32)] + ['2015-11-1']
month2015_11 = ['2015-11-{}'.format(i) for i in range(1, 31)] + ['2015-12-1']
month2015_12 = ['2015-12-{}'.format(i) for i in range(1, 32)] + ['2016-1-1']

month2016_1 = ['2016-1-{}'.format(i) for i in range(1, 32)] + ['2016-2-1']
month2016_2 = ['2016-2-{}'.format(i) for i in range(1, 30)] + ['2016-3-1']
month2016_3 = ['2016-3-{}'.format(i) for i in range(1, 32)] + ['2016-4-1']
month2016_4 = ['2016-4-{}'.format(i) for i in range(1, 31)] + ['2016-5-1']
month2016_5 = ['2016-5-{}'.format(i) for i in range(1, 32)] + ['2016-6-1']
month2016_6 = ['2016-6-{}'.format(i) for i in range(1, 31)] + ['2016-7-1']
month2016_7 = ['2016-7-{}'.format(i) for i in range(1, 32)] + ['2016-8-1']
month2016_8 = ['2016-8-{}'.format(i) for i in range(1, 32)] + ['2016-9-1']
month2016_9 = ['2016-9-{}'.format(i) for i in range(1, 31)] + ['2016-10-1']
month2016_10 = ['2016-10-{}'.format(i) for i in range(1, 32)] + ['2016-11-1']
month2016_11 = ['2016-11-{}'.format(i) for i in range(1, 31)] + ['2016-12-1']
month2016_12 = ['2016-12-{}'.format(i) for i in range(1, 32)] + ['2017-1-1']

month2017_1 = ['2017-1-{}'.format(i) for i in range(1, 32)] + ['2017-2-1']
month2017_2 = ['2017-2-{}'.format(i) for i in range(1, 29)] + ['2017-3-1']
month2017_3 = ['2017-3-{}'.format(i) for i in range(1, 32)] + ['2017-4-1']
month2017_4 = ['2017-4-{}'.format(i) for i in range(1, 31)] + ['2017-5-1']
month2017_5 = ['2017-5-{}'.format(i) for i in range(1, 32)] + ['2017-6-1']
month2017_6 = ['2017-6-{}'.format(i) for i in range(1, 31)] + ['2017-7-1']
month2017_7 = ['2017-7-{}'.format(i) for i in range(1, 32)] + ['2017-8-1']
month2017_8 = ['2017-8-{}'.format(i) for i in range(1, 32)] + ['2017-9-1']
month2017_9 = ['2017-9-{}'.format(i) for i in range(1, 31)] + ['2017-10-1']
month2017_10 = ['2017-10-{}'.format(i) for i in range(1, 32)] + ['2017-11-1']
month2017_11 = ['2017-11-{}'.format(i) for i in range(1, 31)] + ['2017-12-1']
month2017_12 = ['2017-12-{}'.format(i) for i in range(1, 32)] + ['2018-1-1']

month2018_1 = ['2018-1-{}'.format(i) for i in range(1, 32)] + ['2018-2-1']
month2018_2 = ['2018-2-{}'.format(i) for i in range(1, 29)] + ['2018-3-1']
month2018_3 = ['2018-3-{}'.format(i) for i in range(1, 32)] + ['2018-4-1']
month2018_4 = ['2018-4-{}'.format(i) for i in range(1, 31)] + ['2018-5-1']
month2018_5 = ['2018-5-{}'.format(i) for i in range(1, 32)] + ['2018-6-1']
month2018_6 = ['2018-6-{}'.format(i) for i in range(1, 31)] + ['2018-7-1']
month2018_7 = ['2018-7-{}'.format(i) for i in range(1, 32)] + ['2018-8-1']
month2018_8 = ['2018-8-{}'.format(i) for i in range(1, 32)] + ['2018-9-1']
month2018_9 = ['2018-9-{}'.format(i) for i in range(1, 31)] + ['2018-10-1']
month2018_10 = ['2018-10-{}'.format(i) for i in range(1, 32)] + ['2018-11-1']
month2018_11 = ['2018-11-{}'.format(i) for i in range(1, 31)] + ['2018-12-1']
month2018_12 = ['2018-12-{}'.format(i) for i in range(1, 32)] + ['2019-1-1']

month2019_1 = ['2019-1-{}'.format(i) for i in range(1, 32)] + ['2019-2-1']
month2019_2 = ['2019-2-{}'.format(i) for i in range(1, 29)] + ['2019-3-1']
month2019_3 = ['2019-3-{}'.format(i) for i in range(1, 32)] + ['2019-4-1']
month2019_4 = ['2019-4-{}'.format(i) for i in range(1, 31)] + ['2019-5-1']
month2019_5 = ['2019-5-{}'.format(i) for i in range(1, 32)] + ['2019-6-1']
