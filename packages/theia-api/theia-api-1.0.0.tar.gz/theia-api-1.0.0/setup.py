
import setuptools

with open("README.md", "r", encoding="utf-8") as fp:
    long_description = fp.read()

setuptools.setup(
        name="theia-api",
        version="1.0.0",
        author="kyo",
        url="https://gitee.com/iprintf/theia-api",
        author_email="iprintf@qq.com",
        description="基于FastAPI封装通用后台API框架",
        long_description=long_description,
        long_description_content_type="text/markdown",
        package_dir={"": "src"},
        packages=setuptools.find_packages(where="src"),
        python_requires=">=3.10"
)
