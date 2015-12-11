from setuptools import setup, find_packages
import sonosalarm

requirements = ['soco==0.11.1', 'texttable==0.8.4', 'PyYAML==3.11']

setup(name='sonosalarm',
      version=sonosalarm.__version__,
      author='Sam Rudge',
      author_email='sam@codesam.co.uk',
      description='Sane alarm player for Sonos',
      packages=find_packages(),
      install_requires=requirements,
      include_package_data=True,
      zip_safe=False,
      url="https://www.codedog.co.uk/sonosalarm",
      licence="MIT",
      entry_points="""
[console_scripts]
sonosalarm = sonosalarm.cli:run
""",
      classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Topic :: Home Automation",
        "Topic :: Multimedia :: Sound/Audio",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5"
      ]
      )
