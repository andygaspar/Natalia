import numpy as np
import random

time_intervals = [i for i in range(0, 1441, 60)]


class DailyConfiguration:
    def __init__(self, day, df_open_acc, df_regulation_acc, df_delayed_acc,
                 df_airspace_capacity, df_actual_capacity, df_saturation, only_staffing):

        self.day = day
        self.onlyStaffing = only_staffing
        self.maxDelayed = 0
        self.sectorsOpen = self.get_sectors_open(time_intervals, df_open_acc)
        self.airspaceCapacity = df_airspace_capacity.capacity.iloc[0]
        self.actualCapacity = self.get_actual_capacity(time_intervals, df_actual_capacity)
        self.availableCapacity = self.actualCapacity - self.sectorsOpen
        self.inNeed, self.regulated = self.get_regulated(time_intervals, df_regulation_acc)
        self.delayedFlights = self.get_delayed(time_intervals, df_delayed_acc, df_regulation_acc)

        self.spareCapacity = self.make_spare(time_intervals, df_saturation)

        self.spareCapacity_dict = None

    @staticmethod
    def get_start_end_conditions(start_time, end_time, df):
        start_into = ((df.start >= start_time) & (df.start < end_time))
        end_into = ((df.end > start_time) & (df.end <= end_time))
        included = ((df.start < start_time) & (df.end >= end_time))
        df_int = df[start_into | end_into | included]

        return df_int

    def get_sectors_open(self, time_intervals, df_open_acc):
        return df_open_acc.n_sectors.to_numpy()

    def get_actual_capacity(self, time_intervals, df_actual_capacity):
        times = df_actual_capacity.iloc[0].to_numpy()
        return times[1:]

    def get_delayed(self, time_intervals, df_delayed_acc, df_regulation_acc):
        if self.onlyStaffing:
            df_in_need = df_regulation_acc[df_regulation_acc.Reason == 'ATC Staffing']
        else:
            df_in_need = df_regulation_acc[
                (df_regulation_acc.Reason == 'ATC Staffing') | (df_regulation_acc.Reason == "ATC Capacity")]
        delayed = {}
        for regulation in df_in_need.Regulation:
            df_del = df_delayed_acc[df_delayed_acc.Regulation == regulation]

            for i in range(len(time_intervals) - 1):
                delays = df_del[(time_intervals[i] <= df_del.regulation_time) & 
                                (df_del.regulation_time < time_intervals[i+1])]["Delay flight"]
                delayed[time_intervals[i]] = np.sort(delays)[::-1]

        return delayed

    def get_regulated(self, time_intervals, df_regulation_acc):
        in_need = np.zeros(len(time_intervals) - 1, dtype=bool)
        regulated = np.zeros(len(time_intervals) - 1, dtype=bool)
        if df_regulation_acc.shape[0] > 0:
            if self.onlyStaffing:
                df_in_need = df_regulation_acc[df_regulation_acc.Reason == 'ATC Staffing']
            else:
                df_in_need = df_regulation_acc[
                    (df_regulation_acc.Reason == 'ATC Staffing') | (df_regulation_acc.Reason == "ATC Capacity")]
            for i in range(in_need.shape[0]):
                df_reg = self.get_start_end_conditions(time_intervals[i], time_intervals[i + 1], df_regulation_acc)
                regulated[i] = True if df_reg.shape[0] > 0 else False

                df_staff = self.get_start_end_conditions(time_intervals[i], time_intervals[i + 1], df_in_need)
                in_need[i] = True if df_staff.shape[0] > 0 else False

            # TO DO check airspace capacity

        return in_need, regulated

    def make_spare(self, time_intervals, df_saturation):
        spare_capacity = np.zeros(len(time_intervals) - 1, dtype=int)
        for i in range(spare_capacity.shape[0]):
            if not self.regulated[i]:
                spare_capacity[i] = df_saturation[df_saturation.start == time_intervals[i]].n_sectors.iloc[0] \
                                    + self.availableCapacity[i]

        return spare_capacity

    def __repr__(self):
        return self.day


class Acc:

    def __init__(self, index, name, days, df_open_acc, df_regulation_acc, df_delayed_acc,
                 df_airspace_capacity, df_actual_capacity, df_saturation, df_sector_capacity, only_staffing=False):

        self.name = name
        self.index = index
        self.sector_capacity = df_sector_capacity.sector_capacity.iloc[0]
        self.days = {}
        if self.name == "EGCC":
            print(self.name)
        for day in days:
            df_d_day, df_r_day, df_o_day, df_s_day = self.get_day_df(day, df_delayed_acc, df_regulation_acc,
                                                                     df_open_acc, df_saturation)
            self.days[day] = DailyConfiguration(day, df_o_day, df_r_day, df_d_day, df_airspace_capacity,
                                                df_actual_capacity, df_s_day, only_staffing)

    def get_day_df(self, d, df_delayed, df_regulation, df_open, df_saturation):
        df_d_d = df_delayed[df_delayed.Date == d]
        df_r_d = df_regulation[df_regulation.Date == d]
        df_o_d = df_open[df_open.date == d]
        df_s_d = df_saturation[df_saturation.date == d]

        return df_d_d, df_r_d, df_o_d, df_s_d

    def __repr__(self):
        return self.name
