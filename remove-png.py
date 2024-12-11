import os
import csv
import time  # 実行時間計測用

# 対象ディレクトリ
uploads_dir = "/var/www/html/wp-content/uploads"
# CSV ファイルのパス
csv_file = "result.csv"

# 使用する画像拡張子のリスト
valid_extensions = {'.png', '.jpeg', '.jpg'}

# CSV から使用中の画像ファイルパスを読み込む
def load_used_images(csv_file):
    used_images = set()
    with open(csv_file, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # ヘッダーをスキップ
        for row in reader:
            if len(row) == 2:  # "Post ID" と "Image URL" の形式を確認
                used_images.add(row[1])
    return used_images

# ディレクトリ内の画像ファイルを削除
def delete_unused_images(uploads_dir, used_images):
    removed_files = []
    for root, dirs, files in os.walk(uploads_dir):
        for file in files:
            # ファイルの拡張子を取得
            file_extension = os.path.splitext(file)[1].lower()

            # 画像ファイル（png, jpeg, jpg）のみ対象
            if file_extension in valid_extensions:
                file_path = os.path.relpath(os.path.join(root, file), uploads_dir)
                # ファイルが使用されていない場合削除
                if file_path not in used_images:
                    full_path = os.path.join(root, file)
                    try:
                        os.remove(full_path)
                        removed_files.append(full_path)
                    except PermissionError as e:
                        print(f"PermissionError: {e} - {full_path}")
    return removed_files

# メイン処理
def main():
    # 実行時間の開始
    start_time = time.time()
    
    # 使用されている画像をロード
    used_images = load_used_images(csv_file)
    print(f"Total Used Images in CSV: {len(used_images)}")
    
    # 使用されていない画像を削除
    removed_files = delete_unused_images(uploads_dir, used_images)
    print(f"Total Removed Files: {len(removed_files)}")
    
    # 削除されたファイルを表示
    if removed_files:
        print("\nRemoved Files:")
        for file in removed_files:
            print(file)
    
    # 実行時間の終了
    end_time = time.time()
    
    # 実行時間の表示
    execution_time = end_time - start_time
    print(f"\nScript Execution Time: {execution_time:.2f} seconds")

if __name__ == "__main__":
    main()