#!/bin/bash

# 作業ディレクトリに移動
#cd /path/to/your/dir || exit

# Pythonスクリプトを実行
python3 update.py

# Git操作
# git add .
# git commit -m "Automated update $(date '+%Y-%m-%d %H:%M:%S')"
# git push

# エラーハンドリング
if [ $? -ne 0 ]; then
    echo "Error occurred during Git operations" >&2
    exit 1
fi

echo "Update completed successfully"