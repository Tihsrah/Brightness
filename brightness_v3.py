import cv2
import numpy as np
import ctypes
import wmi
import schedule
import time
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import threading
import sys


def calculate_brightness(image):
    # Convert the image to grayscale
    grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Calculate the average pixel value
    brightness = np.mean(grayscale_image)

    return brightness


def set_display_brightness(brightness):
    # Use the WMI library to access the Windows brightness settings
    wmi_namespace = "wmi"
    brightness_class = "WmiMonitorBrightnessMethods"
    wmi_obj = wmi.WMI(namespace=wmi_namespace).WmiMonitorBrightnessMethods()[0]

    # Set the brightness (0-100)
    wmi_obj.WmiSetBrightness(int(brightness), 0)


def capture_and_adjust_brightness():
    try:
        # Open the camera
        camera = cv2.VideoCapture(0)

        # Check if the camera is opened successfully
        if not camera.isOpened():
            raise Exception("Failed to open camera")

        # Capture a frame from the camera
        ret, frame = camera.read()

        # Check if the frame is captured successfully
        if not ret:
            raise Exception("Failed to capture frame")

        # Calculate the brightness of the captured image
        brightness = calculate_brightness(frame)

        # Get the maximum brightness value from the scroll wheel
        max_brightness = brightness_scale.get()

        # Adjust the display brightness based on the image brightness and maximum brightness value
        set_display_brightness(brightness * (max_brightness / 100))

        # Release the camera
        camera.release()

    except Exception as e:
        # Handle the exception gracefully (print error message, log, etc.)
        pass


def quit_application():
    # Display a confirmation dialog before quitting
    answer = messagebox.askyesno("Quit", "Are you sure you want to quit?")
    if answer:
        # Stop the main program loop
        schedule.clear()

        # Close the GUI
        root.destroy()

        # Exit the entire program
        sys.exit()


def gui_thread():
    # Create the main application window
    global root
    root = tk.Tk()
    root.title("Brightness Adjuster")
    root.geometry("300x120")
    root.protocol("WM_DELETE_WINDOW", quit_application)
    # Replace 'path_to_favicon.ico' with the actual path to your favicon file
    root.iconbitmap(
        r'C:\Users\harsh\OneDrive - UPES\Desktop\d_drive\Projects\brightness\logo_v3.ico')

    # Set the application style
    style = ttk.Style()
    style.theme_use('clam')  # Choose a different theme if desired

    # Configure the scroll wheel style
    style.configure("TScale", troughcolor="gray70", sliderthickness=10)

    # Create a scroll wheel to set the maximum brightness
    brightness_label = tk.Label(
        root, text="Maximum Brightness:", font=('Arial', 12))
    brightness_label.pack(pady=10)

    global brightness_scale
    brightness_scale = ttk.Scale(
        root, from_=0, to=100, length=200, orient=tk.HORIZONTAL, style="TScale")
    brightness_scale.set(100)  # Set the initial maximum brightness to 100%
    brightness_scale.pack()

    # Create a quit button
    quit_button = tk.Button(root, text="Quit", command=quit_application, font=(
        'Arial', 12), fg='white', bg='red')
    quit_button.pack(pady=10)

    # Start the GUI main
    # Start the GUI main loop
    root.mainloop()


def main():
    # Schedule the job to run every 0.1 minutes
    schedule.every(15).minutes.do(capture_and_adjust_brightness)

    while True:
        # Run any pending scheduled jobs
        schedule.run_pending()

        # Delay for a while before checking the schedule again
        time.sleep(1)
        # Check if the main program loop should exit
        if not gui_thread.is_alive():
            break


if __name__ == '__main__':
    # Create a separate thread for the GUI
    gui_thread = threading.Thread(target=gui_thread)
    # Set the GUI thread as a daemon so it terminates when the main program exits
    gui_thread.daemon = True
    gui_thread.start()

    # Run the main program loop
    main()
