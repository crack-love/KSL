#include "LabelMapper.h"

LabelMapper LabelMapper::instance;

LabelMapper::LabelMapper()
{
	addMap(0, "안녕하세요");
	addMap(1, "바다");
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

void LabelMapper::addMap(int i, string s)
{
	itosLabel[i] = s;
	stoiLabel[s] = i;
}