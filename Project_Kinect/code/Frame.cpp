#include "Frame.h"

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
		distanceL[i] = distance3d(lHandPos, sarr[i].getPoint());
		distanceR[i] = distance3d(rHandPos, sarr[i].getPoint());
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

TIMESPAN Frame::getTime()
{
	return this->lastFrameRelativeTime;
}

void Frame::LerpMe(float p, const Frame & right)
{
	for (int i = 0; i < SPOINT_SIZE; ++i)
	{
		distanceL[i] = Lerp(p, (float)distanceL[i], (float)right.distanceL[i]);
		distanceR[i] = Lerp(p, (float)distanceR[i], (float)right.distanceR[i]);
		lHandActivated = LerpBool(p, lHandActivated, right.lHandActivated);
		rHandActivated = LerpBool(p, rHandActivated, right.rHandActivated);
	}
}
