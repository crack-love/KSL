#include "ImageCollection.h"


ImageCollection::ImageCollection()
{
	label = "none";
	//data 
}

void ImageCollection::setLabel(string src)
{
	label = src;
}

void ImageCollection::stackFrame(const ImageFrame &f)
{
	// if (collection.size() + 1 >= collection.max_size()) return;

	collection.push_back(f);
}

void ImageCollection::setStandard(TIMESPAN startTime)
{
	if (collection.size() < 2) return;

	vector<ImageFrame> result = vector<ImageFrame>();
	ImageFrame temp;
	TIMESPAN timeLine;
	TIMESPAN endTime = collection[collection.size() - 1].getTime();
	int dt = (int)(endTime - startTime) / (IMAGE_FRAME_STANDARD_SIZE);
	timeLine = startTime + dt;
	double percent = 0;

	int startIdx = 0;
	int endIdx = 0;

	for (int i = 1; i < collection.size(); ++i)
	{
		if (collection[i].getTime() > timeLine)
		{
			endIdx = i;

			// timeLine - startIdx와 endIdx - startIdx의 비율.
			percent = (double)(timeLine - collection[startIdx].getTime()) / (collection[endIdx].getTime() - collection[startIdx].getTime());

			temp = collection[startIdx];
			temp.LerpMe((float)percent, collection[endIdx]);
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

string ImageCollection::toString()
{
	stringstream out;

	out << currentDateTime() << " ";
	out << LABEL(label) << " ";
	out << IMAGE_FRAME_STANDARD_SIZE << " ";
	out << HAND_WIDTH << " ";
	out << HAND_HEIGHT << " ";
	out << IMAGE_CHANNEL << " ";
	out << 1 << " "; // channel

	for (int j = 0; j < IMAGE_FRAME_STANDARD_SIZE; ++j)
	{
		out << collection[j].toString(0) << " ";
	}
	return out.str();
}

int ImageCollection::getCollectionSize()
{
	return (int)collection.size();
}

void ImageCollection::clear()
{
	collection.clear();
}

string ImageCollection::getLabel()
{
	return label;
}