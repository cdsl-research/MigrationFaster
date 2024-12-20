# MigrationFaster

このリポジトリには, WordPressの投稿コンテンツから画像ファイルを抽出し, 未使用の画像を削除するための2つのPythonプログラムが含まれています.

## プログラム一覧

1. `file-search.py`
2. `remove-png.py`

### 前提条件
Pythonの仮想環境をもちいて, 必要なパッケージをpipでインストールする必要があります.
```cmd
python3 -m venv .venv
source .venv/bin/activate

pip3 install -U pip
pip3 install -r requirements.txt
```

### file-search.py

このプログラムは, WordPressのMySQLデータベースから画像を含む投稿を検索し  
各投稿内の画像URLを抽出してCSVファイルに保存します.

#### 使用方法

1. プログラム内のデータベース接続情報を変更します
```Python
connection = pymysql.connect(
  host='YOUR_DATABASE_HOST',
  user='YOUR_DATABASE_USER',
  password='YOUR_DATABASE_PASSWORD',
  database='YOUR_DATABASE_NAME'
)
```

2. プログラムを実行します
```cmd
python file-search.py
```
 
3. result.csv という名前のCSVファイルに結果が保存されます
   プログラムの詳細
- WordPressデータベースに接続し, wp_postsテーブルから画像を含む投稿を取得します
- BeautifulSoupを使用してHTMLコンテンツから画像URLを抽出します
- 画像URLのうち, ~/uploads/ディレクトリ内のパスをCSVファイルに書き出します

#### 出力結果
```cmd
(.venv) nissy@c0a22103-migratipn:~/jikken$ python3 sql-test.py

Total Images Extracted: 802
Script Execution Time: 0.25 seconds
Results saved to: result.csv
```
![Filesearch Console](img/filesearch-console.png)


### remove-png.py

このプログラムは, result.csvに記載された画像ファイル以外の画像をWordPressのuploadsディレクトリから削除します.

#### 使用方法

1. プログラム内のディレクトリパスとCSVファイルのパスを変更します.
```Python
uploads_dir = "/path/to/wp-content/uploads"
csv_file = "path/to/result.csv"
```

2. プログラムを実行します.
```cmd
python remove-png.py
```

3. 実行結果として, 削除されたファイルのリストが表示されます.
プログラムの詳細
- result.csvから使用中の画像ファイルパスを読み込み, セットに保存します
- uploadsディレクトリを再帰的に走査し, CSVに含まれない画像ファイルを削除します
- 削除されたファイルのリストと実行時間を表示します


#### 出力結果

![Begin Remove Console](img/filesearch-console-begin.png)
出力量が多いため, 一部のみ掲載します.
```cmd
/tmp/var/www/html/wp-content/uploads/2024/09/IMG_1388.jpg
                        ・
                        ・
                        ・
/tmp/var/www/html/wp-content/uploads/2024/09/IMG_5611-1-600x450.jpg
```
![Remove Console](img/remove-console.png)


