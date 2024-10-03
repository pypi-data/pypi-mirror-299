
from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fp:
    long_description = fp.read()

#  with open("requirements.txt", "r", encoding="utf-8") as fp:
     #  requires = [x.strip() for x in fp.readlines()]

setup(name="theia-api",
      version="1.0.3",
      author="iprintf",
      author_email="iprintf@qq.com",
      url="https://gitee.com/iprintf/theia-api",
      description="基于FastAPI封装通用后台API组件库",
      long_description=long_description,
      long_description_content_type="text/markdown",
      license="Apache",
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: Apache Software License",
          "Operating System :: OS Independent",
      ],
      python_requires=">=3.10",
      entry_points={"console_scripts": ["theia-create = theia.utils.create_project:main"]},
      install_requires=[
        "aioredis==2.0.1",
        "fastapi==0.110.2",
        "loguru==0.7.2",
        "pydantic==2.7.1",
        "pydantic-settings==2.2.1",
        "python-multipart==0.0.9",
        "redis==5.0.3",
        "uvicorn==0.29.0",
        "sqlalchemy[asyncmy]==2.0.30",
        "alembic==1.13.2",
        "python-jose==3.3.0",
      ],
      package_dir={"": "src"},
      packages=find_packages(where="src"),
)
