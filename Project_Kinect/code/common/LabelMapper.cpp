#include "LabelMapper.h"

// ½ºÅÂÆ½ »ý¼º
LabelMapper LabelMapper::instance;

LabelMapper::LabelMapper()
{

}

void LabelMapper::initialize()
{
	//itosLabel.erase(itosLabel.begin(), itosLabel.end());
	//stoiLabel.erase(stoiLabel.begin(), stoiLabel.end());
	
	load();
}

void LabelMapper::load()
{
	fstream is;
	int id;
	string name;

	is.open(FILE_PATH, fstream::in);

	cout << "Loading " + FILE_PATH + " ... " << (is.is_open() ? "OK" : "FAIL") << endl;
	FAIL_STOP(is.is_open(), FILE_PATH + " open fail");

	while (is.good())
	{
		is >> id >> name;
		//cout << id << ", " << name << endl;

		addMap(id, name);
	}
	is.close();
}

void LabelMapper::printLabel()
{
	int size = itosLabel.size();
	for (int i = 0; i < size; ++i)
	{
		cout << i << ", " << lswap(i) << endl;
	}
}

string LabelMapper::lswap(int i)
{
	return itosLabel[i];
}

int LabelMapper::lswap(string s)
{
	return stoiLabel[s];
}


LabelMapper* LabelMapper::getInstance()
{
	return &instance;
}

string LabelMapper::label(int i)
{
	return itosLabel[i];
}

int LabelMapper::label(string s)
{
	return stoiLabel[s];
}

void LabelMapper::addMap(int i, string s)
{
	itosLabel[i] = s;
	stoiLabel[s] = i;
}