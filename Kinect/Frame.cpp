#include "Frame.h"
#include "myutil.h"

Frame::Frame()
{
}

void Frame::memorize(CameraSpacePoint lHandPos, CameraSpacePoint rHandPos, array<SPoint, SPOINT_SIZE> sarr, bool la, bool ra, TIMESPAN endtime)
{
	this->lHandActivated = la;
	this->rHandActivated = ra;
	this->lastFrameRelativeTime = endtime;

	for (int i = 0; i < SPOINT_SIZE; ++i)
	{
		distanceL[i] = myDistance3d(lHandPos, sarr[i].getPoint());
		distanceR[i] = myDistance3d(rHandPos, sarr[i].getPoint());
	}
}

array<string, Show_Status_DistanceFrame_Size> Frame::toString()
{
	stringstream sstream;
	array<string, Show_Status_DistanceFrame_Size> res = array<string, Show_Status_DistanceFrame_Size>();

	res[0] = sstream.str(); sstream.str("");

	sstream << "-distance : ";
	for (int i = 0; i < SPOINT_SIZE; ++i)
	{
		sstream.precision(2);

		sstream << distanceL[i] << " " << distanceR[i] << ", ";
	}
	res[3] = sstream.str(); sstream.str("");

	sstream << "-LHA, RHA : " << (lHandActivated ? "T" : "F") << " " << (rHandActivated ? "T" : "F");
	res[2] = sstream.str(); sstream.str("");

	sstream << "-EndTime : " << lastFrameRelativeTime;
	res[1] = sstream.str(); sstream.str("");

	return res;
}

string Frame::toString(int nothing)
{
	stringstream sstream;

	sstream << lHandActivated << " ";
	sstream << rHandActivated << " ";

	for (int i = 0; i < SPOINT_SIZE; ++i)
	{
		sstream << distanceL[i] << " " << distanceR[i] << " ";
	}

	return sstream.str();
}

bool Frame::getHAL()
{
	return lHandActivated;
}

bool Frame::getHAR()
{
	return rHandActivated;
}

double Frame::getDistanceL(int i)
{
	return distanceL[i];
}

double Frame::getDistanceR(int i)
{
	return distanceR[i];
}

void Frame::getData(float * dst)
{
	dst[0] = (float)lHandActivated;
	dst[1] = (float)rHandActivated;
	
	dst = &dst[2];

	for (int i = 0; i < SPOINT_SIZE * 2; i+=2)
	{
		dst[i] = distanceL[i / 2];
		dst[i + 1] = distanceR[i / 2];
	}
}

TIMESPAN Frame::getTime()
{
	return this->lastFrameRelativeTime;
}

void Frame::LerpMe(float p, const Frame & right)
{
	for (int i = 0; i < SPOINT_SIZE; ++i)
	{
		distanceL[i] = Lerp(p, distanceL[i], right.distanceL[i]);
		distanceR[i] = Lerp(p, distanceR[i], right.distanceR[i]);
		lHandActivated = LerpBool(p, lHandActivated, right.lHandActivated);
		rHandActivated = LerpBool(p, rHandActivated, right.rHandActivated);
	}
}
