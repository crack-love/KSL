#include "ImageFrameCollection.h"


ImageFrameCollection::ImageFrameCollection()
{
	label = "none";
	//data 
}

void ImageFrameCollection::setLabel(string src)
{
	label = src;
}

void ImageFrameCollection::stackFrame(const ImageFrame& f)
{
	collection.push_back(f);
}

void ImageFrameCollection::setStandard(TIMESPAN startTime)
{
	if (collection.size() < 2) return;

	vector<ImageFrame> result = vector<ImageFrame>();
	ImageFrame temp;
	TIMESPAN timeLine;
	TIMESPAN endTime = collection[collection.size() - 1].getTime();

	int dt = (int)(endTime - startTime) / (IMAEG_STANDARD_FRAME_SIZE);
	timeLine = startTime + dt;

	double percent = 0;

	int startIdx = 0;
	int endIdx = 0;

	int cnt = 0;
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
			cnt++;

			timeLine += dt;
			if (timeLine > collection[endIdx].getTime()) // endidx가 timeLime 시간보다 적을 경우 다음 idx로 넘어감
				startIdx = endIdx;
			else
			{
				i--;
				continue;
			}
		}
	}

	cout << cnt << endl;
	collection = result;
}


// 76_L.bmp
void ImageFrameCollection::save(string dirpath, string suffix)
{
	string fileName;

	for (int j = 0; j < IMAEG_STANDARD_FRAME_SIZE; ++j)
	{
		fileName = to_string(j) + "_" + suffix;

		collection[j].save(dirpath + fileName + ".bmp");
	}
}

int ImageFrameCollection::getCollectionSize()
{
	return (int)collection.size();
}

void ImageFrameCollection::clear()
{
	collection.clear();
}

string ImageFrameCollection::getLabel()
{
	return label;
}