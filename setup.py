from distutils.core import setup

setup(
    name='idt_oauth2',
    version='0.1',
    packages=['idt_oauth2'],
    package_dir={'idt_oauth2': '.'},
    author='Francesco Levorato',
    author_email='francesco@idonethis.com',
    description='A simple django app supporting OAuth2 authentication flows',
)
