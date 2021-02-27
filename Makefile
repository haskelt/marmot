clean:
	rm -f *~
	rm -f bin/*~
	rm -f salal/*~ salal/core/*~ salal/extensions/*~ salal/extensions/*/*~ salal/extensions/*/*/*~
	rm -fr salal/__pycache__ salal/core/__pycache__/ salal/extensions/__pycache__ salal/extensions/*/__pycache__ salal/extensions/*/*/__pycache__
