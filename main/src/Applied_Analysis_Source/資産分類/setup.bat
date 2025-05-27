@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

echo 資産開発言語判定ツール セットアップ
echo ====================================

:: Python環境の確認
python --version 2>nul
if errorlevel 1 (
    echo Python が見つかりません。Python 3.8以上をインストールしてください。
    exit /b 1
)

:: GPU環境の確認
echo GPUの確認中...
python -c "import torch; print('CUDA利用可能:' if torch.cuda.is_available() else 'CPU使用:')"

:: 必要なライブラリのインストール
echo 必要なライブラリをインストールしています...
pip install -r requirement.txt
if errorlevel 1 (
    echo ライブラリのインストールに失敗しました。
    exit /b 1
)

:: 設定情報の収集
echo.
echo 設定情報の収集を開始します...
echo ====================================

:: OpenAI設定
set /p OPENAI_KEY="OpenAI APIキーを入力してください: "
echo OpenAIキーの検証中...
python -c "import openai; openai.api_key='%OPENAI_KEY%'; openai.models.list()" 2>nul
if errorlevel 1 (
    echo OpenAIキーの検証に失敗しました。
    set OPENAI_KEY=dummy-key
)

:: Anthropic設定
set /p ANTHROPIC_KEY="Anthropic APIキーを入力してください: "
echo Anthropicキーの検証中...
python -c "import anthropic; client=anthropic.Anthropic(api_key='%ANTHROPIC_KEY%')" 2>nul
if errorlevel 1 (
    echo Anthropicキーの検証に失敗しました。
    set ANTHROPIC_KEY=dummy-key
)

:: データベース設定
set /p DB_HOST="データベースホストを入力してください [localhost]: "
if "!DB_HOST!"=="" set DB_HOST=localhost
set /p DB_PORT="データベースポートを入力してください [5432]: "
if "!DB_PORT!"=="" set DB_PORT=5432
set /p DB_NAME="データベース名を入力してください [asset_management]: "
if "!DB_NAME!"=="" set DB_NAME=asset_management
set /p DB_USER="データベースユーザーを入力してください [asset_user]: "
if "!DB_USER!"=="" set DB_USER=asset_user
set /p DB_PASS="データベースパスワードを入力してください: "

:: クラウドストレージ設定
echo.
echo クラウドストレージの設定
echo ====================================

:: Azure設定
set /p AZURE_CONN_STR="Azure Storage接続文字列を入力してください: "
python -c "from azure.storage.blob import BlobServiceClient; BlobServiceClient.from_connection_string('%AZURE_CONN_STR%')" 2>nul
if errorlevel 1 (
    echo Azure接続の検証に失敗しました。
    set AZURE_CONN_STR=DefaultEndpointsProtocol=https;...
)

:: AWS設定
set /p AWS_ACCESS_KEY="AWS Access Keyを入力してください: "
set /p AWS_SECRET_KEY="AWS Secret Keyを入力してください: "
python -c "import boto3; boto3.client('s3',aws_access_key_id='%AWS_ACCESS_KEY%',aws_secret_access_key='%AWS_SECRET_KEY%')" 2>nul
if errorlevel 1 (
    echo AWS接続の検証に失敗しました。
    set AWS_ACCESS_KEY=dummy-key
    set AWS_SECRET_KEY=dummy-secret
)

:: 設定ファイルの生成
echo 設定ファイルを生成中...
python -c "
import yaml
config = {
    'model': {'name': 'microsoft/codebert-base', 'threshold': 0.9, 'max_length': 512},
    'ai_services': {
        'openai': {'api_key': '%OPENAI_KEY%', 'model': 'gpt-4'},
        'anthropic': {'api_key': '%ANTHROPIC_KEY%', 'model': 'claude-3-opus-20240229'}
    },
    'databases': {
        'asset_db': {
            'host': '%DB_HOST%', 'port': %DB_PORT%, 'database': '%DB_NAME%',
            'user': '%DB_USER%', 'password': '%DB_PASS%'
        }
    },
    'cloud_services': {
        'azure': {'connection_string': '%AZURE_CONN_STR%'},
        'aws': {'access_key': '%AWS_ACCESS_KEY%', 'secret_key': '%AWS_SECRET_KEY%'}
    }
}
with open('config.yml', 'w', encoding='utf-8') as f:
    yaml.dump(config, f, allow_unicode=True, sort_keys=False)
"

if errorlevel 1 (
    echo 設定ファイルの生成に失敗しました。
    exit /b 1
)

:: プロジェクト構造の初期化
echo.
echo プロジェクト構造を初期化しています...
python -m util.setup
if errorlevel 1 (
    echo プロジェクト構造の初期化に失敗しました。
    exit /b 1
)

:: セットアップ完了
echo.
echo セットアップが完了しました。
echo 設定ファイル（config.yml）を確認し、必要に応じて編集してください。
pause
