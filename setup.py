from setuptools import setup

setup(
    name='sonic-platform-common',
    version='1.0',
    description='Platform-specific peripheral hardware interface APIs for SONiC',
    license='Apache 2.0',
    author='SONiC Team',
    author_email='linuxnetdev@microsoft.com',
    url='https://github.com/Azure/sonic-platform-common',
    maintainer='Joe LeVeque',
    maintainer_email='jolevequ@microsoft.com',
    packages=[
        'sonic_eeprom',
        'sonic_led',
        'sonic_fan',
        'sonic_platform_base',
        'sonic_platform_base.sonic_eeprom',
        'sonic_platform_base.sonic_sfp',
        'sonic_platform_base.sonic_ssd',
        'sonic_platform_base.sonic_pcie',
        'sonic_platform_base.sonic_thermal_control',
        'sonic_psu',
        'sonic_sfp',
        'sonic_thermal',
        'sonic_y_cable',
        'sonic_sensor',
    ],
    # NOTE: Install also depends on sonic-config-engine for portconfig.py
    # This dependency should be eliminated by moving portconfig.py
    # functionality into sonic-py-common
    install_requires=[
        'natsort==6.2.1', # 6.2.1 is the last version which supports Python 2
        'PyYAML',
        'redis',
        'sonic-config-engine',
        'sonic-py-common'
    ],
    setup_requires = [
        'pytest-runner',
        'wheel'
    ],
    tests_require = [
        'pytest',
        'pytest-cov',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.7',
        'Topic :: Utilities',
    ],
    keywords='sonic SONiC platform hardware interface api API'
)
