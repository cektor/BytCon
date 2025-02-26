from setuptools import setup, find_packages

setup(
    name="bytcon",  # Paket adı
    version="1.0",  # Paket sürümü
    description="BytCon (Byte Converter), between MB, GB and TB units is a tool that allows you to make easy conversions.",  # Paket açıklaması
    author="Fatih Önder",  # Paket sahibi adı
    author_email="fatih@algyazilim.com",  # Paket sahibi e-posta adresi
    url="https://github.com/cektor/BytCon",  # Paket deposu URL'si
    packages=find_packages(),  # Otomatik olarak tüm alt paketleri bulur
    install_requires=[
        'PyQt5',  
    ],
    package_data={
        'bytcon': ['*.png', '*.desktop'],  # 'kimoki' paketine dahil dosyalar
    },
    data_files=[
        ('share/applications', ['bytcon.desktop']),  # Uygulama menüsüne .desktop dosyasını ekler
        ('share/icons/hicolor/48x48/apps', ['bytconlo.png']),  # Simgeyi uygun yere ekler
    ],
    entry_points={
        'gui_scripts': [
            'bytcon=bytcon:main',  
        ]
    },
)
