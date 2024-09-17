#!/bin/bash
# Kiểm tra các refix test_ có còn lỗi không
pytest --cov=project

# Tạo report cho tất cả các file có trong src
pytest --cov=src --cov-report=html