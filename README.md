# PDF Audio Reader with Pause/Resume

A Python GUI application that reads PDF content aloud with real-time page tracking and pause/resume functionality(tested for Macbook)Devices.


## Features

- **Text-to-Speech Conversion**  
  Reads PDF content aloud using system voices
- **Page Tracking**  
  Displays current page being read in real-time
- **Pause/Resume Control**  
  Allows interrupting and continuing playback
- **Custom Start Page**  
  Begin reading from any specified page number
- **Cross-Platform**  
  Works on Windows, macOS, and Linux
- **Voice Configuration**  
  Supports custom voice selection and speech rate

## Technologies

- Python 3.10+
- PyPDF2 (PDF text extraction)
- pyttsx3 (Text-to-speech engine)
- Tkinter (GUI interface)

## Installation

1. **Prerequisites**  
   Ensure Python 3.10+ is installed:


2. **Install Dependencies**  
pip install PyPDF2 pyttsx3
## Usage

1. **Launch Application** 
python text2speech-UI.py


2. **Interface Guide**  
- Click "Open PDF" to select your document
- Enter starting page number (default: 1)
- Click "Start" to begin reading
- Use "Pause/Resume" button during playback

3. **Controls**  
- **Start**: Begins reading from specified page
- **Pause**: Temporarily stops playback
- **Resume**: Continues from last paused position
- **Page Display**: Shows current page being read

## Troubleshooting

**Common Issues**  
- **No Audio Output**  
- Verify system audio is working
- Check terminal/app has microphone access
- Test with `python -c "import pyttsx3; e=pyttsx3.init(); e.say('test'); e.runAndWait()"`

- **Partial Text Extraction**  
- Ensure PDF contains selectable text (not scanned images)
- Try alternative PDF libraries (PyMuPDF) if needed

- **Voice Not Available**  
- List available voices with:
 ```
 import pyttsx3
 print([v.name for v in pyttsx3.init().getProperty('voices')])
 ```

## Development

**Future Enhancements**
- [ ] Save/Load reading progress
- [ ] Bookmark system
- [ ] Speed control slider
- [ ] Multiple voice profiles

