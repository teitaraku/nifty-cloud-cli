from setuptools import setup

setup(
    name='NiftyCloudCli',
    version='0.1',
    description='python CLI for NiftyCloud',
    author='clutter',
    author_email='clutter.mk2@gmail.com',
    package_dir={'': 'src'},
    install_requires=[
        'Click', 'ConfigParser', 'Requests', 'BeautifulSoup4'
    ],
    entry_points='''
        [console_scripts]
        describe-availability-zones=zone:describe_availability_zones
        describe-instances=instance:describe_instances
    '''
)
