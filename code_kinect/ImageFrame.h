#pragma once

#include <Kinect.h>
#include <sstream>
#include <array>
#include <string>
#include <vector>
#include <opencv2/opencv.hpp>

using namespace std;

#include "defines.hpp"

// � ����(��) ���� distance ����� �������� defines.hpp�� ���ǵ��ִ�
// todo : JointType -> Spoint

class ImageFrame
{
private:
	cv::Mat image;
	TIMESPAN lastFrameRelativeTime;

public:
	ImageFrame();

	void memorize(cv::Mat image, TIMESPAN endtime);

	// ForFile
	string toString(int noting);

	TIMESPAN getTime();

	void LerpMe(float p, const ImageFrame &right);

private:


};