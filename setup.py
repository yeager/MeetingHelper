from setuptools import setup, find_packages

setup(
    name="meetinghelper",
    version="1.0.0",
    description="Visuellt mötesprotokoll för LSS/vårdplanering",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="MeetingHelper",
    license="MIT",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "PyGObject>=3.42",
    ],
        package_data={
        "": ["locale/*/LC_MESSAGES/*.mo"],
    },
    entry_points={
        "console_scripts": [
            "meetinghelper=meetinghelper.app:main",
        ],
    },
    data_files=[
        ("share/applications", ["se.meetinghelper.app.desktop"]),
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Environment :: X11 Applications :: GTK",
    ],
)
