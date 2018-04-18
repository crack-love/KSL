#pragma once

#include "include.h"
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

	void getData(float*);

	void setStandard(TIMESPAN startTime);

	// for serialize
	string toString();

	int getCollectionSize();

	void clear();

	string getLabel();

private:

};