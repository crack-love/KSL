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

void ImageFrame::save(string filepath)
{
	cv::Mat gray;
	cv::cvtColor(image, gray, CV_RGB2GRAY);
	cv::imwrite(filepath, gray);
}


TIMESPAN ImageFrame::getTime()
{
	return this->lastFrameRelativeTime;
}

void ImageFrame::LerpMe(float p, const ImageFrame & right)
{
	//cv::addWeighted(image, 1.0 - p, right.image, p, 0.0, image);
}

void ImageFrame::toString(stringstream &stream, char delimeter)
{
	cv::Size size = image.size();
	int total = size.width * size.height * image.channels();
	
	std::vector<uchar> data(image.ptr(), image.ptr() + total);
	std::string s(data.begin(), data.end());
	stream << data.size() << delimeter; // 1번째 아이템 dataLength
	stream << s << delimeter; // 2번째 아이템 data
}