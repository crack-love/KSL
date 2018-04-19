#pragma once

#include <iostream>
#include <fstream>
#include <map>
#include <string>
using namespace std;

#include "defines.hpp"

#define LABEL LabelMapper::label

// 싱글톤 패턴
// LABEL(arg) 로 string, integer간 상호 전환
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
	LabelMapper(); // load 호출

	void load();
	void addMap(int i, string s);
	string lswap(int i);
	int lswap(string s);
};