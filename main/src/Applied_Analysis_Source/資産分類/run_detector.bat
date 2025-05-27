@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

echo 資産開発言語判定ツール
echo ====================

:: 引数チェック
if "%~1"=="" (
    echo 使用方法: run_detector.bat 入力フォルダパス [出力ファイル名]
    echo 例: run_detector.bat C:\input C:\output\result.xlsx
    exit /b 1
)

:: 出力ファイル名の設定
set OUTPUT=%~2
if "%OUTPUT%"=="" set OUTPUT=output\result.xlsx

:: 入力フォルダの存在チェック
if not exist "%~1" (
    echo 入力フォルダ "%~1" が見つかりません。
    exit /b 1
)

:: 出力ディレクトリの作成
for %%F in ("%OUTPUT%") do (
    if not exist "%%~dpF" mkdir "%%~dpF"
)

:: ツールの実行
echo 処理を開始します...
python asset_language_detector.py --input-dir "%~1" --output "%OUTPUT%"
if errorlevel 1 (
    echo 処理中にエラーが発生しました。
    exit /b 1
)

echo 処理が完了しました。
echo 結果ファイル: %OUTPUT%
pause
