import cv2
import numpy as np
import pyautogui
import os
import time
from skimage.metrics import structural_similarity as ssim
import threading

class SubtitleDetector:
    def __init__(self, output_dir='output_frames'):
        self.output_dir = output_dir
        self.subtitle_count = 0
        self.prev_frame = None

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def select_subtitle_region(self):
        print("Select the subtitle region by dragging a rectangle with the mouse.")
        img = pyautogui.screenshot()
        cv2.namedWindow("Select Subtitle Region", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("Select Subtitle Region", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        region = cv2.selectROI("Select Subtitle Region", np.array(img))
        cv2.destroyAllWindows()

        if region[2] == 0 or region[3] == 0:
            raise ValueError("Invalid region selected. Please select a valid region.")
        
        print("Selected region:", region)
        return region

    def get_screen_region(self, region):
        try:
            screenshot = pyautogui.screenshot(region=region)
            frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            return frame
        except Exception as e:
            print(f"Error capturing screen region: {e}")
            return None

    def process_frame(self, frame):
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_frame = cv2.GaussianBlur(gray_frame, (5, 5), 0)
        edges = cv2.Canny(gray_frame, 50, 150)
        return edges

    def detect_subtitle_change(self, current_frame, prev_frame):
        score, diff = ssim(current_frame, prev_frame, full=True)
        non_zero_count = np.count_nonzero(diff)
        return score < 0.8 and non_zero_count > 1000

    def save_subtitle_frame(self, frame, timestamp):
        output_path = os.path.join(self.output_dir, f'subtitle_{self.subtitle_count:04d}_{timestamp}.png')
        cv2.imwrite(output_path, frame)
        print(f'Subtitle change detected, saved frame {self.subtitle_count} as {output_path}')
        self.subtitle_count += 1

    def run(self):
        try:
            region = self.select_subtitle_region()
            cv2.namedWindow('Latest Subtitle', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('Latest Subtitle', region[2], region[3])

            subtitle_change_detected = False
            subtitle_change_timestamp = 0

            while True:
                frame = self.get_screen_region(region)
                if frame is None:
                    continue

                processed_frame = self.process_frame(frame)

                if self.prev_frame is not None:
                    if self.detect_subtitle_change(processed_frame, self.prev_frame):
                        subtitle_change_detected = True
                        subtitle_change_timestamp = time.time()

                if subtitle_change_detected and time.time() - subtitle_change_timestamp > 0.2:
                    timestamp = time.strftime("%Y%m%d_%H%M%S")
                    self.save_subtitle_frame(frame, timestamp)
                    cv2.imshow('Latest Subtitle', frame)
                    subtitle_change_detected = False

                self.prev_frame = processed_frame.copy()
                time.sleep(1)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        except ValueError as ve:
            print(f"Value Error: {ve}")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            cv2.destroyAllWindows()
            print("Processing completed.")

if __name__ == '__main__':
    detector = SubtitleDetector()
    detection_thread = threading.Thread(target=detector.run)
    detection_thread.start()
    detection_thread.join()


