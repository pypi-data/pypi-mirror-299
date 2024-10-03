from setuptools import setup, find_packages

setup(
    name='BlessedCrack',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'passlib',  # أي مكتبات أخرى تحتاجها
    ],
    entry_points={
        'console_scripts': [
            'blessed_crack = BlessedCrack.Blessed_Crack:main',  # مسار الدالة الرئيسية
        ],
    },
    description='A tool for cracking and encrypting hashes like MD5 and SHA-256.',
    author='JustMuhimin',  # استبدل باسمك
    author_email='',  # استبدل ببريدك الإلكتروني
)
