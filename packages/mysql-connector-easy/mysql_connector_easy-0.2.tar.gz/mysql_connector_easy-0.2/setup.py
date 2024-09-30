from setuptools import setup,find_packages


# ================= #

setup(
    name='mysql-connector-easy',
    version='0.2',
    packages=find_packages(),
    install_requires=["mysql-connector-python"], 
    description="""An interface library to summarize database queries """,
    author='mdev2007',
    author_email='m.programmer20070@gmail.com',
)