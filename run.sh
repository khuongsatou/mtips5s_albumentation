#!/bin/bash

# Tạo file note
echo "chmod +x run.sh&./run.sh" > readme.md

# Tạo file requirements.txt và thêm các gói cần thiết
echo "flask" > requirements.txt
echo "requests" >> requirements.txt
echo "numpy" >> requirements.txt
echo "pandas" >> requirements.txt
echo "pytest" >> requirements.txt
echo "pytest-cov" >> requirements.txt

# Tạo môi trường ảo
python3 -m venv env

# Kích hoạt môi trường ảo
source env/bin/activate

# Cài đặt các gói từ file requirements.txt
pip install -r requirements.txt

