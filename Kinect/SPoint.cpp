#include "SPoint.h"

SPoint::SPoint()
{
}

SPoint::SPoint(SPointsType t)
{
	point = CameraSpacePoint();
	type = t;
}


SPoint::~SPoint()
{
}

string SPoint::getName()
{
	return SPointsName[type];
}

SPointsType SPoint::getType()
{
	return type;
}

CameraSpacePoint SPoint::getPoint()
{
	return point;
}

// lerp
void SPoint::setPoint(CameraSpacePoint p)
{
	point.X = Lerp(LERP_PERCENT, point.X, p.X);
	point.Y = Lerp(LERP_PERCENT, point.Y, p.Y);
	point.Z = Lerp(LERP_PERCENT, point.Z, p.Z);
}

float SPoint::Lerp(float p, float x, float y)
{
	if (x > y)
	{
		float temp = x;
		x = y;
		y = temp;
	}

	return  x + (y - x) * p;
}
