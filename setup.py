from os.path import dirname, join
from setuptools import setup


readme_path = join(dirname(__file__), 'README.md')

with open(readme_path, encoding='utf-8') as readme_file:
    readme = readme_file.read()


setup(
    name='aiovkcom',
    version='0.0.5',
    author='Konstantin Togoi',
    author_email = 'konstantin.togoi@gmail.com',
    url='https://github.com/KonstantinTogoi/aiovkcom',
    description='vk.com Python REST API wrapper',
    long_description=readme,
    long_description_content_type='text/markdown',
    license='BSD',
    packages=['aiovkcom'],
    install_requires='aiohttp>=3.0.0',
    keywords=['vk.com api asyncio'],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
