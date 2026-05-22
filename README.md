[English](README.en.md)

# FOMC 联邦储备委员会新闻发布会视频自动下载工具

用于学术研究的 FOMC 联邦储备委员会新闻发布会视频元数据抓取与自动下载工具。

> **项目说明**：本工具为学术研究目的开发，仅用于个人学习和研究使用。

---

## 功能概述

- `1_fetch_metadata.py`：从 YouTube 联邦储备频道抓取所有视频元数据（标题、时长、上传日期等）
- `2_download_videos.py`：根据筛选条件自动下载 FOMC 新闻发布会视频（支持并发下载 + 进度条）

## 使用方法

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 抓取元数据

```bash
python 1_fetch_metadata.py
```

执行后会生成 `fed_raw_metadata.xlsx` 文件。

### 3. 下载视频

```bash
python 2_download_videos.py
```

程序会自动筛选“Press Conference”相关视频并提供下载。

## 配置说明

- 下载目录默认为项目下的 `raw_videos` 文件夹（可在代码中修改）
- 支持并发下载（默认 4 线程）
- 已存在的视频会自动跳过

## 项目来源

此为学术研究目的开发的工具脚本。

## License

MIT License