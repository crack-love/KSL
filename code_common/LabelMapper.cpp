#include "LabelMapper.h"

LabelMapper LabelMapper::instance;

LabelMapper::LabelMapper()
{
	load();
}

string LabelMapper::lswap(int i)
{
	return itosLabel[i];
}

int LabelMapper::lswap(string s)
{
	return stoiLabel[s];
}


string LabelMapper::label(int i)
{
	return instance.itosLabel[i];
}

int LabelMapper::label(string s)
{
	return instance.stoiLabel[s];
}

void LabelMapper::load()
{
	int id;
	string name;
	fstream is;

	is.open(FILENAME, fstream::in);

	cout << "Loading LABEL.txt ... open = " << is.is_open() << endl;
	FAIL_STOP(is.is_open(), "LABEL.txt file open fail");
	
	while (is.good())
	{
		is >> id >> name;
		cout << ">>> " << id << ", " << name << endl;

		addMap(id, name);
	}	
	is.close();
}

void LabelMapper::addMap(int i, string s)
{
	itosLabel[i] = s;
	stoiLabel[s] = i;
}