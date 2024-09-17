chmod +x run.sh&./run.sh
# Tải file từ GitHub
wget -q https://github.com/albumentations-team/albumentations_examples/archive/main.zip -O /tmp/albumentations_examples-main.zip

# Giải nén file zip
unzip -o -qq /tmp/albumentations_examples-main.zip -d /Users/apple/Desktop/mtips5s_albumentation

# Sao chép thư mục images vào thư mục hiện tại
cp -r /Users/apple/Desktop/mtips5s_albumentation/albumentations_examples-main/notebooks/images /Users/apple/Desktop/mtips5s_albumentation
