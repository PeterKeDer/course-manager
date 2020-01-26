from setuptools import setup

setup(
    name='course_manager',
    version='0.1',
    packages=['course_manager'],
    install_requires=[
        'Click'
    ],
    entry_points={
        'console_scripts': [
            'cm=course_manager.__main__:main'
        ]
    }
)
