#include "ImageFrame.h"

ImageFrame::ImageFrame()
{
}

void ImageFrame::memorize(cv::Mat image, TIMESPAN endtime)
{
	// this->image = image;
	image.copyTo(this->image);
	this->lastFrameRelativeTime = endtime;
}

void ImageFrame::save(string filename)
{
	cv::imwrite(filename, image);
}


TIMESPAN ImageFrame::getTime()
{
	return this->lastFrameRelativeTime;
}

void ImageFrame::LerpMe(float p, const ImageFrame & right)
{
	//cv::addWeighted(image, 1.0 - p, right.image, p, 0.0, image);
}
