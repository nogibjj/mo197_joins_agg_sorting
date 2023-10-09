install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

format:	
	black *.py 

lint:
	pylint --disable=R,C --ignore-patterns=test_.*?py *.py src/*.py


refactor: format lint
		
all: install lint  format 
