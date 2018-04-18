#pragma once

#include <map>
#include <string>
using namespace std;

#define LABEL LabelMapper::label

// see source file to know&mod mapping
class LabelMapper
{
private :
	static LabelMapper instance;

	map<int, string> itosLabel;
	map<string, int> stoiLabel;

public:
	static string label(int i);
	static int label(string s);

private:
	LabelMapper();

	void addMap(int i, string s);
	string lswap(int i);
	int lswap(string s);
};