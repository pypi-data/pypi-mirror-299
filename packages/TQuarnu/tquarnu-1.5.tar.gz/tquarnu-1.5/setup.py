from setuptools import setup, find_packages

setup(
    name="TQuarnu",
    version="1.5",
    packages=find_packages(),
    description="A modern and advanced Quran library for Arabic text and Tafsir",
    long_description=open("readme.md").read(),
    long_description_content_type="text/markdown",
    url="",
    author="Khattab Aluqba",
    author_email="",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    include_package_data=True,  # تفعيل تضمين ملفات البيانات
    package_data={
        "TQuranu": ["quran.json", "tafser.json"],
    },
)
