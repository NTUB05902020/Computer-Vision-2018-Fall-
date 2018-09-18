all:
	test ! -f "lena.bmp" && echo "lena.bmp not exist"\
	 || (test -f "lena.bmp" && ((test ! -d "output" && mkdir output || true)\
	 && python3 hw1-1a.py && python3 hw1-1b.py\
	 && python3 hw1-1c.py && python3 hw1-2.py))\
