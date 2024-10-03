from setuptools import setup, find_packages

setup(
    name='VPP-Scaler',           
    version='0.1',              
    description='Scaler_image', 
    author='minhle',          
    author_email='xuanminh.xm201@gmail.com',  
    packages=find_packages(),    
    install_requires=[            
        # 'dependency1',
        # 'dependency2',
    ],
    classifiers=[               
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',      
)
 
