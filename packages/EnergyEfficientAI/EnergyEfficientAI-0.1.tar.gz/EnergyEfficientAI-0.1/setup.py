from setuptools import setup, find_packages

setup(
    name='EnergyEfficientAI',  # Name of your library
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'numpy', 
        'psutil', 
        'scikit-learn'
    ],
    entry_point = {
        "console_scripts":[
            "EnergyEfficientAI = EnergyEfficientAI:Message",
        ],
    },
    author='Uzair Hassan, Zia Ur Rehman, Saif Ul Islam',
    description='A library to calculate power, energy, and training time of machine learning algorithms',
    # url='https://github.com/yourusername/energy_ml_lib',  # Add your repo if any
)
