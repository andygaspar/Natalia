import numpy as np
import random


class Acc:
    def __init__(self, index, name, interval_size, time_intervals, df_open_acc, df_regulation_acc, df_delayed_acc,
                 df_max_config, sector_capacity=30, only_staffing=False):

        self.index = index
        self.name = name
        self.onlyStaffing = only_staffing
        self.maxDelayed = 0
        self.sectorsOpen = self.get_sectors_open(time_intervals, df_open_acc)
        self.max_config = df_max_config.iloc[0].max_sectors
        self.availableCapacity = self.max_config - self.sectorsOpen
        self.actualCapacity = self.get_actual_capacity(time_intervals)
        self.inNeed, self.regulated = self.get_regulated(time_intervals, df_regulation_acc)
        self.delayedFlights = self.get_delayed(time_intervals, df_delayed_acc, df_regulation_acc)

        self.sector_capacity = round(interval_size * sector_capacity / 60)
        self.spareCapacity = self.make_spare(time_intervals)

    @staticmethod
    def get_start_end_conditions(start_time, end_time, df):
        start_into = ((df.start >= start_time) & (df.start < end_time))
        end_into = ((df.end > start_time) & (df.end <= end_time))
        included = ((df.start < start_time) & (df.end >= end_time))
        df_int = df[start_into | end_into | included]

        return df_int

    def get_sectors_open(self, time_intervals, df_open_acc):
        opens = np.zeros(len(time_intervals) - 1, dtype=int)
        for i in range(opens.shape[0]):
            df_int = self.get_start_end_conditions(time_intervals[i], time_intervals[i + 1], df_open_acc)
            busiest_configs = [max(df_int[df_int.acc == acc].n_sectors) for acc in df_int.acc.unique()]
            opens[i] = sum(busiest_configs)

        return opens

    def get_actual_capacity(self, time_intervals):
        actual_capacity = np.zeros(len(time_intervals) - 1)
        for i in range(actual_capacity.shape[0]):
            if self.sectorsOpen[i] < self.max_config:
                actual_capacity[i] = random.choice(range(self.sectorsOpen[i], self.max_config + 1))
            else:
                actual_capacity[i] = self.max_config

        return actual_capacity

    def get_delayed(self, time_intervals, df_delayed_acc, df_regulation_acc):
        if self.onlyStaffing:
            df_in_need = df_regulation_acc[df_regulation_acc.Reason == 'ATC Staffing']
        else:
            df_in_need = df_regulation_acc[
                (df_regulation_acc.Reason == 'ATC Staffing') | (df_regulation_acc.Reason == "ATC Capacity")]
        delays = np.zeros(len(time_intervals) - 1, dtype=int)
        for regulation in df_in_need.Regulation:
            df_staff = df_in_need[df_in_need.Regulation == regulation]
            df_del = df_delayed_acc[df_delayed_acc.MPR == regulation]
            delays_reg = df_del["Total Delay"].sort_values(ascending=False).to_numpy()
            start = df_staff.iloc[0].start
            end = df_staff.iloc[0].end
            delayed_time = np.array([start + (end - start) * i / delays_reg.shape[0]
                                     for i in range(delays_reg.shape[0])])
            num_delayed_per_interval = np.array([
                delays_reg[np.where((time_intervals[i] <= delayed_time)
                                    & (delayed_time < time_intervals[i + 1]))].shape[0]
                for i in range(len(time_intervals) - 1)])
            if max(num_delayed_per_interval) > self.maxDelayed:
                self.maxDelayed = max(num_delayed_per_interval)
            delays_per_interval = np.array([
                sum(delays_reg[np.where((time_intervals[i] <= delayed_time) & (delayed_time < time_intervals[i + 1]))])
                for i in range(len(time_intervals) - 1)])
            delays += delays_per_interval

        return delays

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

    def make_spare(self, time_intervals):
        spare_capacity = np.zeros(len(time_intervals) - 1, dtype=int)
        for i in range(spare_capacity.shape[0]):
            if not self.regulated[i]:
                spare_capacity[i] = self.max_config - self.sectorsOpen[i]

        return spare_capacity

    def __repr__(self):
        return self.name
