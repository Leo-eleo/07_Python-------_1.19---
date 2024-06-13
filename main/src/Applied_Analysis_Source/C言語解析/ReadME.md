# README

## 依存関係をインストールする

```bash
cd <CBLTDA_TOOL root folder>

pip install -r requirements.txt
```

## 使い方

```bash
cd <CBLTDA_TOOL root folder>

python c_parse_main.py c_sources_folder db_path setting_path result_folder

# Cプログラムのビット72-80が無効なデータであり、削除する必要がある場合は、以下のコマンドを使用する。
python c_parse_main.py c_sources_folder db_path setting_path result_folder -R
```
