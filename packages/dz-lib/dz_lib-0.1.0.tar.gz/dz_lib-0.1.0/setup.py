from setuptools import setup

setup(
    name='dz_lib',
    version='0.1.0',
    description='A library for visualizing, comparing, and interpreting detrital zircon data',
    url='https://github.com/nielrya4/dz_lib',
    author='Ryan Nielsen',
    author_email='nielrya4@isu.edu',
    license='BSD 2-clause',
    packages=['dz_lib'],
    install_requires=['joblib==1.4.2',
                      'numpy==2.1.1',
                      'scikit-learn==1.5.2',
                      'scipy==1.14.1',
                      'threadpoolctl==3.5.0'
                      ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)