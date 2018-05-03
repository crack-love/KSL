#pragma once

#include <sstream>
#include <array>
#include <vector>
#include <string>
using namespace std;

#include "defines.hpp"
#include "ImageFrame.h"
#include "LabelMapper.h"

class ImageCollection
{
private:
	vector<ImageFrame> collection = vector<ImageFrame>();
	string label;
	float** data;

public:
	ImageCollection();

	void setLabel(string src);

	void stackFrame(const ImageFrame &f);

	// array<string, Show_Status_DistanceFrame_Size> lastFrameToString();

	void setStandard(TIMESPAN startTime);  // «•¡ÿ»≠ (FrameSize, Lerp)

										   // for serialize
	string toString();

	int getCollectionSize();

	void clear();

	string getLabel();

private:

};