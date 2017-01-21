clean:
	rm -rf build/
	rm *.pyc

all:
	 pyinstaller --onefile --windowed dialog.py