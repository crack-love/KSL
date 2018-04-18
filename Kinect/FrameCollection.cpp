#include "Frame.h"
#include "FrameCollection.h"
#include "myutil.h"
#include "LabelMapper.h"

FrameCollection::FrameCollection()
{
	label = "none";
	//data 
}

void FrameCollection::setLabel(string src)
{
	label = src;
}

void FrameCollection::stackFrame(const Frame &f)
{
	if (collection.size() + 1 >= collection.max_size()) return;

	collection.push_back(f);
}

array<string, Show_Status_DistanceFrame_Size> FrameCollection::lastFrameToString()
{
	if (collection.size() < 1) return array<string, Show_Status_DistanceFrame_Size>();
	
	return collection[collection.size() - 1].toString();
}

void FrameCollection::getData(float* dst)
{
	for (int i = 0; i < FRAME_STANDARD_SIZE; ++i)
	{
		// Frame[i]
		collection[i].getData(&dst[i * (SPOINT_SIZE + 1) * 2]);
	}

}

void FrameCollection::setStandard(TIMESPAN startTime)
{
	if (collection.size() < 2) return;

	vector<Frame> result = vector<Frame>();
	Frame temp;
	TIMESPAN timeLine;
	TIMESPAN endTime = collection[collection.size() - 1].getTime();
	int dt = (endTime - startTime) / (FRAME_STANDARD_SIZE);
	timeLine = startTime + dt;
	double percent = 0;

	int startIdx = 0;
	int endIdx = 0;

	for (int i = 1; i < collection.size(); ++i)
	{
		if (collection[i].getTime() > timeLine)
		{
			endIdx = i;

			percent = (double)(timeLine - collection[startIdx].getTime()) / (collection[endIdx].getTime() - collection[startIdx].getTime());

			temp = collection[startIdx];
			temp.LerpMe(percent, collection[endIdx]);
			result.push_back(temp);

			timeLine += dt;
			if (timeLine > collection[endIdx].getTime())
				startIdx = endIdx;
			else
			{
				i--;
				continue;
			}
		}
	}

	collection = result;
}

string FrameCollection::toString()
{
	stringstream out;

	out << currentDateTime() << " ";
	out << LABEL(label) << " ";
	out << FRAME_STANDARD_SIZE << " ";
	out << FRAME_STANDARD_SIZE << " ";
	out << 1 << " "; // channel

	for (int j = 0; j < FRAME_STANDARD_SIZE; ++j)
	{
		out << collection[j].toString(0) << " ";
	}		
	return out.str();
}

int FrameCollection::getCollectionSize()
{
	return collection.size();
}

void FrameCollection::clear()
{
	collection.clear();
}

string FrameCollection::getLabel()
{
	return label;
}