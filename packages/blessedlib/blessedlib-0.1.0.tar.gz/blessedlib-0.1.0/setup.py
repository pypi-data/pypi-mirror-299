from setuptools import setup, find_packages

setup(
    name="blessedlib",  # اسم المكتبة
    version="0.1.0",  # إصدار المكتبة
    description="A library for cracking hashes, developed by Team Blessed",
    author="blessed",
    author_email="example@example.com",
    packages=find_packages(),  # جميع الحزم التي سيتم تضمينها في المكتبة
    install_requires=['hashlib'],  # المكتبات المطلوبة لتشغيل مكتبتك
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # الحد الأدنى من إصدار بايثون المطلوب
)
