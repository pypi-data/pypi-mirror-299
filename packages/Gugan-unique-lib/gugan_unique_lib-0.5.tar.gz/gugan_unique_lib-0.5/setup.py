from setuptools import setup, find_packages

setup(
    name='Gugan_unique_lib',
    version='0.5',
    packages=find_packages(),
    install_requires = [
        # Add dependencies here
    ],
    entry_points = {
        "console_scripts" : [
            "Hello = Gugan_unique_lib:hello",
            "AVLTree = Gugan_unique_lib:display_avl_tree_from_input",
            "Addition = GUgan_unique_lib:addition",
        ],
    },
)
#a61f9712-5363-4a7a-9d2f-d640a36afb19