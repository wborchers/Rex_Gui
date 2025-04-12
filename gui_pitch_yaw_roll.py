import tkinter as tk
import serial
import threading

SERIAL_PORT = "/dev/ttyACM0"
BAUD_RATE = 115200

class SensorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("BNO085 Pitch/Yaw/Roll")

        self.yaw_label = tk.Label(root, text="Yaw: 0.00", font=("Arial", 16))
        self.yaw_label.pack(pady=5)

        self.pitch_label = tk.Label(root, text="Pitch: 0.00", font=("Arial", 16))
        self.pitch_label.pack(pady=5)

        self.roll_label = tk.Label(root, text="Roll: 0.00", font=("Arial", 16))
        self.roll_label.pack(pady=5)

        self.serial_connection = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)

        self.update_thread = threading.Thread(target=self.read_serial_data, daemon=True)
        self.update_thread.start()

    def read_serial_data(self):
        while True:
            try:
                line = self.serial_connection.readline().decode("utf-8").strip()
                if line:
                    parts = line.split(",")
                    if len(parts) == 3:
                        yaw, pitch, roll = map(float, parts)
                        self.yaw_label.config(text=f"Yaw: {yaw:.2f}")
                        self.pitch_label.config(text=f"Pitch: {pitch:.2f}")
                        self.roll_label.config(text=f"Roll: {roll:.2f}")
            except Exception as e:
                print(f"Error reading serial: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    gui = SensorGUI(root)
    root.mainloop()
