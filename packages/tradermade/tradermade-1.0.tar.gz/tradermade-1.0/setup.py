from setuptools import setup

setup(
    name='tradermade',
    version='1.0',    
    description='A package that helps you get Forex data from TraderMade data API',
    url='https://github.com/tradermade',
    author='TraderMade',
    author_email='support@tradermade.com',
    license='MIT',
    long_description=open('README.rst', 'r').read(),
    packages=['tradermade'],
    install_requires=['numpy',
                      'pandas',
                      'requests',  
                      'websockets',                 
                      ],

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
    ],
)
