import pymysql
from bs4 import BeautifulSoup
import time  # 実行時間計測用
import csv   # CSV 書き出し用
from urllib.parse import urlparse  # URL のパスを抽出するために使用

# 実行時間の開始
start_time = time.time()

# MySQL への接続
connection = pymysql.connect(
    host='c0a22103-migratipn.a910.tak-cslab.org',
    user='wp_user',
    password='CDSL_2024',
    database='wordpress'
)

# データ取得
cursor = connection.cursor()
cursor.execute("""
    SELECT ID, post_title, post_content
    FROM wp_posts
    WHERE post_type = 'post'
      AND post_status = 'publish'
      AND post_content LIKE '%<img%>';
""")
posts = cursor.fetchall()

# HTML 解析と CSV 書き出し準備
total_images = 0  # 画像の総数をカウント
output_file = "result.csv"  # 出力ファイル名

with open(output_file, mode='w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    # ヘッダーを書き出し
    csvwriter.writerow(["Post ID", "Image URL"])

    for post in posts:
        post_id, post_title, post_content = post
        soup = BeautifulSoup(post_content, 'html.parser')
        images = [img['src'] for img in soup.find_all('img') if 'src' in img.attrs]

        for image_url in images:
            # URL のパスを抽出し、uploads 以下の部分を取得
            parsed_url = urlparse(image_url)
            path = parsed_url.path
            if "/uploads/" in path:
                uploads_path = path.split("/uploads/")[1]  # uploads 以下を取得
                # CSV に書き出し (Post ID と uploads_path のみ)
                csvwriter.writerow([post_id, uploads_path])
                total_images += 1

# 接続終了
cursor.close()
connection.close()

# 実行時間の終了
end_time = time.time()

# 実行時間の表示
execution_time = end_time - start_time
print(f"\nTotal Images Extracted: {total_images}")  # 総数を表示
print(f"Script Execution Time: {execution_time:.2f} seconds")
print(f"Results saved to: {output_file}")