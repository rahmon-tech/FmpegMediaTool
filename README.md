# FMpeg MediaTool v3.9
*A robust and responsive media tool built with Python and FFmpeg.*

Created by [Rahmony](https://www.linkedin.com/in/rahmony).

<img width="544" height="981" alt="Caghpture" src="https://github.com/user-attachments/assets/64e8a4e0-6219-4334-b148-0990c743ecb3" />
<img width="544" height="981" alt="Capghhture" src="https://github.com/user-attachments/assets/70d389d0-f13f-4d80-9948-5c336ef0cb73" />
<img width="544" height="981" alt="Capture" src="https://github.com/user-attachments/assets/e27f6c2f-c53d-4256-8dd0-c5e0bdde9f13" />


## Features
* **Batch Processing:** Select multiple videos at once.
* **Easy Conversion:** Convert videos to formats like `.mp4`, `.mkv`, `.mov`, `.avi`) with a dropdown. Control video quality (CRF) and resolution (picture size).
* **Robust GIF Creation:** Convert videos to optimized GIFs with sliders for **Width** and **FPS**.
* **Integrated Unique-izer:** Apply random filters (resolution, volume, gamma, saturation, brightness) *during* conversion with a simple checkbox.
* **Audio Tools:**
    * Extract audio from videos and save as `.mp3`.
    * Mute videos by removing the audio track (Instant).
* **Simple Workflow:** Output files are automatically saved in the **same folder** as the original input files, prefixed with `fmpeg_`.
* **Live Progress Bar:** See the progress for each file during conversion/extraction.
* **Self-Contained (Release):** The downloadable release `.zip` includes the necessary FFmpeg components. No extra installations needed! (Built for Windows).
* **User-Friendly GUI**: Intuitive interface with progress tracking and emoji-based logs (ℹ️ ✅ ❌ 🚀).

---

## For Users (Using the Release Download)

### Requirements
* **Operating System**: Windows 7/8/10/11.
* **Disk Space**: Enough space for the application folder and your output files.

### Installation & Usage
1.  Go to the [**Releases Page**](https://github.com/rahmon-tech/FmpegMediaTool/releases) **<-- (Make sure this link is correct!)**.
2.  Download the latest `.zip` file (e.g., `FMpeg-MediaTool-v1.0-Windows.zip`).
3.  **Unzip** the entire folder to a location on your computer (e.g., right-click > "Extract All...").
4.  Open the extracted folder (it will likely be named `FMpeg Tool`).
5.  Run `FMpeg Tool.exe` **from inside this folder**.
    * **Important:** Do *not* move the `.exe` file out of its folder, as it needs the other bundled files (like `ffmpeg.exe`, `ffprobe.exe`, and the `_internal` folder) to work.
6.  Click **Select Videos** to choose your files.
7.  Use the tabs (**Convert & Unique-ize**, **Audio Tools**) to select your task and settings.
8.  Click **Start Processing**. Output files will appear in the same folders as the original videos, prefixed with `fmpeg_`.

---

## For Developers (Running from Source / Building)

### Requirements
* **Operating System**: Windows recommended (developed/tested on Windows). macOS/Linux may require code adjustments.
* **Python**: Python 3.8+ recommended.
* **FFmpeg & FFprobe**: You must download these separately.
    1.  Download a **static build** of FFmpeg for your OS from [ffmpeg.org](https://ffmpeg.org/download.html) or [gyan.dev](https://www.gyan.dev/ffmpeg/builds/).
    2.  Extract the downloaded archive.
    3.  Copy `ffmpeg.exe` and `ffprobe.exe` (from the `bin` folder of the extracted archive) into the **root directory** of this project (the same folder as `app.py`).

### Running from Source
1.  Ensure Python, FFmpeg, and FFprobe are set up as described above.
2.  Open your terminal or command prompt in the project's root directory.
3.  Run the application:
    ```bash
    python app.py
    ```

### Building the Executable
This project uses PyInstaller to create the distributable package.

1.  Ensure you have followed the setup steps above (Python, FFmpeg/FFprobe in the root folder).
2.  Install PyInstaller:
    ```bash
    pip install pyinstaller
    ```
3.  Run the build command from the project's root directory:
    ```bash
    pyinstaller --windowed --add-binary "ffmpeg.exe;." --add-binary "ffprobe.exe;." --name "FMpeg Tool" app.py
    ```
4.  The distributable application folder will be created in `dist/FMpeg Tool`. You can zip this folder for sharing (this is what goes into the GitHub Release).

---

## Troubleshooting
* **Error: “ffmpeg.exe or ffprobe.exe not found”**:
    * **If using the Release `.zip`**: Make sure you are running `FMpeg Tool.exe` from *inside* its original extracted folder. Do not move the `.exe` file by itself.
    * **If running from source (`python app.py`)**: Ensure `ffmpeg.exe` and `ffprobe.exe` have been downloaded and placed in the *same directory* as `app.py`.
* **Emojis not displaying**: This is cosmetic. Ensure your Windows version supports modern emojis, or install a font like Segoe UI Emoji.
* **Conversion fails**: Check the log area within the app for specific FFmpeg error messages. Ensure your input files are valid video formats.
* **Output not found**: Output files are saved in the *same folder* as their respective input files, prefixed with `fmpeg_`.

---

## Credits
* Built by [Rahmony](https://www.linkedin.com/in/rahmony).
* Powered by [FFmpeg](https://ffmpeg.org/).

## License
* **FMpeg MediaTool:** Uses the MIT License (see `LICENSE` file). Free for personal and commercial use.
* **FFmpeg:** FFmpeg itself is licensed under the LGPL/GPL (depending on the build components). See [https://ffmpeg.org/legal.html](https://ffmpeg.org/legal.html). Bundling the executables in the release build is generally permissible under these licenses for this type of application.

## Support
Report issues or suggest features via the [GitHub Issues page](https://github.com/rahmon-tech/FmpegMediaTool/issues) **<-- (Make sure this link is correct!)** or contact Rahmony via LinkedIn. Contributions and feedback are welcome!
