#ifndef INCLUDE_H
#define INCLUDE_H

#include <iostream>
#include <Windows.h>
#include <Kinect.h>
#include <Kinect.Face.h>
#include <opencv2/opencv.hpp>
#include <sstream>
#include <string>
#include <vector>
#include <wrl/client.h>
#include <stdexcept>
#include <thread>
#include <chrono>
#include <ppl.h>
#include <cmath>
#include <fstream>
#include <time.h>

using namespace Microsoft::WRL;
using namespace std;

#define M_PI 3.14159265358979323846

#define Show_Status_Basic
#define Show_Status_FPS
#define Show_Status_Mode
//#define Show_Status_PointPos
#define Show_Status_Face
#define Show_Status_MLVar
#define Show_Status_DistanceFrame
#define Show_Status_DistanceFrame_Size 4 // do not Change this

#define LERP_PERCENT 0.6
#define HAND_RECORD_TYPE_L JointType_HandLeft
#define HAND_RECORD_TYPE_R JointType_HandRight
#define FRAME_STANDARD_SIZE ((SPOINT_SIZE+1)*2)

#endif