import tkinter as tk
from tkinter import ttk
import serial.tools.list_ports
import pyaudio
import numpy as np
import threading

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

p = pyaudio.PyAudio()
ser = None
stream = None

root = tk.Tk()
root.title("ESP32 Ses Görselleştirici")
root.geometry("400x300")

com_port_label = ttk.Label(root, text="COM Portu Seçin:")
com_port_label.pack(pady=5)

com_port_combobox = ttk.Combobox(root, state="readonly")
com_port_combobox.pack()

input_device_label = ttk.Label(root, text="Ses Giriş Cihazı Seçin:")
input_device_label.pack(pady=5)

input_device_combobox = ttk.Combobox(root, state="readonly")
input_device_combobox.pack()

def refresh_com_ports():
    ports = serial.tools.list_ports.comports()
    com_port_combobox['values'] = [port.device for port in ports]
    if ports:
        com_port_combobox.current(0)

def refresh_input_devices():
    input_devices = []
    for i in range(p.get_device_count()):
        device_info = p.get_device_info_by_index(i)
        if device_info['maxInputChannels'] > 0:
            input_devices.append(f"{device_info['index']}: {device_info['name']}")
    input_device_combobox['values'] = input_devices
    if input_devices:
        input_device_combobox.current(0)

refresh_com_ports()
refresh_input_devices()

def connect_to_esp32():
    global ser
    selected_port = com_port_combobox.get()
    try:
        ser = serial.Serial(selected_port, 115200)
        status_label.config(text=f"Bağlandı: {selected_port}", fg="green")
    except Exception as e:
        status_label.config(text=f"Hata: {str(e)}", fg="red")

connect_button = ttk.Button(root, text="Bağlan", command=connect_to_esp32)
connect_button.pack(pady=10)

def select_input_device():
    global stream
    if stream:
        stream.stop_stream()
        stream.close()
    selected_device = input_device_combobox.get()
    if selected_device:
        device_index = int(selected_device.split(":")[0])
        try:
            stream = p.open(format=FORMAT,
                            channels=CHANNELS,
                            rate=RATE,
                            input=True,
                            input_device_index=device_index,
                            frames_per_buffer=CHUNK)
            status_label.config(text=f"Ses cihazı seçildi: {selected_device}", fg="blue")
        except Exception as e:
            status_label.config(text=f"Hata: {str(e)}", fg="red")

select_device_button = ttk.Button(root, text="Ses Cihazını Seç", command=select_input_device)
select_device_button.pack(pady=10)

status_label = tk.Label(root, text="Bağlantı bekleniyor...", fg="black")
status_label.pack(pady=10)

def process_audio():
    while True:
        if ser and ser.is_open and stream:
            try:
                data = stream.read(CHUNK, exception_on_overflow=False)
                data = np.frombuffer(data, dtype=np.int16)

                fft_data = np.fft.fft(data)
                fft_magnitude = np.abs(fft_data)[:CHUNK // 2]

                bands = np.array_split(fft_magnitude, 32)
                band_values = [int(np.mean(band)) for band in bands]

                band_values = (band_values / np.max(band_values)) * 100
                band_values = band_values.astype(int)

                ser.write(f"bars,{','.join(map(str, band_values))}\n".encode())
            except Exception as e:
                print(f"Hata: {str(e)}")
                break

audio_thread = threading.Thread(target=process_audio, daemon=True)
audio_thread.start()

root.mainloop()
