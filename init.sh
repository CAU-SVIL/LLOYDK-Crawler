#!/bin/bash
pip install --no-cache-dir -r requirements.txt
cd app
echo "start crawling demon..."
python3 $FILE_NAME