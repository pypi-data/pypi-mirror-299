# setup.py
from setuptools import setup, Extension, find_packages
from Cython.Build import cythonize

extensions = [
    Extension(
        "vnstockdata.config.config",  # Tên module cho file config.pyx
        ["vnstockdata/config/config.pyx"]  # Đường dẫn đến file config.pyx
    ),
    Extension(
        "vnstockdata.config.ensure_logged_in",  # Tên module cho file ensure_logged_in.pyx
        ["vnstockdata/config/ensure_logged_in.pyx"]  # Đường dẫn đến file ensure_logged_in.pyx
    ),
    Extension(
        "vnstockdata.client.login",  # Tên module cho file login.pyx
        ["vnstockdata/client/login.pyx"]  # Đường dẫn đến file login.pyx
    ),
    Extension(
        "vnstockdata.stock.price",  # Tên module cho file trong thư mục stock/price
        ["vnstockdata/stock/price.pyx"]  # Đường dẫn đến file price.pyx
    )
]

setup(
    name="library_test",  # Tên gói sử dụng dấu gạch dưới
    version="0.5.16",
    author="vnstockdata.com",
    author_email="support@vnstockdata.com",
    description="Mô tả thư viện của bạn",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://vnstockdata.com",
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
    python_requires='>=3.8',
    install_requires=[
        "pandas==2.1.2",
        "requests",
        # Thêm bất kỳ thư viện nào khác mà bạn cần
    ],
)
