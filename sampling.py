#Sinusoidal function sampling - SoFi 2020

import math
import numpy as np
import matplotlib.pyplot as plt
from queue import Queue

#Sinusoidal equation (to describe the fish heading)
class HeadingAveraging():
    def __init__(self, function='default', method='binning1', alpha=2.0, offset=0, omega=1.0, offset_2=0, omega_2=5.0):
        """
        function values: default; slanted; curved; special
        method values: binning1 (default); binning2; running; moving
        """
        self.function = function
        self.method = method

        #sin function parameters
        self.alpha = alpha     
        self.offset = offset
        self.omega = omega
        self.omega_2 = omega_2
        self.offset_2 = offset_2
        self.period = (2*math.pi/omega)

        #All x (time) and y (horizontal fish position) values
        self.time = np.arange(0, 150, 0.1)
        self.amplitude = self.create_data_points()
        

    #Various sin functions to test averaging on
    def sin_func(self, t):
        return self.alpha * math.sin(self.omega*t) + self.offset
    def sin_func_slanted(self, t):
        return self.alpha * math.sin(self.omega*t) + self.offset + t
    def sin_func_curved(self, t):
        return self.alpha * math.sin(self.omega*t) + self.offset + t**2
    def sin_func_special(self, t):
        return (self.alpha * math.sin(self.omega*t) + self.offset) + (math.sin(self.omega_2 * t) + self.offset_2)
    def create_data_points(self):
        amplitude = []
        if self.function == 'slanted':
            amplitude = [self.sin_func_slanted(t) for t in self.time]
        elif self.function == 'curved':
            amplitude = [self.sin_func_curved(t) for t in self.time]
        elif self.function == 'special':
            amplitude = [self.sin_func_special(t) for t in self.time]
        else:
            amplitude = [self.sin_func(t) for t in self.time]
        return amplitude

    #Do the sampling in multiple ways
    ##########################
    #PERIODIC BINNING AVERAGE#
    ##########################
    def run_binning_average_1(self):
        samples = []
        sample_times = []
        avg_bin = []
        count = 1
        for x in range(len(self.amplitude)):       #10 samples per second
            time_step = float(x) / 10.0
            if time_step >= (self.period * count) and x != 0:
                average = sum(avg_bin)/len(avg_bin)
                samples.append(average)
                sample_times.append(time_step)
                avg_bin = []
                count += 1
            else:
                avg_bin.append(self.amplitude[x]) 
        return sample_times, samples

    ####################
    #BINNING AVERAGE V2#
    ####################
    def run_binning_average_2(self):
        samples = []
        sample_times = []
        avg_bin = []
        current_point = 0
        last_point = 0
        current_slope = 0       #-1, 0, 1 for negative slope, zero slope, positive slope
        for x in range(len(self.amplitude)):
            time_step = float(x) / 10.0
            #update every parameter
            last_point = current_point
            current_point = self.amplitude[x]
            new_slope = (current_point - last_point) / 0.1
            if new_slope != 0:
                new_slope = new_slope / abs(new_slope)
            # if current_slope == -1:
            #     if new_slope >= 0:
            #         average = sum(avg_bin) / len(avg_bin)
            #         samples.append(average)
            #         sample_times.append(time_step)
            #         avg_bin = []
            if current_slope == 1:
                if new_slope <= 0:
                    average = sum(avg_bin) / len(avg_bin)
                    samples.append(average)
                    sample_times.append(time_step)
                    avg_bin = []
            avg_bin.append(current_point)
            current_slope = new_slope
        return sample_times, samples
     
    #################
    #RUNNING AVERAGE#
    #################
    def run_running_average(self):
        current_sum = 0.0
        count = 0.0
        samples = []
        for i in range(len(self.amplitude)):
            current_sum += amplitude[i]
            count += 1.0
            average = current_sum / count
            samples.append(average)
        return self.time, samples 


    #######################
    #MOVING WINDOW AVERAGE#
    #######################
    def run_moving_average(self):
        window_size = self.period * 10
        window  = []
        samples = []
        for i in range(len(self.amplitude)):
            if len(window) >= window_size:
                window.pop(0)
            window.append(self.amplitude[i])
            average = sum(window) / len(window)
            samples.append(average)
            #print(window)
        return self.time, samples

    def run(self):
        sample_times = []
        samples = []
        if self.method == 'binning2':
            sample_times, samples = self.run_binning_average_2()
        elif self.method == 'running':
            sample_times, samples = self.run_running_average()
        elif self.method == 'moving':
            sample_times, samples = self.run_moving_average()
        else:
            sample_times, samples = self.run_binning_average_1()
        return self.time, self.amplitude, sample_times, samples

if __name__ == '__main__':
    """
    function values: default; slanted; curved; special
    method values: binning1 (default); binning2; running; moving
    """    
    experiment = HeadingAveraging(function='slanted', method='moving')
    time, amplitude, sample_times, samples = experiment.run()
    # sample_times_2, samples_2 = experiment.run_binning_average_2()
    # sample_times_3, samples_3 = experiment.run_running_average()
    # sample_times_4, samples_4 = experiment.run_moving_average()
    #Plot the results
    plt.title('Title')
    plt.plot(time, amplitude, color='blue', label='Fish heading')
    plt.plot(sample_times, samples, color='red', label='averaging results')
    plt.show()
    print("DONE!")

#print time2
#print samples
#print(2*math.pi/omega)