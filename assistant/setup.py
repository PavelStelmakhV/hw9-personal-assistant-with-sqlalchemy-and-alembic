from setuptools import setup, find_namespace_packages

setup(name='assistant',
      version='0.1.0',
      description='assistant for me',
      url='https://github.com/PavelStelmakhV/personal-assistant-with-cli',
      author='Stelmakh Pavel, Klymenko Denys, ',
      author_email='stelmahpv13@ukr.net, ranok.denis@gmail.com',
      license='MIT',
      packages=find_namespace_packages(),
      entry_points={'console_scripts': ['assistant=assistant.main:main']},
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
      ]
)
