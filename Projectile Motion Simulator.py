import matplotlib.pyplot as plt
from tkinter import *
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from tkinter import messagebox

# Constants
g = 9.81  # Acceleration due to gravity (m/s^2)
time_step = 0.01 # Time step to calulcate new motion equations

# Function to simulate projectile motion
def simulate_projectile_motion(initial_velocity, launch_angle, time_step):
    x = []
    y = []

    # Convert launch angle to radians
    launch_angle_rad = np.deg2rad(launch_angle)

    # Initial conditions
    x.append(0)
    y.append(0)

    # Initial horizontal and vertical velocities
    vx = initial_velocity * np.cos(launch_angle_rad)
    vy = initial_velocity * np.sin(launch_angle_rad)

    # Simulation loop
    while y[-1] >= 0:
        # Update position
        x.append(x[-1] + vx * time_step)
        y.append(y[-1] + vy * time_step)

        # Update velocities
        vy -= g * time_step

    return x, y

# Function to update the plot based on user input
def update_plot():
    initial_velocity = float(velocity_entry.get())
    launch_angle = float(angle_entry.get())
    
    #Check that the inital velocity is greater than 0

    if initial_velocity < 0.1 :
        messagebox.showerror("Invalid Inital Velocity", "Inital velocity must be greater than 0.1m/s.")
        return # Do not update plot if the inital velocity is invalid
    
    # Check if the launch angle is within the valid range
    if launch_angle < 1 or launch_angle > 89:
        messagebox.showerror("Invalid Launch Angle", "Launch angle must be between 1 and 89 degrees.")
        return  # Do not update the plot if the angle is invalid

    x, y = simulate_projectile_motion(initial_velocity, launch_angle, time_step)

    x_limit = x_limit_slider.get()  # Get the x limit from the slider
    y_limit = y_limit_slider.get()  # Get the y limit from the slider

    ax.clear()
    ax.plot(x, y,'k',label='Trajectory')
    ax.set_title('Projectile Motion')
    ax.set_xlabel('Horizontal Distance (m)')
    ax.set_ylabel('Vertical Distance (m)')
    ax.grid()
    ax.set_facecolor('seagreen')
    ax.legend()
    ax.set_xlim(0, x_limit)  # Set x limit
    ax.set_ylim(0, y_limit)  # Set y limit

    canvas.draw()

# Create the main application window
root = Tk()
root.title("Projectile Motion Simulation")

# Configure the rows and columns to expand when the window is resized
root.columnconfigure(0, weight=1)
root.rowconfigure(1, weight=1)

# Create and configure the main frame
main_frame = ttk.Frame(root)
main_frame.grid(row=0, column=0, sticky="nsew")

# Create and configure the input fields and labels
style = ttk.Style()
style.configure("TButton", font=("Arial", 18))  # Set the button font and size
style.configure("TLabel", font=("Arial", 18))   # Set the label font and size

velocity_label = ttk.Label(main_frame, text="Initial Velocity (m/s):")
velocity_label.grid(row=0, column=0, padx=10, pady=10)
velocity_entry = ttk.Entry(main_frame,font=("Arial", 18),width=20)
velocity_entry.grid(row=0, column=1, padx=10, pady=10)
velocity_entry.insert(0, "20.0")

angle_label = ttk.Label(main_frame, text="Launch Angle (degrees):")
angle_label.grid(row=1, column=0, padx=10, pady=10)
angle_entry = ttk.Entry(main_frame,font=("Arial", 18),width=20)
angle_entry.grid(row=1, column=1, padx=10, pady=10)
angle_entry.insert(0, "45.0")


# Create sliders for x and y limits
x_limit_label = ttk.Label(main_frame, text="X Limit:")
x_limit_label.grid(row=2, column=0, padx=0, pady=10)
x_limit_slider = Scale(main_frame, from_=10, to=1000, resolution=1, orient=HORIZONTAL,length=300)
x_limit_slider.grid(row=2, column=1, padx=0, pady=10)
x_limit_slider.set(50.0)  # Initial x limit value

y_limit_label = ttk.Label(main_frame, text="Y Limit:")
y_limit_label.grid(row=3, column=0, padx=0, pady=10)
y_limit_slider = Scale(main_frame, from_=10, to=1000, resolution=1, orient=HORIZONTAL,length=300)
y_limit_slider.grid(row=3, column=1, padx=0, pady=10)
y_limit_slider.set(30.0)  # Initial y limit value

# Create a button to update the plot
update_button = ttk.Button(main_frame, text="Update Plot", command=update_plot)
update_button.grid(row=4, columnspan=2, padx=10, pady=10)

# Create a Matplotlib figure
fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.grid(row=1, column=0, sticky="nsew")

# Initialize the plot
update_plot()

# Start the GUI application
root.mainloop()
