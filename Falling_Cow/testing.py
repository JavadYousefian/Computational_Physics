import math, matplotlib
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

vx = 1
vy = 100
drag = 0
x0 = 0
y0 = 1000
time_step = 0.001
time = []
position_x = []
position_y = []

#num_points = len(y_values)

# t = [i * time_step for i in range(num_points)] 
#or
# t = np.arange(0, end_time, time_step), where end_time is where we know time stops (when y = 0)

def force(mass, acce):
    F = mass * acce
    acce = F / mass
    return F, acce

#calculate force fromm its position and current velocity

def updated_position(t0, t, y0, v0):
    y = y0 + v0 * (t-t0)
#y_ = y_0 + v_{y0}\delta t

#V_y = V_(y,0) - g\Delta try

def updated_velocity(v0,tf,ti):
    new_vel = v0 - g*(tf-ti)
    return new_vel

def plot_the_cow():


'For F_net = ma, we can let dy/dt = -v, and dv/dt = g - D/m v^2 '
'm = 4/3 \pi R^3'
''

def generate_plots(self):
        read_header = read_header_file(run_number) #call a function
        samp = int(read_header[0]['sample_interval']) #then define one of the returns of that function
        print('samp', samp)
        print('sensor names',sensors)
        global sensor_data
    

        for line, column in zip(sensors,stored_data): #this has to be for position x and position y
        #for line in read_header[2]:         
            # Create a plot in the tab
            figure = plt.Figure()
            ax = figure.add_subplot(111)
            global x
            #ax.plot(x_values,column) #read_header[0]['sample_interval]
            x = [] #This is how we're multiplying our x-values in the plot with the sample interval
            for i in range(0,len(column)):
                x_values=i * samp
                x.append(x_values)
            ax.plot(x,column)
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_ylim(min(column)* 0.9, max(column) * 1.1) 
            ax.set_title('Plot for {}'.format(tab_name))
            canvas.show()
         