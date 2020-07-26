#Sinusoidal function sampling - SoFi 2020

import math
import numpy as np
import matplotlib.pyplot as plt

#Sinusoidal equation (to describe the fish heading)
alpha = 2.0         
offset = 0
omega = 4.0
period = (2*math.pi/omega)
def sin_func(t):
    return alpha * math.sin(omega*t) + offset
def sin_func_slanted(t):
    return alpha * math.sin(omega*t) + offset + t
def sin_func_curved(t):
    return alpha * math.sin(omega*t) + offset + t**2

#All x axis and y axis points
time = np.arange(0, 50, 0.1)
amplitude = [sin_func_curved(t) for t in time]
samples = []

#Do the sampling in multiple ways
#Average the heading over a period
time2 = []
average_list = []
count = 1
for x in range(0, len(amplitude), 1):       #10 samples per second
    time_step = float(x) / 10.0
    if time_step >= (period * count) and x != 0:
        average = sum(average_list)/len(average_list)
        samples.append(average)
        time2.append(time_step)
        
        average_list = []
        count += 1
    else:
        average_list.append(amplitude[x]) 

#Use a moving average?

#Plot the results
plt.title('Straight Forward Fish Travel (bias of 5, no offset)')
plt.plot(time, amplitude, color='blue', label='Fish heading')
plt.plot(time2, samples, color='red', label='periodic averaging')

print time2
print samples
print(2*math.pi/omega)

plt.show()