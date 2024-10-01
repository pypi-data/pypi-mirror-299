# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['synthetic_data_samples_generator',
 'synthetic_data_samples_generator.configs',
 'synthetic_data_samples_generator.generator',
 'synthetic_data_samples_generator.sampling',
 'synthetic_data_samples_generator.utils']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'synthetic-data-samples-generator',
    'version': '0.0.1',
    'description': 'Generates synthetic data samples on the fly for test cases.',
    'long_description': '\n<!-- <p align=\'center\'>\n    <img src=\'./.docs/cctv.png\' width=\'20%\' height=\'20%\'>\n</p> -->\n\n<h1 align=\'center\'>\n    <strong> Synthetic Data Generator </strong>\n</h1>\n\n<p align=\'center\'>\n    Designed to generate synthetic data on the fly so you can stress test your pipelines with ease.\n</p>\n\n<div align="center">\n\n  <a href="code coverage">![coverage](https://img.shields.io/badge/coverage-99%25-brightgreen)</a>\n  <a href="tests">![tests](https://img.shields.io/badge/tests-34%20passed%2C%200%20failed-brightgreen)</a>\n  <a href="python version">![sbt_version](https://img.shields.io/badge/python-3.11.4-blue?logo=python&logoColor=white)</a>\n\n</div>\n\n### **1. Intro**\n\nThe Synthetic Data Generator is a powerful tool designed to help developers and data engineers stress test their data pipelines with ease. By generating realistic, customizable synthetic data on the fly, this project enables thorough testing of data processing systems under various conditions and loads.\n\nKey features of the Synthetic Data Generator include:\n\n- **On-demand data generation**: Create large volumes of synthetic data as needed;\n- **Scalability**: Suitable for testing small to large-scale data pipelines;\n- **Integration-friendly**: Designed to work seamlessly with various data processing frameworks.\n\nWhether you\'re developing a new data pipeline, optimizing an existing one, or conducting performance testing, the Synthetic Data Generator provides the flexible, controllable data source you need to ensure your systems are robust and reliable under real-world conditions.\n\n### **2. How to Use - _high level_**\n\n- if you want to generate samples to all the file type handled by the project:\n````python\ngenerator = SyntheticDataGenerator(\n    target_size_mb=10,\n    num_columns=10,\n    sample_rows_num=1000,\n)\n\ngenerator.generate_all_file_types("test_data", "test_folder")\n````\n\n- if you want to generate samples to a specific file type:\n\n````python\ngenerator = SyntheticDataGenerator(target_size_mb=100)\n\ngenerator.generate_file(\n    values_type=ValuesType.STRING,\n    file_name="test_data_100mb",\n    file_type=FileType.CSV,\n    landing_path="test_folder"\n)\n````\n\n### **A1. Future Work**\n\nThere are still some points that we should tackle:\n\n- It\'s hard to scale the size of the generated data for the ttl files up to the target size, since it\'s not proportional to the records number - *something that needs to be explored*;\n',
    'author': 'Joao Nisa',
    'author_email': 'joao.je.nisa@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
