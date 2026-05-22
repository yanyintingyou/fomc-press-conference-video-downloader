# -*- coding: utf-8 -*-

import yt_dlp
import pandas as pd
from datetime import datetime

# --- 配置区域 ---
CHANNEL_URL = "https://www.youtube.com/@federalreserve/videos" 
OUTPUT_EXCEL = "fed_raw_metadata.xlsx" 

def fetch_metadata():
    print(f"[{datetime.now().strftime('%H:%M:%S')}] 开始抓取元数据，请稍候...")
    
    # yt-dlp 配置：只抓列表，不下载视频
    ydl_opts = {
        'extract_flat': True,       # 关键：仅提取元数据
        'dump_single_json': True,   # 输出单一JSON结构以便解析
        'quiet': True,              
        'ignoreerrors': True,       
        # 伪装成浏览器
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    }

    video_data = []

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            # 抓取频道信息
            info = ydl.extract_info(CHANNEL_URL, download=False)
            
            if 'entries' in info:
                entries = info['entries']
                print(f"[{datetime.now().strftime('%H:%M:%S')}] 频道扫描完成，共发现 {len(entries)} 个视频。")
                print("正在解析数据...")
                
                for entry in entries:
                    # 提取关键字段
                    video_data.append({
                        'title': entry.get('title', 'N/A'),
                        'id': entry.get('id', 'N/A'),
                        'url': entry.get('url', 'N/A'),
                        'duration': entry.get('duration', 0),
                        'upload_date': entry.get('upload_date', 'N/A'),
                        'view_count': entry.get('view_count', 0)
                    })
            else:
                print("未找到视频列表，请检查 URL。")

        except Exception as e:
            print(f"发生错误: {e}")

    return video_data


def save_to_excel(data):
    if not data:
        print("没有数据可保存。")
        return

    df = pd.DataFrame(data) 
    
    # 数据清洗：构造完整的 URL
    if 'id' in df.columns:
        df['full_url'] = df['id'].apply(lambda x: f"https://www.youtube.com/watch?v={x}")
    else:
        df['full_url'] = df['url'] if 'url' in df.columns else 'N/A'
    
    # 格式化日期
    if 'upload_date' in df.columns:
        df['upload_date'] = pd.to_datetime(df['upload_date'], format='%Y%m%d', errors='coerce')
    
    # 筛选列顺序
    desired_cols = ['upload_date', 'title', 'duration', 'full_url', 'id', 'view_count']
    existing_cols = [c for c in desired_cols if c in df.columns]
    df = df[existing_cols]
    
    # 按日期降序排列
    if 'upload_date' in df.columns:
        df = df.sort_values(by='upload_date', ascending=False)

    print(f"[{datetime.now().strftime('%H:%M:%S')}] 正在保存到 {OUTPUT_EXCEL} ...")
    df.to_excel(OUTPUT_EXCEL, index=False)
    print(f"文件已保存。")


if __name__ == "__main__":
    data = fetch_metadata()
    save_to_excel(data)