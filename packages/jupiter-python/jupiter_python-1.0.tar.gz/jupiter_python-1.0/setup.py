import setuptools

setuptools.setup(
	name='jupiter-python',
	version='1.0',
	author='__token__',
	author_email='volodymyrsup@yandex.ru',
	description='Fastest way to handle jup.ag swap API',
	packages=['jupiter-python'],
	include_package_data=True,
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.6',
)