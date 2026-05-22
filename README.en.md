[Chinese](README.md)

# FOMC Federal Reserve Press Conference Video Downloader

Tool for fetching metadata and automatically downloading FOMC Federal Reserve press conference videos from YouTube for academic research purposes.

> **Project Note**: This tool was developed for academic research. For personal learning and research use only.

---

## Features

- `1_fetch_metadata.py`: Fetch video metadata (title, duration, upload date, etc.) from the Federal Reserve YouTube channel.
- `2_download_videos.py`: Automatically filter and download FOMC press conference videos with concurrent downloading and progress bar.

## How to Use

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Fetch Metadata

```bash
python 1_fetch_metadata.py
```

This will generate `fed_raw_metadata.xlsx`.

### 3. Download Videos

```bash
python 2_download_videos.py
```

The script will automatically filter videos containing "Press Conference" and start downloading.

## Configuration

- Download directory defaults to `raw_videos` folder in the project root (can be modified in the code).
- Supports concurrent downloads (default: 4 threads).
- Already downloaded videos will be skipped automatically.

## Project Background

This tool was developed as part of academic research on FOMC communications.

## License

MIT License