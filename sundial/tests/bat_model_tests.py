import sys
import unittest
import numpy as np
sys.path.append('/Users/ryanstoddard/Documents/UW/CSE_586/Project/SunDial')
sys.path.append('/Users/ryanstoddard/Documents/UW/CSE_586/'
                'Project/SunDial/sundail')
sys.path.append('/Users/ryanstoddard/Documents/UW/CSE_586/'
                'Project/SunDial/sundail/data')
from sundial import battery_model


class UtilsTest(unittest.TestCase):

    def test_smoke(self):
        soc = 50
        temp = 20
        days = 100
        battery_model.bat_shelf(soc, temp, days)

    def test_smoke2(self):
        cycles = 200
        soc_low = 20
        soc_high = 80
        rate = 1
        battery_model.bat_cycle(cycles, soc_low, soc_high, rate)

    def test_smoke3(self):
        cycles = 200
        soc_low = 20
        soc_high = 80
        rate = 1
        soc = 50
        temp = 20
        battery_model.bat_day(soc, temp, cycles, soc_low,
                              soc_high, rate)

    def test_smoke4(self):
        usage_kWhr = 8
        t_start = 18
        t_final = 22
        date = 343
        cap_kWhr = 100
        cost_mult = 10*cap_kWhr
        battery_model.bat_price_per_hour(usage_kWhr, t_start,
                                         t_final, date, cap_kWhr,
                                         cost_mult)

    def test_value(self):
        usage_kWhr = 8
        t_start = 18
        t_final = 22
        date = 343
        cap_kWhr = 100
        cost_mult = 10*cap_kWhr
        a = battery_model.bat_price_per_hour(usage_kWhr, t_start,
                                             t_final, date, cap_kWhr,
                                             cost_mult)
        self.assertTrue(np.sum(a) > 0)

    def test_useage(self):
        usage_kWhr = 8
        t_start = 18
        t_final = 22
        date = 343
        cap_kWhr = 100
        cost_mult = 10*cap_kWhr
        a1 = battery_model.bat_price_per_hour(usage_kWhr, t_start,
                                              t_final, date,
                                              cap_kWhr, cost_mult)
        usage_kWhr = 100
        a2 = battery_model.bat_price_per_hour(usage_kWhr, t_start, t_final,
                                              date, cap_kWhr, cost_mult)

        self.assertTrue(np.sum(a2) > np.sum(a1))


if __name__ == '__main__':
    unittest.main()
