from setuptools import setup

setup(
    name='nifcloud_computing_cli',
    version='0.1',
    description='python CLI for NifCloud Computing',
    author='clutter',
    author_email='clutter.mk2@gmail.com',
    package_dir={'': 'src'},
    install_requires=[
        'click',
        'ConfigParser',
        'Requests',
        'BeautifulSoup4',
    ],
    entry_points='''
        [console_scripts]
        anything=anything:anything_request
        describe-availability-zones=zone:describe_availability_zones
        describe-instances=instance:describe_instances
        modify-instance-attribute=instance:modify_instance_attribute
        nifty-describe-separate-instance-rules=separate_rule:nifty_describe_separate_instance_rules
        nifty-create-separate-instance-rule=separate_rule:nifty_create_separate_instance_rule
        nifty-delete-separate-instance-rule=separate_rule:nifty_delete_separate_instance_rule
    '''
)
