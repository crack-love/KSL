#pragma once

#include "kygUtil.hpp" // Macro using functions

// ---------------------------------------------------------------------
//	dnn using defines
// ---------------------------------------------------------------------

//#define PRINT_DETAIL
//#define WRITE_LOG

//#define M_PI 3.14159265358979323846

// ---------------------------------------------------------------------
//	kinect using defines
// ---------------------------------------------------------------------

#define Show_Status_Basic
#define Show_Status_FPS
#define Show_Status_Mode
//#define Show_Status_PointPos
//#define Show_Status_Face
#define Show_Status_MLVar
//#define Show_Status_DistanceFrame
#define Show_Status_DistanceFrame_Size 4 // do not Change/disable this

#define LERP_PERCENT 0.35
#define HAND_RECORD_TYPE_L JointType_HandLeft
#define HAND_RECORD_TYPE_R JointType_HandRight
#define FRAME_STANDARD_SIZE 150

#define PATH_DATA_FOLDER "../../data/"
#define FILE_LABEL "LABEL.txt"

// ROI defines
#define IMAEG_STANDARD_FRAME_SIZE 35 // 왼/오 각 채널당 프레임 개수 (총 *2)
#define IMAGE_WIDTH 80
#define IMAGE_HEIGHT 80

// ---------------------------------------------------------------------
//	Macro
// ---------------------------------------------------------------------

// if fail, system("pause"), throw runtim-err
#define FAIL_STOP(check, msg) fail_than_stop(check, msg)

// InputType은 oerator >> 오버로딩 필요
#define INPUT(Type, name) input_something<Type>(std::cin, std::cout, name)

// EnumType은 to_string 오버로딩 필요
#define SHOW_ENUM(Type, size, paading) show_enumeration<Type>(std::cout, size, paading)

// Error Check Macro (HRESULT)
#define ERROR_CHECK( ret )											    \
    if( FAILED( ret ) ){											    \
        std::stringstream ss;										    \
        ss << "failed " << #ret << " " << std::hex << ret << std::endl;	\
        throw std::runtime_error( ss.str().c_str() );					\
    }