from setuptools import find_packages, setup

with open("requirements.txt", "r", encoding="utf-8") as req_file:
    install_requires = req_file.read().splitlines()

with open("README.md", "r", encoding="utf-8") as readme_file:
    readme = readme_file.read()

version = "1.0.3.17"

setup(
    name="src_demand_forecast",
    packages=find_packages(where="src_demand_forecast"),
    package_dir={"": "src_demand_forecast"},
    version=version,
    description="This is lib-predicts for demand forecast based on machine learning",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Eduard Poliakov",
    author_email="ya.polykov@gmail.com",
    license="MIT",
    install_requires=install_requires,
    package_data={
        'src_demand_forecast': ['demand_forecast_source/*'],
    },
    include_package_data=True,
    url="https://github.com/Edipool/DemandForecast",
    classifiers=[
        'Programming Language :: Python :: 3.8',
    ],
)
