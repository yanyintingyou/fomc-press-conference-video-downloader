import pandas as pd
import random
import yt_dlp
import os
import re
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

# --- 配置区域 ---
METADATA_FILE = "fed_raw_metadata.xlsx"
CHECKLIST_FILE = "fed_targets_checklist.xlsx"

# 下载目录（相对路径，建议放在项目根目录下或 data/raw_videos 中）
DOWNLOAD_DIR = "raw_videos"
MAX_WORKERS = 4  # 并发线程数


def extract_date_from_title(title):
    """
    从标题中提取日期 
    """
    pattern = r'(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}'
    match = re.search(pattern, title, re.IGNORECASE)
    
    if match:
        date_str = match.group(0).replace(',', '') 
        try:
            dt = datetime.strptime(date_str, '%B %d %Y')
            return dt.strftime('%Y-%m-%d')
        except ValueError:
            return "Unknown_Date"
    return "Unknown_Date"


def filter_videos(df):
    print("正在筛选目标视频...")
    mask_title = df['title'].str.contains("Press Conference", case=False, na=False)
    mask_exclude = ~df['title'].str.contains("Introductory Statement", case=False, na=False)
    mask_duration = df['duration'] > 800
    
    target_df = df[mask_title & mask_exclude & mask_duration].copy()
    
    print("正在从标题修复日期格式...")
    target_df['date_str'] = target_df['title'].apply(extract_date_from_title)
    target_df = target_df.sort_values(by='date_str', ascending=False)

    print(f"从 {len(df)} 个视频中找到了 {len(target_df)} 个目标发布会视频。")
    return target_df


def download_single_video(row):
    date_prefix = row['date_str']
    if date_prefix == "Unknown_Date":
        date_prefix = f"Unknown_{row.get('id', 'NoID')}"
    
    video_url = row['full_url']
    safe_title = re.sub(r'[\\/*?:"<>|]', "", row['title'])
    safe_title = safe_title.replace(" ", "_")
    file_name = f"{date_prefix}_{safe_title}.mp4"
    output_path = os.path.join(DOWNLOAD_DIR, file_name)
    
    sleep_time = random.uniform(0.5, 2)
    time.sleep(sleep_time)
    
    ydl_opts = {
        'format': 'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': os.path.join(DOWNLOAD_DIR, f"{row['date_str']}_{safe_title}.%(ext)s"),
        'quiet': True, 
        'no_warnings': True,
        'ignoreerrors': True,
        'no_overwrites': True,
        'concurrent_fragment_downloads': 4,
        'merge_output_format': 'mp4',
    }
    
    try:
        if os.path.exists(output_path):
            tqdm.write(f"⏭️ [跳过] {file_name} (已存在)")
            return "Skipped"
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
            
        tqdm.write(f"✅ [完成] {file_name}")
        return "Success"
        
    except Exception as e:
        tqdm.write(f"❌ [失败] {file_name} : {e}")
        return "Failed"


def main():
    if not os.path.exists(DOWNLOAD_DIR):
        os.makedirs(DOWNLOAD_DIR)
        
    # 读取与筛选
    try:
        df = pd.read_excel(METADATA_FILE)
    except FileNotFoundError:
        df = pd.read_csv(METADATA_FILE.replace(".xlsx", ".csv"))
    except Exception as e:
        print(f"读取文件失败: {e}")
        return

    targets = filter_videos(df)
    
    print(f"正在保存筛选结果到: {CHECKLIST_FILE} ...")
    try:
        save_cols = ['date_str', 'title', 'duration', 'full_url', 'id']
        actual_cols = [c for c in save_cols if c in targets.columns]
        targets[actual_cols].to_excel(CHECKLIST_FILE, index=False)
        print("清单保存成功！")
    except Exception as e:
        print(f"清单保存失败: {e}")
    
    print("\n即将下载视频：")
    print(targets[['title', 'duration', 'date_str']])
    
    user_input = input(f"\n确认要开始下载这 {len(targets)} 个视频吗？(y/n): ")
    if user_input.lower() != 'y':
        print("已取消。")
        return

    print(f"\n启动并发下载 (线程数: {MAX_WORKERS})...")
    
    video_list = targets.to_dict('records')
    
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(download_single_video, video) for video in video_list]
        
        for _ in tqdm(as_completed(futures), total=len(video_list), unit="v", desc="总进度"):
            pass

    print("\n所有下载任务完成，请检查文件夹。")


if __name__ == "__main__":
    main()