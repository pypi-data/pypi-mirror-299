import setuptools

with open("README.md", "r",encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="stu-dense-fog",  # 模块名称
    version="1.0.1",  # 当前版本
    author="LYX",  # 作者
    author_email="1787424709@qq.com",  # 作者邮箱
    description="快速架构tcp服务器并于模型交互",  # 模块简介
    long_description=long_description,  # 模块详细介绍
    long_description_content_type="text/markdown",  # 模块详细介绍格式
    packages=setuptools.find_packages(),  # 自动找到项目中导入的模块
    # 模块相关的元数据
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",  # Linux操作系统
        "Operating System :: Microsoft :: Windows",  # Windows操作系统
    ],
    # 依赖模块
    install_requires=[
        # 如果有其他第三方库依赖，可以在这里列出
    ],
    python_requires='>=3',
)