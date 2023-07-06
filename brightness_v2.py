import cv2
import numpy as np
import ctypes
import wmi
import schedule
import time


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
    # Open the camera
    camera = cv2.VideoCapture(0)

    # Capture a frame from the camera
    ret, frame = camera.read()

    # Calculate the brightness of the captured image
    brightness = calculate_brightness(frame)

    # Adjust the display brightness based on the image brightness
    set_display_brightness(brightness)

    # Release the camera
    camera.release()


def main():
    # Schedule the job to run every 30 minutes
    schedule.every(0.1).minutes.do(capture_and_adjust_brightness)

    while True:
        # Run any pending scheduled jobs
        schedule.run_pending()

        # Delay for a while before checking the schedule again
        time.sleep(1)


if __name__ == '__main__':
    main()
