# Fmpeg MediaTool v1.0

A user-friendly GUI application for batch video processing, powered by FFmpeg. Convert videos to various formats, extract audio, mute videos, or apply random filters to create unique outputs. Perfect for casual users and video enthusiasts!

## Features
- **Batch Conversion**: Convert videos to MP4, MKV, MOV, GIF, or AVI.
- **GIF Customization**: Adjust GIF width (100–1000px) and framerate (5–30 FPS).
- **Audio Tools**: Extract audio to MP3 or mute videos instantly.
- **Unique-izer**: Apply random filters (resolution, gamma, saturation, brightness, volume) for unique video outputs.
- **User-Friendly GUI**: Intuitive interface with progress tracking and emoji-based logs (ℹ️ for info, ✅ for success, ❌ for errors).
- **Output Handling**: Saves files in the same directory as inputs with an `ffmpeg_` prefix.

## Requirements
- **Operating System**: Windows 10/11 (macOS/Linux may work with modifications).
- **Dependencies**:
  - `ffmpeg.exe` and `ffprobe.exe` (must be in the same folder as the app; download from https://ffmpeg.org/download.html).
  - Python 3.6+ with Tkinter (if running from source).
- **Disk Space**: Enough space for input and output files.

## Installation
1. Download the latest release from [GitHub link or other source].
2. Extract the ZIP file to a folder.
3. Ensure `ffmpeg.exe` and `ffprobe.exe` are in the same folder as `FmpegMediaTool.exe`. Download from https://ffmpeg.org/download.html if not included.
4. Run `FmpegMediaTool.exe`. For source users, run `python app.py` after installing Python and Tkinter.

## Usage
1. Launch the app and click **Select Videos** to choose video files.
2. In the **Convert & Unique-ize** tab:
   - Select a format (e.g., `.gif`, `.mp4`).
   - Adjust resolution (e.g., 1080p, 720p) or keep original.
   - Set quality (CRF 18–30, lower is better) or GIF settings (width, FPS).
   - Check **Apply Random Filters** for unique outputs (optional).
3. In the **Audio Tools** tab, choose **Extract Audio (.mp3)** or **Remove Audio (Mute Videos)**.
4. Click **Start Processing** and monitor progress in the log area.
5. Find output files in the same folder as inputs (e.g., `ffmpeg_video.mp4`, `ffmpeg_video_audio.mp3`).

## Troubleshooting
- **Error: “ffmpeg.exe or ffprobe.exe not found”**: Ensure both files are in the app’s folder. Download from https://ffmpeg.org/download.html.
- **Emojis not displaying**: Use Windows 10/11 or a font like Segoe UI Emoji. Contact support if issues persist.
- **Conversion fails**: Check the log area for FFmpeg error details. Ensure input files are valid and accessible.
- **Output not found**: Outputs save in the same folder as inputs. Check for `ffmpeg_` prefix in filenames.

## Credits
- Built by Rahmony (https://www.linkedin.com/in/rahmony).
- Powered by FFmpeg (https://ffmpeg.org/).

## License
Fmpeg MediaTool is free for personal use. FFmpeg is distributed under the GPL license; see https://ffmpeg.org/legal.html for details.

## Support
Report issues or suggest features at [GitHub link] or contact Rahmony at https://www.linkedin.com/in/rahmony. Contributions and feedback are welcome!

