import numpy as np
import random

time_intervals = [i for i in range(0, 1441, 60)]
num_intervals = len(time_intervals) - 1


class DailyConfiguration:
    def __init__(self, day, df_open_acc, df_regulation_acc, df_delayed_acc,
                 df_airspace_capacity, df_actual_capacity, df_saturation, only_staffing):

        self.day = day
        self.onlyStaffing = only_staffing
        self.maxDelayed = 0
        self.sectorsOpen = self.get_sectors_open(df_open_acc)
        self.airspaceCapacity = df_airspace_capacity.capacity.iloc[0]
        self.actualCapacity = self.get_actual_capacity(df_actual_capacity)
        self.availableCapacity = self.set_available()
        self.inNeed, self.regulated = self.get_regulated(df_regulation_acc)
        self.delayedFlights = self.get_delayed(df_delayed_acc, df_regulation_acc)
        self.delays = self.compute_delay()

        self.totalDailyDelay = np.sum(self.delays)

        self.spareCapacity = self.make_spare(df_saturation)

        self.spareCapacity_dict = None

    @staticmethod
    def get_start_end_conditions(start_time, end_time, df):
        start_into = ((df.start >= start_time) & (df.start < end_time))
        end_into = ((df.end > start_time) & (df.end <= end_time))
        included = ((df.start < start_time) & (df.end >= end_time))
        df_int = df[start_into | end_into | included]

        return df_int

    @staticmethod
    def get_sectors_open(df_open_acc):
        return df_open_acc.n_sectors.to_numpy()

    @staticmethod
    def get_actual_capacity(df_actual_capacity):
        times = df_actual_capacity.iloc[0].to_numpy()
        return times[1:]

    def set_available(self):
        available = self.actualCapacity - self.sectorsOpen
        available[available < 0] = 0
        return available

    def get_delayed(self, df_delayed_acc, df_regulation_acc):
        if self.onlyStaffing:
            df_in_need = df_regulation_acc[df_regulation_acc.Reason == 'ATC Staffing']
        else:
            df_in_need = df_regulation_acc[
                (df_regulation_acc.Reason == 'ATC Staffing') | (df_regulation_acc.Reason == "ATC Capacity")]
        delayed = [np.array([]) for _ in range(num_intervals)]
        delayed_dict = {}
        for regulation in df_in_need.Regulation:
            df_del = df_delayed_acc[df_delayed_acc.Regulation == regulation]

            for i in range(num_intervals):
                delays = df_del[(time_intervals[i] <= df_del.regulation_time) &
                                (df_del.regulation_time < time_intervals[i + 1])]["Delay flight"]
                delayed[i] = np.append(delayed[i], delays)

        for i in range(num_intervals):
            delayed[i] = np.sort(delayed[i])[::-1]
            delayed_dict[i] = delayed[i]

        return delayed

    def get_regulated(self, df_regulation_acc):
        in_need = np.zeros(num_intervals, dtype=bool)
        regulated = np.zeros(num_intervals, dtype=bool)
        if df_regulation_acc.shape[0] > 0:
            if self.onlyStaffing:
                df_in_need = df_regulation_acc[df_regulation_acc.Reason == 'ATC Staffing']
            else:
                df_in_need = df_regulation_acc[
                    (df_regulation_acc.Reason == 'ATC Staffing') | (df_regulation_acc.Reason == "ATC Capacity")]
            for i in range(in_need.shape[0]):
                df_reg = self.get_start_end_conditions(time_intervals[i], time_intervals[i + 1], df_regulation_acc)
                if not regulated[i]:
                    regulated[i] = True if df_reg.shape[0] > 0 else False

                df_staff = self.get_start_end_conditions(time_intervals[i], time_intervals[i + 1], df_in_need)
                if not in_need[i]:
                    in_need[i] = True if df_staff.shape[0] > 0 and self.sectorsOpen[i] < self.airspaceCapacity \
                        else False

        return in_need, regulated

    def make_spare(self, df_saturation):
        spare_capacity = np.zeros(num_intervals, dtype=int)
        for i in range(spare_capacity.shape[0]):
            if not self.regulated[i]:
                spare_capacity[i] = df_saturation[df_saturation.start == time_intervals[i]].n_sectors.iloc[0] \
                                    + self.availableCapacity[i]

        return spare_capacity

    def __repr__(self):
        return self.day

    def compute_delay(self):
        delays = np.zeros(num_intervals)
        for i in range(num_intervals):
            delays[i] = sum(self.delayedFlights[i])

        return delays


class Acc:

    def __init__(self, index, name, days, df_open_acc, df_regulation_acc, df_delayed_acc,
                 df_airspace_capacity, df_actual_capacity, df_saturation, df_sector_capacity, only_staffing=False):
        self.name = name
        self.index = index
        self.sector_capacity = df_sector_capacity.sector_capacity.iloc[0]
        self.days = []
        self.days_dict = {}
        for day in days:
            df_d_day, df_r_day, df_o_day, df_s_day = self.get_day_df(day, df_delayed_acc, df_regulation_acc,
                                                                     df_open_acc, df_saturation)
            daily_config = DailyConfiguration(day, df_o_day, df_r_day, df_d_day, df_airspace_capacity,
                                              df_actual_capacity, df_s_day, only_staffing)
            self.days.append(daily_config)

            self.days_dict[day] = daily_config

        self.totalDelay = sum([day.totalDailyDelay for day in self.days])

    @staticmethod
    def get_day_df(d, df_delayed, df_regulation, df_open, df_saturation):
        df_d_d = df_delayed[df_delayed.Date == d]
        df_r_d = df_regulation[df_regulation.Date == d]
        df_o_d = df_open[df_open.date == d]
        df_s_d = df_saturation[df_saturation.date == d]

        return df_d_d, df_r_d, df_o_d, df_s_d

    def __repr__(self):
        return self.name
