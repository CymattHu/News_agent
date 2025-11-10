#!/usr/bin/env bash
set -e
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env .env || true
echo "虚拟环境创建完成。编辑 .env 填入 OPENAI_API_KEY 后运行： python -m src.llm_agent"
