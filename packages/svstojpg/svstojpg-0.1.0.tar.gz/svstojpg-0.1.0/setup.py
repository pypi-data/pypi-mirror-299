from setuptools import setup,find_packages

setup(
    name='svstojpg',
    version='0.1.0',
    author='liu-ru-yan',
    author_email='jiaohongbao04@gmail.com',
    description='Here is an early file processing tool that uses deep learning methods to analyze pathological sections. Its specific function is to divide a larger SVS file (about several GB) into smaller JPG files, providing the material needed for deep learning. The project is still under development.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/liu-ru-yan/A-tool-for-converting-large-SVS-files-into-segmented-small-JPG-PNG-files-using-OpenSlide.',
    classifiers=[
        'Programming Language :: Python :: 3.10',
    ],
    install_requires=[
            'openslide',
            'tqdm',
            'argparse',
            'PIL',
    ],
    packages=find_packages(),

    entry_points={
            'console_scripts':[
            'stj=svstojpg.process_files:process_file',],
    },

    keywords=['svs','jpg'],
    python_requires='>=3.10',
    license='MIT',

)
