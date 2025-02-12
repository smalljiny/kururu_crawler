#!/bin/bash

# 가상환경이 이미 존재하는 경우 삭제
if [ -d "crawler" ]; then
    rm -rf crawler
fi

# 가상환경 생성
python3 -m venv crawler

# 가상환경 활성화
source crawler/bin/activate

# pip 업그레이드
pip install --upgrade pip

# 필요한 패키지 설치
pip install -r requirements.txt

echo "패키지 설치 완료 및 가상환경 활성화됨"