import sys
import cv2
import numpy as np
import random
import time
import win32api
import win32con
import win32gui
from mss import mss
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QSpinBox, QHBoxLayout, QCheckBox
from PyQt5.QtGui import QPixmap, QImage, QIcon
from PyQt5.QtCore import QTimer


class ScreenRecorderAlpha(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Screen Recorder Alpha")
        self.setGeometry(100, 100, 800, 600)
        self.setWindowIcon(QIcon("camera.ico"))

        # Settings
        self.game_running = False
        self.crosshair_size = 50
        self.zoom_mode = False
        self.aim_smooth_min = 0.05
        self.aim_smooth_max = 0.15
        self.click_delay_min = 0.02
        self.click_delay_max = 0.08
        self.headshot_probability = 0.8
        self.crosshair_center = (960, 540)
        self.target_window_name = "TEST"

        # Mor renk tespiti
        self.hsv_lower = np.array([140, 50, 50])
        self.hsv_upper = np.array([160, 255, 255])
        self.min_purple_percentage = 0.02
        self.max_purple_percentage = 0.3

        # HOG Parameters
        self.winStride = (4, 4)
        self.padding = (8, 8)
        self.scale = 1.02

        # Screen capture
        self.sct = mss()

        # Initialize HOG detector
        self.hog = cv2.HOGDescriptor()
        self.hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

        # Target memory
        self.last_target_position = None
        self.target_miss_frames = 0

        # Initialize UI
        self.init_ui()

        # Timer for processing frames
        self.timer = QTimer()
        self.timer.timeout.connect(self.process_frame)

    def init_ui(self):
        layout = QVBoxLayout()

        self.video_label = QLabel("Game Feed")
        self.video_label.setFixedSize(800, 450)
        layout.addWidget(self.video_label)

        smooth_layout = QHBoxLayout()
        smooth_layout.addWidget(QLabel("Aim Smoothness Min (s):"))
        self.smooth_min_spin = QSpinBox()
        self.smooth_min_spin.setRange(1, 100)
        self.smooth_min_spin.setValue(int(self.aim_smooth_min * 100))
        self.smooth_min_spin.valueChanged.connect(self.update_smooth_min)
        smooth_layout.addWidget(self.smooth_min_spin)

        smooth_layout.addWidget(QLabel("Aim Smoothness Max (s):"))
        self.smooth_max_spin = QSpinBox()
        self.smooth_max_spin.setRange(1, 100)
        self.smooth_max_spin.setValue(int(self.aim_smooth_max * 100))
        self.smooth_max_spin.valueChanged.connect(self.update_smooth_max)
        smooth_layout.addWidget(self.smooth_max_spin)

        layout.addLayout(smooth_layout)

        self.zoom_checkbox = QCheckBox("Zoom Mode")
        self.zoom_checkbox.stateChanged.connect(self.toggle_zoom_mode)
        layout.addWidget(self.zoom_checkbox)

        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.start_game)
        layout.addWidget(self.start_button)

        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self.stop_game)
        layout.addWidget(self.stop_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def update_smooth_min(self, value):
        self.aim_smooth_min = value / 100

    def update_smooth_max(self, value):
        self.aim_smooth_max = value / 100

    def toggle_zoom_mode(self, state):
        self.zoom_mode = state == 2

    def start_game(self):
        self.game_running = True
        self.timer.start(5)

    def stop_game(self):
        self.game_running = False
        self.timer.stop()

    def move_mouse(self, x, y):
        win32api.SetCursorPos((int(x), int(y)))

    def left_click(self):
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
        time.sleep(0.02)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

    def is_purple_detected(self, region):
        hsv_region = cv2.cvtColor(region, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv_region, self.hsv_lower, self.hsv_upper)

        purple_pixels = cv2.countNonZero(mask)
        total_pixels = region.shape[0] * region.shape[1]
        purple_percentage = purple_pixels / total_pixels

        return purple_percentage >= self.min_purple_percentage

    def is_game_window_active(self):
        hwnd = win32gui.GetForegroundWindow()
        window_title = win32gui.GetWindowText(hwnd)
        return self.target_window_name.lower() in window_title.lower()

    def process_frame(self):
        if not self.game_running or not self.is_game_window_active():
            return

        try:
            monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080}
            screenshot = self.sct.grab(monitor)
            frame = np.array(screenshot)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

            boxes, weights = self.hog.detectMultiScale(
                frame,
                winStride=self.winStride,
                padding=self.padding,
                scale=self.scale,
            )

            crosshair_area = self.crosshair_size * (2 if not self.zoom_mode else 4)
            target_found = False

            for (x, y, w, h) in boxes:
                target_x = x + w // 2
                target_y = y + h // 2

                if abs(target_x - self.crosshair_center[0]) <= crosshair_area and \
                   abs(target_y - self.crosshair_center[1]) <= crosshair_area:
                    region = frame[y:y + h, x:x + w]

                    if self.is_purple_detected(region) or random.random() > 0.2:  # %80 ihtimalle ateş et
                        aim_y = y + h // 4 if random.random() < self.headshot_probability else y + (3 * h) // 4
                        self.move_mouse(target_x, aim_y)
                        time.sleep(random.uniform(self.aim_smooth_min, self.aim_smooth_max))
                        self.left_click()
                        self.last_target_position = (target_x, target_y)
                        target_found = True
                        break

            if not target_found:
                self.target_miss_frames += 1
                if self.target_miss_frames > 5:
                    self.last_target_position = None
            else:
                self.target_miss_frames = 0

            self.update_ui(frame)

        except Exception as e:
            print(f"Error: {e}")

    def update_ui(self, frame):
        frame_resized = cv2.resize(frame, (800, 450))
        height, width, channel = frame_resized.shape
        qimg = QImage(frame_resized.data, width, height, width * channel, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimg)
        self.video_label.setPixmap(pixmap)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ScreenRecorderAlpha()
    window.show()
    sys.exit(app.exec_())
