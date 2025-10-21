import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox, scrolledtext
import subprocess
import os
import random
import threading
import webbrowser
from tkinter import font
import sys
import re

# --- Constants ---
CREATE_NO_WINDOW = 0x08000000

class VideoProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fmpeg MediaTool v1.0 by Rahmony") # --- NEW --- Version bump
        self.root.geometry("600x710") # Made shorter - removed output link

        # --- Variables ---
        self.video_files = []
        self.is_processing = False
        self.ffmpeg_path = self.get_binary_path("ffmpeg.exe")
        self.ffprobe_path = self.get_binary_path("ffprobe.exe")
        # self.last_output_folder = "" # Removed - no longer needed

        # --- UI Layout ---
        top_frame = ttk.Frame(root, padding=10)
        top_frame.pack(fill='x')

        self.btn_select_videos = ttk.Button(top_frame, text="Select Videos", command=self.select_videos)
        self.btn_select_videos.pack(side='left', fill='x', expand=True, padx=(0, 10))

        self.lbl_videos_status = ttk.Label(top_frame, text="Selected Videos: 0", relief="sunken", padding=5)
        self.lbl_videos_status.pack(side='left', fill='x', expand=True)

        self.notebook = ttk.Notebook(root, padding=10)
        self.notebook.pack(fill='both', expand=True)

        self.tab_audio = ttk.Frame(self.notebook, padding=10)
        self.tab_convert = ttk.Frame(self.notebook, padding=10)

        self.notebook.add(self.tab_convert, text='   Convert & Unique-ize   ')
        self.notebook.add(self.tab_audio, text='   Audio Tools   ')

        # --- Tab 1: Converter & Unique-izer (Layout same as v3.7) ---
        convert_frame = ttk.Frame(self.tab_convert); convert_frame.pack(pady=(10, 5))
        convert_label = ttk.Label(convert_frame, text="Convert all selected videos to:")
        convert_label.pack(side='left', padx=(0, 10))
        self.convert_format = tk.StringVar(value=".mp4")
        convert_options = [".mp4", ".mkv", ".mov", ".gif", ".avi"]
        self.convert_dropdown = ttk.OptionMenu(convert_frame, self.convert_format, convert_options[0], *convert_options, command=self.on_format_change)
        self.convert_dropdown.pack(side='left')
        ttk.Separator(self.tab_convert, orient='horizontal').pack(fill='x', pady=10)
        res_frame = ttk.Frame(self.tab_convert)
        res_frame.pack(fill='x', pady=5, padx=20)
        res_label = ttk.Label(res_frame, text="Resolution (Picture Size):")
        res_label.pack(side='left')
        self.resolution_var = tk.StringVar(value="Keep Original")
        res_options = ["Keep Original", "1080p (1920px wide)", "720p (1280px wide)", "480p (854px wide)", "360p (640px wide)"]
        self.resolution_dropdown = ttk.OptionMenu(res_frame, self.resolution_var, res_options[0], *res_options)
        self.resolution_dropdown.pack(side='right')
        self.controls_frame = ttk.Frame(self.tab_convert); self.controls_frame.pack(fill='x', expand=True, pady=10)
        self.crf_frame = ttk.Frame(self.controls_frame)
        self.quality_label = ttk.Label(self.crf_frame, text="Video Quality (18=Best, 30=Smallest): 23")
        self.quality_label.pack(pady=(10,0))
        self.crf_var = tk.IntVar(value=23)
        self.quality_slider = ttk.Scale(self.crf_frame, from_=18, to=30, orient='horizontal', variable=self.crf_var, command=self.update_quality_label)
        self.quality_slider.pack(fill='x', expand=True, padx=20, pady=5)
        quality_desc_frame = ttk.Frame(self.crf_frame); quality_desc_frame.pack(fill='x', padx=20)
        ttk.Label(quality_desc_frame, text="High Quality").pack(side='left')
        ttk.Label(quality_desc_frame, text="Low Quality").pack(side='right')
        self.gif_frame = ttk.Frame(self.controls_frame)
        self.gif_width_label = ttk.Label(self.gif_frame, text="GIF Width (Pixels): 480px")
        self.gif_width_label.pack(pady=(10,0))
        self.gif_width_var = tk.IntVar(value=480)
        self.gif_width_slider = ttk.Scale(self.gif_frame, from_=100, to=1000, orient='horizontal', variable=self.gif_width_var, command=self.update_gif_width_label)
        self.gif_width_slider.pack(fill='x', expand=True, padx=20, pady=5)
        self.gif_fps_label = ttk.Label(self.gif_frame, text="GIF Framerate (FPS): 12")
        self.gif_fps_label.pack(pady=(10,0))
        self.gif_fps_var = tk.IntVar(value=12)
        self.gif_fps_slider = ttk.Scale(self.gif_frame, from_=5, to=30, orient='horizontal', variable=self.gif_fps_var, command=self.update_gif_fps_label)
        self.gif_fps_slider.pack(fill='x', expand=True, padx=20, pady=5)
        self.crf_frame.pack(fill='x'); self.gif_frame.pack_forget()
        ttk.Separator(self.tab_convert, orient='horizontal').pack(fill='x', pady=10)
        self.unique_var = tk.IntVar(value=0)
        self.unique_check = ttk.Checkbutton(self.tab_convert, text="Apply Random Filters (Unique-ize)", variable=self.unique_var)
        self.unique_check.pack(pady=5)
        self.btn_start_convert = ttk.Button(self.tab_convert, text="Start Processing", command=self.start_convert_process)
        self.btn_start_convert.pack(pady=10, ipady=10)
        # --- End Tab 1 ---

        # --- Tab 2: Audio Tools (Layout same as v3.7) ---
        self.btn_extract_audio = ttk.Button(self.tab_audio, text="Extract Audio (.mp3)", command=self.start_extract_audio_process)
        self.btn_extract_audio.pack(pady=(10, 5), ipady=10, fill='x')
        self.btn_mute_videos = ttk.Button(self.tab_audio, text="Remove Audio (Mute Videos) - Instant", command=self.start_mute_videos_process)
        self.btn_mute_videos.pack(pady=5, ipady=10, fill='x')

        # --- Progress Bar (Layout same as v3.7) ---
        self.progress_frame = ttk.Frame(root, padding=(10, 0, 10, 5))
        self.progress_frame.pack(fill='x')
        self.progress_label = ttk.Label(self.progress_frame, text="Progress: Idle")
        self.progress_label.pack(fill='x')
        self.progressbar = ttk.Progressbar(self.progress_frame, orient='horizontal', mode='determinate')
        self.progressbar.pack(fill='x', expand=True)

        # --- Output Link Removed ---
        # self.output_link_label = ... (Deleted)

        # --- Log Area (Layout same as v3.7) ---
        self.log_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=10)
        self.log_area.pack(pady=10, padx=10, fill='both', expand=True)

        # --- Credit Links (Layout same as v3.7) ---
        credit_frame = ttk.Frame(root)
        credit_frame.pack(side='bottom', pady=5)
        credits_text = ttk.Label(credit_frame, text="Credits: ")
        credits_text.pack(side='left')
        self.link_font = font.Font(family="Arial", size=9, underline=True) # Defined here for use
        ffmpeg_label = tk.Label(credit_frame, text="FFmpeg", fg="blue", cursor="hand2", font=self.link_font)
        ffmpeg_label.pack(side='left')
        ffmpeg_label.bind("<Button-1>", self.open_ffmpeg_link)
        separator_label = ttk.Label(credit_frame, text=" , ")
        separator_label.pack(side='left')
        credit_label = tk.Label(credit_frame, text="Rahmony", fg="blue", cursor="hand2", font=self.link_font)
        credit_label.pack(side='left')
        credit_label.bind("<Button-1>", self.open_linkedin_link)
        # --- END Credits ---


        self.log_message("Welcome to the Video Multi-Tool! Select your videos at the top.", msg_type="info")

        if not (os.path.exists(self.ffmpeg_path) and os.path.exists(self.ffprobe_path)):
             self.log_message("CRITICAL ERROR: ffmpeg.exe or ffprobe.exe not found!", msg_type="error")
             self.log_message("Please ensure both files are in the same folder as the app.", msg_type="info")
             self.set_ui_processing(True)

    # --- HELPER FUNCTIONS ---
    def get_binary_path(self, binary_name):
        if getattr(sys, 'frozen', False): base_path = sys._MEIPASS
        else: base_path = os.path.abspath(".")
        return os.path.join(base_path, binary_name)

    def open_ffmpeg_link(self, event): webbrowser.open_new_tab("https://ffmpeg.org/")
    def open_linkedin_link(self, event): webbrowser.open_new_tab("https://www.linkedin.com/in/rahmony")
    # def open_output_folder(self, event): ... # Removed

    def select_videos(self):
        if self.is_processing: return
        filetypes = (("Video files", "*.mp4 *.avi *.mkv *.mov *.flv"), ("All files", "*.*"))
        files = filedialog.askopenfilenames(title="Select Video Files", filetypes=filetypes)
        if files:
            self.video_files = files
            self.lbl_videos_status.config(text=f"Selected Videos: {len(self.video_files)}")
            self.log_message(f"Loaded {len(self.video_files)} video(s). Ready for a task.", msg_type="info")

    # def update_output_link(self, folder_path): ... # Removed

    def update_quality_label(self, value):
        current_val = round(float(value))
        self.quality_label.config(text=f"Video Quality (18=Best, 30=Smallest): {current_val}")

    def update_gif_width_label(self, value):
        current_val = round(float(value))
        self.gif_width_label.config(text=f"GIF Width (Pixels): {current_val}px")

    def update_gif_fps_label(self, value):
        current_val = round(float(value))
        self.gif_fps_label.config(text=f"GIF Framerate (FPS): {current_val}")

    def on_format_change(self, selected_format):
        if selected_format == ".gif":
            self.crf_frame.pack_forget(); self.gif_frame.pack(fill='x')
            self.resolution_dropdown.config(state='disabled')
        else:
            self.gif_frame.pack_forget(); self.crf_frame.pack(fill='x')
            self.resolution_dropdown.config(state='normal')

    def set_ui_processing(self, processing):
        self.is_processing = processing
        state = 'disabled' if processing else 'normal'
        self.btn_select_videos.config(state=state)
        # self.btn_start_unique.config(state=state) # Removed
        self.btn_extract_audio.config(state=state)
        self.btn_mute_videos.config(state=state)
        self.btn_start_convert.config(state=state)
        self.convert_dropdown.config(state=state)
        self.quality_slider.config(state=state)
        self.gif_width_slider.config(state=state)
        self.gif_fps_slider.config(state=state)
        self.resolution_dropdown.config(state=state)
        self.unique_check.config(state=state)

        if not processing:
            self.on_format_change(self.convert_format.get())

    def update_progress(self, value, text):
        self.root.after(0, self.progressbar.config, {'value': value})
        self.root.after(0, self.progress_label.config, {'text': text})

    def convert_time_to_seconds(self, time_str):
        try:
            h, m, s_micro = time_str.split(':')
            s, micro = s_micro.split('.')
            return int(h) * 3600 + int(m) * 60 + int(s) + int(micro) / 100.0
        except: return None

    def get_video_duration(self, video_path):
        command = [self.ffprobe_path, "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", video_path]
        try:
            result = subprocess.run(command, capture_output=True, text=True, creationflags=CREATE_NO_WINDOW, encoding='utf-8')
            return float(result.stdout.strip())
        except Exception as e:
            self.log_message(f"Error getting duration: {e}", msg_type="error"); return None

    def log_message(self, msg, msg_type="info"):
        """
        Log a message with an emoji based on type.
        msg_type: 'info' (ℹ️), 'success' (✅), 'error' (❌), 'start' (🚀)
        """
        emojis = {
            "info": "ℹ️ ",
            "success": "✅ ",
            "error": "❌ ",
            "start": "🚀 "
        }
        emoji = emojis.get(msg_type, "")
        def _log():
            self.log_area.insert(tk.END, f"{emoji}{msg}\n")
            self.log_area.see(tk.END)
        self.root.after(0, _log)

    # def check_before_run(self): ... # Removed

    # --- CORE PROCESSING LOGIC ---

    def run_ffmpeg_with_progress(self, command, video_path, total_videos, current_video_index):
        self.log_message(f"Processing ({current_video_index+1}/{total_videos}): {os.path.basename(video_path)}", msg_type="info")
        total_duration = self.get_video_duration(video_path)
        if not total_duration:
            self.log_message("Could not get video duration, cannot show progress.", msg_type="error")
            total_duration = 1
        process = subprocess.Popen(command, stderr=subprocess.PIPE, stdout=subprocess.PIPE,
                                   universal_newlines=True, encoding='utf-8', errors='replace',
                                   creationflags=CREATE_NO_WINDOW)
        time_regex = re.compile(r"time=(\d{2}:\d{2}:\d{2}\.\d{2})")

        full_stderr = "" # --- NEW --- Store full error

        for line in process.stderr:
            full_stderr += line # --- NEW --- Append line
            match = time_regex.search(line)
            if match:
                current_time_str = match.group(1)
                current_time_sec = self.convert_time_to_seconds(current_time_str)
                if current_time_sec is not None:
                    percentage = (current_time_sec / total_duration) * 100
                    self.update_progress(percentage, f"Processing file {current_video_index+1}/{total_videos}... {int(percentage)}%")
        process.wait()
        if process.returncode == 0:
            return True
        else:
            # --- NEW --- Log the *entire* error message
            self.log_message(f"ERROR processing {os.path.basename(video_path)}:", msg_type="error")
            self.log_message(f"FFmpeg Error Output:\n{full_stderr}", msg_type="error")
            # --- END NEW ---
            return False


    # --- 1. UNIQUE-IZER (REMOVED) ---

    # --- 2. AUDIO TOOLS (--- UPDATED --- Output Path) ---
    def start_extract_audio_process(self):
        if self.is_processing: return
        # --- NEW --- Check for files directly
        if not self.video_files:
            messagebox.showerror("Error", "Please select at least one video file at the top.")
            return
        # --- END NEW ---
        self.set_ui_processing(True); self.log_message("--- Starting Batch: Extract Audio ---", msg_type="start")
        processing_thread = threading.Thread(target=self.process_extract_audio, daemon=True) # Removed output_folder arg
        processing_thread.start()

    def process_extract_audio(self): # Removed output_folder arg
        total_videos = len(self.video_files)
        for i, video_path in enumerate(self.video_files):
            try:
                # --- NEW --- Calculate output dir per file
                output_dir = os.path.dirname(video_path)
                base_name, _ = os.path.splitext(os.path.basename(video_path))
                output_path = os.path.join(output_dir, f"fmpeg_{base_name}_audio.mp3") # Use output_dir
                # --- END NEW ---

                command = [self.ffmpeg_path, "-i", video_path, "-vn", "-c:a", "mp3", output_path, "-y"]
                success = self.run_ffmpeg_with_progress(command, video_path, total_videos, i)
                if success:
                    self.log_message(f"SUCCESS: Saved to {output_path}", msg_type="success")
            except Exception as e: self.log_message(f"A fatal error occurred: {e}", msg_type="error")
        self.log_message("--- Batch Finished: Extract Audio ---", msg_type="start")
        self.update_progress(0, "Progress: Idle")
        self.set_ui_processing(False)

    def start_mute_videos_process(self):
        if self.is_processing: return
        # --- NEW --- Check for files directly
        if not self.video_files:
            messagebox.showerror("Error", "Please select at least one video file at the top.")
            return
        # --- END NEW ---
        self.set_ui_processing(True); self.log_message("--- Starting Batch: Mute Videos ---", msg_type="start")
        processing_thread = threading.Thread(target=self.process_mute_videos, daemon=True) # Removed output_folder arg
        processing_thread.start()

    def process_mute_videos(self): # Removed output_folder arg
        total_videos = len(self.video_files)
        for i, video_path in enumerate(self.video_files):
            try:
                self.log_message(f"Muting ({i+1}/{total_videos}): {os.path.basename(video_path)} (This is instant)", msg_type="info")
                self.update_progress((i+1)/total_videos*100, f"Muting file {i+1}/{total_videos}...")

                # --- NEW --- Calculate output dir per file
                output_dir = os.path.dirname(video_path)
                base_name, ext = os.path.splitext(os.path.basename(video_path))
                output_path = os.path.join(output_dir, f"fmpeg_{base_name}_muted{ext}") # Use output_dir
                # --- END NEW ---

                command = [self.ffmpeg_path, "-i", video_path, "-c:v", "copy", "-an", output_path, "-y"]
                result = subprocess.run(command, capture_output=True, text=True, creationflags=CREATE_NO_WINDOW)
                if result.returncode == 0:
                    self.log_message(f"SUCCESS: Saved to {output_path}", msg_type="success")
                else:
                    # Log full error here too
                    self.log_message(f"ERROR processing {os.path.basename(video_path)}:", msg_type="error")
                    self.log_message(f"FFmpeg Error Output:\n{result.stderr}", msg_type="error")

            except Exception as e: self.log_message(f"A fatal error occurred: {e}", msg_type="error")
        self.log_message("--- Batch Finished: Mute Videos ---", msg_type="start")
        self.update_progress(0, "Progress: Idle")
        self.set_ui_processing(False)


    # --- 3. CONVERTER (--- UPDATED --- Output Path & GIF Fix) ---
    def start_convert_process(self):
        if self.is_processing: return
        # --- NEW --- Check for files directly
        if not self.video_files:
            messagebox.showerror("Error", "Please select at least one video file at the top.")
            return
        # --- END NEW ---

        # Get ALL settings from the UI (same as v3.7)
        convert_to_ext = self.convert_format.get()
        crf_value = round(self.crf_var.get())
        gif_width = round(self.gif_width_var.get())
        gif_fps = round(self.gif_fps_var.get())
        is_unique = self.unique_var.get() == 1
        resolution_str = self.resolution_var.get()

        self.set_ui_processing(True)
        self.log_message(f"--- Starting Batch: Convert to {convert_to_ext} ---", msg_type="start")

        # Pass all settings to the processing thread (Removed output_folder arg)
        processing_thread = threading.Thread(target=self.process_convert,
            args=(convert_to_ext, crf_value, gif_width, gif_fps, is_unique, resolution_str),
            daemon=True)
        processing_thread.start()

    def process_convert(self, convert_to_ext, crf_value, gif_width, gif_fps, is_unique, resolution_str): # Removed output_folder arg
        total_videos = len(self.video_files)
        for i, video_path in enumerate(self.video_files):
            try:
                # --- 1. Build Output Path (--- UPDATED ---) ---
                output_dir = os.path.dirname(video_path) # Get dir of current file
                base_name, _ = os.path.splitext(os.path.basename(video_path))
                output_filename = f"fmpeg_{base_name}"
                if is_unique:
                    output_filename += "_unique"
                output_filename += convert_to_ext
                output_path = os.path.join(output_dir, output_filename) # Use output_dir
                # --- END UPDATE ---

                # --- 2. Build Filter Lists (same as v3.7) ---
                video_filters = []
                audio_filters = []
                if is_unique:
                    self.log_message("...Applying 'Unique-izer' filters...", msg_type="info")
                    rand_resolution = random.uniform(0.90, 1.10); rand_volume = random.uniform(0.90, 1.10)
                    rand_gamma = random.uniform(0.90, 1.10); rand_saturation = random.uniform(0.90, 1.10)
                    rand_brightness = random.uniform(0.00, 0.10)
                    video_filters.append(f"scale='ceil(iw*{rand_resolution}/2)*2:ceil(ih*{rand_resolution}/2)*2'")
                    video_filters.append(f"eq=gamma={rand_gamma}:saturation={rand_saturation}:brightness={rand_brightness}")
                    audio_filters.append(f"volume={rand_volume}")

                # --- 3. Build Command (--- UPDATED --- GIF Scale) ---
                command = [self.ffmpeg_path, "-i", video_path]
                if convert_to_ext == ".gif":
                    self.log_message(f"...GIF Settings: Width={gif_width}px, FPS={gif_fps}...", msg_type="info")
                    # --- FIX --- Use -2 for height scaling, ensures divisibility by 2
                    gif_filters_list = video_filters + [f"fps={gif_fps},scale={gif_width}:-2:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse"]
                    video_filters = gif_filters_list # Overwrite video filters for GIF
                    # --- END FIX ---
                    command.extend(["-loop", "0", "-an"])
                else:
                    if resolution_str != "Keep Original":
                        res_match = re.search(r"(\d+)px", resolution_str)
                        if res_match:
                           res_width = res_match.group(1)
                           video_filters.append(f"scale={res_width}:-2") # Use -2 here too
                           self.log_message(f"...Resizing to {res_width}px wide...", msg_type="info")
                    self.log_message(f"...Using quality setting CRF={crf_value}...", msg_type="info")
                    command.extend(["-crf", str(crf_value)])

                # --- 4. Add filters to command (same as v3.7) ---
                if video_filters:
                    command.extend(["-vf", ",".join(video_filters)])
                if audio_filters:
                    command.extend(["-af", ",".join(audio_filters)])

                # --- 5. Add output path and run (same as v3.7) ---
                command.extend([output_path, "-y"])
                success = self.run_ffmpeg_with_progress(command, video_path, total_videos, i)
                if success:
                    self.log_message(f"SUCCESS: Saved to {output_path}", msg_type="success")

            except Exception as e:
                self.log_message(f"A fatal error occurred: {e}", msg_type="error")

        self.log_message(f"--- Batch Finished: Convert to {convert_to_ext} ---", msg_type="start")
        self.update_progress(0, "Progress: Idle")
        self.set_ui_processing(False)


if __name__ == "__main__":
    root = tk.Tk()
    app = VideoProcessorApp(root)
    root.mainloop()