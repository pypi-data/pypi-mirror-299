from setuptools import setup, find_packages

setup(
    name="ThisIsACoolThing",
    version="1.0.2",
    author="Lucy",
    author_email="connectchario@gmail.com",
    description="Ethereum Price Prediction Package for Short-Term Trading",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/LUCY-1986-2009-project-ethereum-market-prediction-unit-limit_uncertainty,control_yourself--OurFriendLucy",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "tensorflow>=2.0",
        "pandas",
        "ccxt",
        "pandas-ta",
        "numpy",
        "joblib",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',

    # Add entry_points to make command-line tools
    entry_points={
        'console_scripts': [
            'twelve=LUCY.app:main',  # Runs app.py
            'one=LUCY.ppa:main',     # Runs ppa.py
        ],
    },

    # Include model and scaler files
    package_data={
        'LUCY': [
            'eth_lstm_model_1h_optimized.h5',
            'scaler-1h.pkl',
            'eth_lstm_best_model_1hour.h5',
            'scaler_custom.pkl'
        ],
    },
)
