from setuptools import setup, find_packages

setup(
    name="quranu",  # اسم الحزمة
    version="0.1.0",  # الإصدار الأول
    packages=find_packages(),  # البحث عن جميع الحزم والموديولات
    description="A modern and advanced Quran library for Arabic text and Tafsir",
    long_description=open("readme.md").read(),
    long_description_content_type="text/markdown",
    url="",  # رابط المستودع الخاص بك
    author="Khattab Aluqba",
    author_email="",
    license="MIT",  # الرخصة
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',  # الحد الأدنى من إصدار Python
    include_package_data=True,  # يشمل بيانات مثل ملفات JSON
    package_data={
        "quranu": ["quran.json", "tafser.json"],  # تضمين ملفات JSON
    },
)
