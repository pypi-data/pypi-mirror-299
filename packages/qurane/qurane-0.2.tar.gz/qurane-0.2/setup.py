from setuptools import setup, find_packages

setup(
    name="qurane",
    version="0.2",
    packages=find_packages(),
    description="A modern and advanced Quran library for Arabic text and Tafsir",
    long_description=open("readme.md").read(),
    long_description_content_type="text/markdown",
    url="",
    author="Khattab_Aluqba",
    author_email="exmidleg@gmail.com",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    include_package_data=True,  # تفعيل تضمين ملفات البيانات
    package_data={  # تعريف ملفات البيانات داخل الحزمة
        "qurane": ["quran.json", "tafser.json"],
    },
)