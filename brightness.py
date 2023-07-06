import cv2
import numpy as np
import ctypes
import wmi


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


def main():
    # Open the camera
    camera = cv2.VideoCapture(0)

    while True:
        # Capture a frame from the camera
        ret, frame = camera.read()

        # Calculate the brightness of the captured image
        brightness = calculate_brightness(frame)

        # Adjust the display brightness based on the image brightness
        set_display_brightness(brightness)

        # Show the frame in a window
        cv2.imshow("Camera", frame)

        # Exit the loop when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close the window
    camera.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
