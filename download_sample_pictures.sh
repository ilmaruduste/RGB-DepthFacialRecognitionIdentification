mkdir picture_data
cd picture_data
python -c "import gdown; gdown.download('https://drive.google.com/uc?id=169j2ClELErqvTrlGJztbea_ceaIBlE9z', 'sample_pictures.zip', quiet=False)"
unzip sample_pictures.zip
rm sample_pictures.zip