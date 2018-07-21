#!/bin/bash

echo "HMM模型生成中..."
python3 main.py

echo -e "...\n...\n...\n"

echo "数据对比中......"
# 显示模型评估信息
cd ./data/icwb2-data/scripts/ 
./command.sh 
