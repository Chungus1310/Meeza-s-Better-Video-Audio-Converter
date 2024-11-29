import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os
import threading

class ConversionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Meeza's Song Converter")

        self.file_queue = []
        self.conversion_running = False
        self.stop_event = threading.Event()  # Use threading.Event

        self.file_path = ctk.StringVar()
        self.output_path = ctk.StringVar()
        self.media_type = ctk.StringVar(value="audio")
        self.output_format = ctk.StringVar()
        self.preset = ctk.StringVar()

        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.create_widgets()

    def create_widgets(self):
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        # Media Type Selection
        media_frame = ctk.CTkFrame(main_frame)
        media_frame.pack(padx=10, pady=10, fill=tk.X)

        ctk.CTkLabel(media_frame, text="Select Media Type:").pack(side=tk.LEFT, padx=5, pady=5)
        audio_radio = ctk.CTkRadioButton(media_frame, text="Audio", variable=self.media_type, value="audio", command=self.update_formats)
        audio_radio.pack(side=tk.LEFT, padx=5, pady=5)
        video_radio = ctk.CTkRadioButton(media_frame, text="Video", variable=self.media_type, value="video", command=self.update_formats)
        video_radio.pack(side=tk.LEFT, padx=5, pady=5)

        # Format and Preset Selection
        format_frame = ctk.CTkFrame(main_frame)
        format_frame.pack(padx=10, pady=10, fill=tk.X)

        self.format_label = ctk.CTkLabel(format_frame, text="Select Output Format:")
        self.format_label.pack(side=tk.LEFT, padx=5, pady=5)
        self.format_menu = ctk.CTkComboBox(format_frame, variable=self.output_format, state="readonly")
        self.format_menu.pack(side=tk.LEFT, padx=5, pady=5)

        self.preset_label = ctk.CTkLabel(format_frame, text="Select Preset:")
        self.preset_label.pack(side=tk.LEFT, padx=5, pady=5)
        self.preset_menu = ctk.CTkComboBox(format_frame, variable=self.preset, state="readonly")
        self.preset_menu.pack(side=tk.LEFT, padx=5, pady=5)

        # File Queue
        queue_frame = ctk.CTkFrame(main_frame)
        queue_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        ctk.CTkLabel(queue_frame, text="File Queue:").pack(side=tk.TOP, padx=5, pady=5)
        self.listbox = tk.Listbox(queue_frame, height=10, width=50)
        self.listbox.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.BOTH, expand=True)

        button_frame = ctk.CTkFrame(queue_frame)
        button_frame.pack(side=tk.RIGHT, padx=5, pady=5, fill=tk.Y)

        add_button = ctk.CTkButton(button_frame, text="Add Files", command=self.add_files)
        add_button.pack(side=tk.TOP, padx=5, pady=5)
        remove_button = ctk.CTkButton(button_frame, text="Remove Selected", command=self.remove_selected)
        remove_button.pack(side=tk.TOP, padx=5, pady=5)

        # Progress Bar
        progress_frame = ctk.CTkFrame(main_frame)
        progress_frame.pack(padx=10, pady=10, fill=tk.X)

        self.progress_var = ctk.DoubleVar()
        self.progress_bar = ctk.CTkProgressBar(progress_frame, variable=self.progress_var)
        self.progress_bar.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)

        # Start and Stop Buttons
        control_frame = ctk.CTkFrame(main_frame)
        control_frame.pack(padx=10, pady=10, fill=tk.X)

        self.start_button = ctk.CTkButton(control_frame, text="Start", command=self.start_conversion)
        self.start_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.stop_button = ctk.CTkButton(control_frame, text="Stop", command=self.stop_conversion_command, state=tk.DISABLED)
        self.stop_button.pack(side=tk.RIGHT, padx=5, pady=5)

        # Output Path Selection
        path_frame = ctk.CTkFrame(main_frame)
        path_frame.pack(padx=10, pady=10, fill=tk.X)

        ctk.CTkLabel(path_frame, text="Select Output Path:").pack(side=tk.LEFT, padx=5, pady=5)
        entry_output = ctk.CTkEntry(path_frame, textvariable=self.output_path, width=400)
        entry_output.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)
        ctk.CTkButton(path_frame, text="Browse", command=self.browse_output_path).pack(side=tk.RIGHT, padx=5, pady=5)

        # Output Text Box
        output_frame = ctk.CTkFrame(main_frame)
        output_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.output_text = ctk.CTkTextbox(output_frame, width=600, height=200, state='disabled')
        self.output_text.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.BOTH, expand=True)
        fineprint_frame = ctk.CTkFrame(self.root)
        fineprint_frame.pack(side=tk.BOTTOM, fill=tk.X)

        fineprint_label = ctk.CTkLabel(fineprint_frame, text="Built by Chun", font=("Arial", 10))
        fineprint_label.pack(side=tk.RIGHT, padx=10, pady=5)
        self.update_formats()

    def add_files(self):
        files = filedialog.askopenfilenames(filetypes=[("Media Files", "*.mp4 *.mkv *.avi *.mp3 *.wav *.ogg *.webm *.flv *.mov")])
        if files:
            for file in files:
                self.file_queue.append(file)
                self.listbox.insert(tk.END, os.path.basename(file))

    def remove_selected(self):
        selected_indices = self.listbox.curselection()
        if selected_indices:
            for index in reversed(selected_indices):
                del self.file_queue[index]
                self.listbox.delete(index)

    def update_formats(self):
        media_type = self.media_type.get()
        if media_type == "audio":
            self.format_menu.configure(values=["mp3", "wav", "ogg", "aac", "flac"])
            self.preset_menu.configure(values=["High Quality", "Medium Quality", "Low Quality", "Fastest"])
        elif media_type == "video":
            self.format_menu.configure(values=["mp4", "webm", "avi", "flv", "mov", "mkv"])
            self.preset_menu.configure(values=["High Quality", "Medium Quality", "Low Quality", "Fastest"])

    def update_text_box(self, text):
        def insert_text():
            self.output_text.configure(state='normal')
            self.output_text.insert(tk.END, text)
            self.output_text.configure(state='disabled')
            self.output_text.see(tk.END)
        self.root.after(0, insert_text)

    def start_conversion(self):
        if not self.file_queue:
            messagebox.showwarning("No Files", "Please add files to the queue.")
            return
        if not self.output_path.get():
            messagebox.showwarning("No Output Path", "Please select an output path.")
            return
        self.conversion_running = True
        self.stop_event.clear()  # Reset the stop event
        self.start_button.configure(state=tk.DISABLED)
        self.stop_button.configure(state=tk.NORMAL)
        threading.Thread(target=self.convert_queue).start()

    def stop_conversion_command(self):
        if self.conversion_running:
            self.stop_event.set()  # Signal to stop

    def convert_queue(self):
        total_files = len(self.file_queue)
        for index, input_file in enumerate(self.file_queue, 1):
            if self.stop_event.is_set():
                self.update_text_box("Conversion stopped by user.\n")
                break
            output_file = os.path.join(self.output_path.get(), os.path.splitext(os.path.basename(input_file))[0] + f'.{self.output_format.get()}')
            self.convert_file(input_file, output_file)
            # Update progress bar
            progress = (index / total_files) * 100
            self.progress_var.set(progress)
        self.conversion_running = False
        self.progress_var.set(0)
        self.update_text_box("Conversion completed.\n")
        self.start_button.configure(state=tk.NORMAL)
        self.stop_button.configure(state=tk.DISABLED)

    def convert_file(self, input_file, output_file):
        preset = self.preset.get()
        fast_audio_options = {
            'mp3': {'codec': 'libmp3lame', 'bitrate': '128k'},
            'wav': {'codec': 'pcm_s16le'},
            'ogg': {'codec': 'libvorbis', 'qscale:a': 5},
            'aac': {'codec': 'aac', 'bitrate': '128k'},
            'flac': {'codec': 'flac', 'compression_level': 0},
        }

        fast_video_options = {
            'mp4': {'vcodec': 'libx264', 'preset': 'ultrafast', 'acodec': 'aac'},
            'webm': {'vcodec': 'libvpx-vp9', 'cpu-used': '5', 'deadline': 'realtime', 'acodec': 'libopus'},
            'avi': {'vcodec': 'libxvid', 'acodec': 'mp3'},
            'flv': {'vcodec': 'libx264', 'preset': 'ultrafast', 'acodec': 'aac'},
            'mov': {'vcodec': 'libx264', 'preset': 'ultrafast', 'acodec': 'aac'},
            'mkv': {'vcodec': 'libx264', 'preset': 'ultrafast', 'acodec': 'aac'},
        }

        try:
            if preset == "Fastest":
                media_type = self.media_type.get()
                if media_type == "audio":
                    options = fast_audio_options.get(self.output_format.get(), {})
                    command = ['ffmpeg', '-i', input_file]
                    for key, value in options.items():
                        if isinstance(value, dict):
                            for k, v in value.items():
                                command.extend(['-{}'.format(k), str(v)])
                        else:
                            command.extend(['-{}'.format(key), str(value)])
                    command.append(output_file)
                elif media_type == "video":
                    options = fast_video_options.get(self.output_format.get(), {})
                    command = ['ffmpeg', '-i', input_file]
                    for key, value in options.items():
                        if isinstance(value, dict):
                            for k, v in value.items():
                                command.extend(['-{}'.format(k), str(v)])
                        else:
                            command.extend(['-{}'.format(key), str(value)])
                    command.append(output_file)
            else:
                if self.media_type.get() == "audio":
                    bitrate_map = {
                        "High Quality": "192k",
                        "Medium Quality": "128k",
                        "Low Quality": "96k"
                    }
                    bitrate = bitrate_map.get(preset, "192k")
                    command = ['ffmpeg', '-i', input_file, '-ab', bitrate, output_file]
                elif self.media_type.get() == "video":
                    if preset == "Custom WEBM":
                        command = ['ffmpeg', '-i', input_file, '-vcodec', 'libvpx-vp9', '-cpu-used', '5', '-deadline', 'realtime', '-acodec', 'libopus', output_file]
                    else:
                        quality_map = {
                            "High Quality": (20, 'aac'),
                            "Medium Quality": (23, 'aac'),
                            "Low Quality": (26, 'aac')
                        }
                        crf, acodec = quality_map.get(preset, (20, 'aac'))
                        command = ['ffmpeg', '-i', input_file, '-vcodec', 'libx264', '-crf', str(crf), '-acodec', acodec, output_file]

            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            while True:
                if self.stop_event.is_set():
                    process.terminate()
                    self.update_text_box("Conversion process terminated.\n")
                    break
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    self.update_text_box(output)
            rc = process.poll()
            if rc != 0:
                self.update_text_box(f"Conversion exited with return code {rc}\n")
            else:
                messagebox.showinfo("Success", f"File converted to {self.output_format.get().upper()} successfully!")
        except Exception as e:
            self.update_text_box(f"Error: {str(e)}\n")
            messagebox.showerror("Error", f"Conversion failed: {str(e)}")

    def browse_output_path(self):
        output_path = filedialog.askdirectory()
        if output_path:
            self.output_path.set(output_path)

if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("800x600")  # Set a larger window size
    app = ConversionApp(root)
    root.mainloop()