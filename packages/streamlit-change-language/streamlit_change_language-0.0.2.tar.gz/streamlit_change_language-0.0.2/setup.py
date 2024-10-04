import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

package_data = {
    '': ['config.ini'],
}

setuptools.setup(
    name="streamlit_change_language",
    version="0.0.2",
    author="py_yzy",
    url='',
    package_data=package_data,
    install_requires=['streamlit>=1.38.0','configparser'],
    author_email="3215574613@qq.com",
    description="支持streamlit内置组件中的文本中英文切换",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.9",
)