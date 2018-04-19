#pragma once

#include <iostream>
#include <fstream>
#include <map>
#include <string>
using namespace std;

#include "defines.hpp"

#define LABEL LabelMapper::label

// �̱��� ����
// LABEL(arg) �� string, integer�� ��ȣ ��ȯ
class LabelMapper
{
private :
	const string FILENAME = "../data/LABEL.txt";

	static LabelMapper instance;

	map<int, string> itosLabel;
	map<string, int> stoiLabel;

public:
	static string label(int i);
	static int label(string s);

private:
	LabelMapper(); // load ȣ��

	void load();
	void addMap(int i, string s);
	string lswap(int i);
	int lswap(string s);
};