from setuptools import setup

setup(
    name='my-nellie-plugin',
    version='0.1.0',
    py_modules=['plugin_module'],
    install_requires=[
        'nellie',
        'numpy',
    ],
    entry_points={
        'nellie.plugins': [
            'Custom Plugin Name = plugin_module:my_custom_nellie_plugin',
        ],
    },
)