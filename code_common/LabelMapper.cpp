#include "LabelMapper.h"

LabelMapper LabelMapper::instance;

LabelMapper::LabelMapper()
{
	addMap(0, "�ȳ��ϼ���");
	addMap(1, "�ٴ�");
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