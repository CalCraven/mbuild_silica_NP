from setuptools import setup


setup(
    # Self-descriptive entries which should always be present
    name='build_silica_NP',
    author='Cal',
    author_email='nicholas.c.craven@vanderbilt.edu',
    license='MIT',
    version='0.0.0',
    description='Create a course grained silica NP using the methodlology found in Summers, A. Z., et al. A Transferable, Multiresolution Coarse-Grained Model for Amorphous Silica Nanoparticles. 2018, p. In preparation.',
    zip_safe=False,
    entry_points={
        'mbuild.plugins':[
        "build_silica_NP = build_silica_NP.build_silica_NP:build_silica_NP"
        ]
        }
    )
