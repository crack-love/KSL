#pragma once

#include <sstream>
#include <array>
#include <vector>
#include <string>
using namespace std;

#include "defines.hpp"
#include "Frame.h"
#include "LabelMapper.h"

class FrameCollection
{
private:
	vector<Frame> collection = vector<Frame>();
	string label;
	float** data;

public:
	FrameCollection();

	void setLabel(string src);

	void stackFrame(const Frame &f);

	array<string, Show_Status_DistanceFrame_Size> lastFrameToString();

	void getData(float*);

	void setStandard(TIMESPAN startTime);

	// for serialize
	string toString();

	int getCollectionSize();

	void clear();

	string getLabel();

private:

};