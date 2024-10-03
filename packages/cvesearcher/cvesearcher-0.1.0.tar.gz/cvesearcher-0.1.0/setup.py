import shutil
from setuptools import find_packages
from setuptools import setup, Command


class CleanCommand(Command):
    """Custom clean command to tidy up the project root."""
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        shutil.rmtree('build', ignore_errors=True)
        shutil.rmtree('dist', ignore_errors=True)
        shutil.rmtree('cvesearcher.egg-info', ignore_errors=True)
        # 여기에 추가로 삭제할 파일/폴더를 넣을 수 있습니다.


setup(
    name="cvesearcher",  # 패키지 이름
    version="0.1.0",  # 버전
    description="A Python library for searching CVEs using NVD API",
    author="gnuestae",
    author_email="hi563@naever.com",
    packages=find_packages(),  # 패키지 자동 검색
    install_requires=[
        "requests",
    ],
    entry_points={
        'console_scripts': [
            'cvesearch=cvesearcher.search:main',  # CLI 명령어로 실행 가능
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
