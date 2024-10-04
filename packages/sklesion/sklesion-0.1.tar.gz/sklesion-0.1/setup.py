from setuptools import setup, find_packages

setup(
    name="sklesion",
    version="0.1",
    # Automatically find python packages (they need to have a __init__.py file in them)
    packages=find_packages(),
    install_requires=["tensorflow", "pandas"],
    package_data={
        "sklesion": ["model.keras", "model_props", "prob_to_label"],
    },
    include_package_data=True,
    description="A Keras model for diagnosing skin lesions.",
    author="Elio Pereira",
    author_email="eliocpereira@htomail.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # Minimu Python version
    python_requires=">=3.11",
)
