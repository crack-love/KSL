#pragma once

#include <sstream>
#include <array>
#include <vector>
#include <string>
using namespace std;

#include "common/defines.hpp"
#include "common/LabelMapper.h"
#include "Frame.h"

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

	void setStandard(TIMESPAN startTime);

	// for serialize
	string toString();

	int getCollectionSize();

	void clear();

	string getLabel();

private:

};