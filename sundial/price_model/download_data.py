import os
import numpy as np
import utils

NODE_LOCATION = 'STMARIA_7_N101'

start_times = ['20160915', '20160829', '20160927', '20161026', '20161124']
end_times = ['20160928', '20160927', '20161026', '20161124', '20161222']

xml_fn = []
for (s_time, e_time) in zip(start_times, end_times):
    URL = 'http://oasis.caiso.com/oasisapi/SingleZip?queryname=' +\
        'PRC_LMP&startdatetime=' + s_time + 'T07:00-0000&enddatetime=' +\
        e_time + 'T07:00-0000&version=1&market_run_id=DAM&node=' + \
        NODE_LOCATION

    fn = utils.get_data(URL, 'zip')
    xml_fn.append(fn)
    break
