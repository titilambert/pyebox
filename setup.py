from setuptools import setup

install_requires = list(val.strip() for val in open('requirements.txt'))
tests_require = list(val.strip() for val in open('test_requirements.txt'))

setup(name='pyebox',
      version='1.1.3',
      description='Get your EBox consumption (wwww.ebox.ca)',
      author='Thibault Cohen',
      author_email='titilambert@gmail.com',
      url='http://github.com/titilambert/pyebox',
      package_data={'': ['LICENSE.txt']},
      include_package_data=True,
      packages=['pyebox'],
      entry_points={
          'console_scripts': [
              'pyebox = pyebox.__main__:main'
          ]
      },
      license='Apache 2.0',
      install_requires=install_requires,
      tests_require=tests_require,
      classifiers=[
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
      ],
)
