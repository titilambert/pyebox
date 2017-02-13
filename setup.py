from pip.req import parse_requirements
from setuptools import setup
from pip.download import PipSession

session = PipSession()
install_reqs = parse_requirements('requirements.txt', session=session)
test_reqs = parse_requirements('test_requirements.txt', session=session)

setup(name='pyebox',
      version='0.1.0',
      description='Get your EBox consumption (wwww.ebox.ca)',
      author='Thibault Cohen',
      author_email='titilambert@gmail.com',
      url='http://github.org/titilambert/pyebox',
      packages=['pyebox'],
      entry_points={
          'console_scripts': [
              'pyebox = pyebox.__main__:main'
          ]
      },
      install_requires=[str(r.req) for r in install_reqs],
      tests_require=[str(r.req) for r in test_reqs],
)
