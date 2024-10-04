# setup.py
from setuptools import setup, Extension, find_packages
from Cython.Build import cythonize

extensions = [
    Extension(
        "vnstockdata.config.config",  # Tên module cho file config.c
        ["vnstockdata/config/config.c"]  # Đường dẫn đến file config.c
    ),
    Extension(
        "vnstockdata.config.ensure_logged_in",  # Tên module cho file ensure_logged_in.c
        ["vnstockdata/config/ensure_logged_in.c"]  # Đường dẫn đến file ensure_logged_in.c
    ),
    Extension(
        "vnstockdata.process_client.login",  # Tên module cho file login.c
        ["vnstockdata/process_client/login.c"]  # Đường dẫn đến file login.c
    ),
    Extension(
        "vnstockdata.process_stock.ohlcv",  # Tên module cho file trong thư mục stock/price
        ["vnstockdata/process_stock/ohlcv.c"]  # Đường dẫn đến file price.c
    )
]

setup(
    name="vnstockdata",  # Tên gói sử dụng dấu gạch dưới
    version="1.0.5",
    author="vnstockdata.com",
    author_email="support@vnstockdata.com",
    description="Dữ liệu thị trường chứng khoán Việt Nam",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://vnstockdata.com",
    include_package_data=True,
    packages=find_packages(),
    ext_modules=cythonize(
        extensions, 
        compiler_directives={
            'language_level': "3",
            "embedsignature":True}),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
    install_requires=[
        "pandas==2.1.2",
        "requests",
       
    ],
)
