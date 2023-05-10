#!/bin/bash
cd app
cd ${FILE_NAME:0:(-3)}

echo "download library..."
pip install --no-cache-dir -r requirements.txt

echo "start crawling demon..."
python3 $FILE_NAME
