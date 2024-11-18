import time
import numpy as np
import pyautogui
import pytesseract
import matplotlib.pyplot as plt
import threading
from matplotlib.patches import Rectangle
from sentiment_analysis import analyze_sentiment  # Import your sentiment analysis function

# Define global variables for screen selection
start_point = None
end_point = None
selection_done = False
recording = False
display_callback = None

def reset_selection():
    global start_point, end_point, selection_done
    start_point = None
    end_point = None
    selection_done = False

def select_screen_area():
    global start_point, end_point, selection_done
    selection_done = False  # Reset flag

    # Capture the entire screen for display
    screenshot = pyautogui.screenshot()
    screenshot = np.array(screenshot)

    # Create a figure and axes for Matplotlib
    fig, ax = plt.subplots()
    ax.imshow(screenshot)
    rect = Rectangle((0, 0), 1, 1, fill=False, edgecolor="red", linewidth=2)
    ax.add_patch(rect)

    # Callback for mouse events
    def on_mouse_press(event):
        global start_point
        start_point = (event.xdata, event.ydata)
        print(f"Mouse pressed at: {start_point}")  # Debug

    def on_mouse_move(event):
        global end_point
        if start_point is not None:
            end_point = (event.xdata, event.ydata)
            width = abs(end_point[0] - start_point[0])
            height = abs(end_point[1] - start_point[1])
            rect.set_width(width)
            rect.set_height(height)
            rect.set_xy((min(start_point[0], end_point[0]), min(start_point[1], end_point[1])))
            plt.draw()

    def on_mouse_release(event):
        global selection_done
        end_point = (event.xdata, event.ydata)
        selection_done = True
        print(f"Mouse released at: {end_point}")  # Debug
        plt.close()

    fig.canvas.mpl_connect("button_press_event", on_mouse_press)
    fig.canvas.mpl_connect("motion_notify_event", on_mouse_move)
    fig.canvas.mpl_connect("button_release_event", on_mouse_release)
    
    plt.title("Select Area for Screen Recording (Drag to select)")
    plt.show()

    if selection_done and start_point and end_point:
        x1, y1 = map(int, start_point)
        x2, y2 = map(int, end_point)
        width, height = x2 - x1, y2 - y1
        print(f"Selected region: {x1, y1, width, height}")  # Debug
        return x1, y1, width, height
    else:
        print("Selection canceled or incomplete.")
        return None

def run_screen_recording(x, y, width, height, callback):
    global recording
    print("Screen recording started...")
    recording = True
    
    while recording:
        screenshot = pyautogui.screenshot(region=(x, y, width, height))
        screenshot.save("chat_screenshot.png")
        
        # Perform OCR and analyze sentiment
        text = pytesseract.image_to_string("chat_screenshot.png")
        print(f"Extracted text: {text}")  # Debug
        sentiment = analyze_sentiment(text)
        print(f"Sentiment: {sentiment}")  # Debug
        if callback:
            callback(sentiment)
        
        time.sleep(2)  # Reduce interval between checks for faster updates

def start_screen_recording():
    global recording, display_callback
    if not recording:
        # Reset selection before starting a new recording session
        reset_selection()
        # Select screen area in the main thread
        region = select_screen_area()
        if region is not None:
            x, y, width, height = region
            # Start the recording in a separate thread
            recording_thread = threading.Thread(target=run_screen_recording, args=(x, y, width, height, display_callback))
            recording_thread.start()

def stop_screen_recording():
    global recording
    recording = False
    print("Screen recording stopped.")

def set_display_callback(callback):
    global display_callback
    display_callback = callback
