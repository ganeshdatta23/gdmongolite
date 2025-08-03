"""Setup script for gdmongolite"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

# Read requirements
requirements = []
try:
    with open('requirements.txt', 'r') as f:
        requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]
except FileNotFoundError:
    requirements = [
        'click>=8.1.0',
        'motor>=3.3.2',
        'pymongo>=4.6.0',
        'python-dotenv>=1.0.0',
        'pydantic[email]>=2.5.3',
        'fastapi>=0.104.0',
        'uvicorn[standard]>=0.24.0',
        'pyyaml>=6.0.1',
        'aiohttp>=3.9.0',
        'aioconsole>=0.6.1',
        'rich>=13.7.0',
        'bson>=0.5.10'
    ]

setup(
    name="gdmongolite",
    version="1.0.0",
    author="Ganesh Datta Padamata",
    author_email="ganeshdattapadamata@gmail.com",
    description="The World's Most Powerful and Easiest MongoDB Toolkit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ganeshdatta999/gdmongolite",
    project_urls={
        "Bug Tracker": "https://github.com/ganeshdatta999/gdmongolite/issues",
        "Documentation": "https://gdmongolite.readthedocs.io",
        "Source Code": "https://github.com/ganeshdatta999/gdmongolite",
    },
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Database",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP",
        "Framework :: AsyncIO",
        "Framework :: Pydantic",
        "Framework :: FastAPI",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "redis": ["aioredis>=2.0.1"],
        "all": ["aioredis>=2.0.1"],
    },
    entry_points={
        "console_scripts": [
            "gdmongolite=gdmongolite.cli:main",
        ],
    },
    keywords=[
        "mongodb", "database", "orm", "async", "pydantic", "fastapi", 
        "websockets", "caching", "security", "monitoring", "migrations", 
        "real-time", "analytics", "aggregation", "joins", "cli"
    ],
    include_package_data=True,
    zip_safe=False,
)