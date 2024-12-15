# MigrationFaster
# README

このリポジトリには、WordPressの投稿コンテンツから画像ファイルを抽出し、未使用の画像を削除するための2つのPythonスクリプトが含まれています。

## スクリプト一覧

1. `file-search.py`
2. `remove-png.py`

### file-search.py

このスクリプトは、WordPressのMySQLデータベースから画像を含む投稿を検索し  
各投稿内の画像URLを抽出してCSVファイルに保存します。

#### 使用方法

1. 必要なパッケージをインストールします
```sh
pip install pymysql beautifulsoup4
```

2. スクリプト内のデータベース接続情報を変更します
```Python
connection = pymysql.connect(
  host='YOUR_DATABASE_HOST',
  user='YOUR_DATABASE_USER',
  password='YOUR_DATABASE_PASSWORD',
  database='YOUR_DATABASE_NAME'
)
```

3. スクリプトを実行します
```Python
python file-search.py
```
 
4. result.csv という名前のCSVファイルに結果が保存されます
   スクリプトの詳細
- WordPressデータベースに接続し、wp_postsテーブルから画像を含む投稿を取得します
- BeautifulSoupを使用してHTMLコンテンツから画像URLを抽出します
- 画像URLのうち、/uploads/ディレクトリ内のパスをCSVファイルに書き出します

### remove-png.py

このスクリプトは、result.csvに記載された画像ファイル以外の画像をWordPressのuploadsディレクトリから削除します。

#### 使用方法

1. スクリプト内のディレクトリパスとCSVファイルのパスを変更します。
```Python
uploads_dir = "/path/to/wp-content/uploads"
csv_file = "path/to/result.csv"
```

2. スクリプトを実行します。
```Python
python remove-png.py
```

3. 実行結果として、削除されたファイルのリストが表示されます。
スクリプトの詳細
- result.csvから使用中の画像ファイルパスを読み込み、セットに保存します
- uploadsディレクトリを再帰的に走査し、CSVに含まれない画像ファイルを削除します
- 削除されたファイルのリストと実行時間を表示します

#### 注意事項
スクリプトを実行する前に、必ずデータベースとuploadsディレクトリのバックアップを取ってください。
ファイルの削除操作は不可逆であるため、十分に注意して実行してください。
