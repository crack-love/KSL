#pragma once
#pragma comment(lib,"ws2_32.lib")

// for networking
#include <winsock2.h>

#include <Kinect.h>
#include <Kinect.face.h>
#include <ppl.h> // parallel_for_each
#include <opencv2/opencv.hpp>
#include <vector>
#include <string>
#include <wrl/client.h>
#include <thread> // this_thread
#include <Process.h> // for loading python



// #include <windows.h>

using namespace std;
using namespace Microsoft::WRL;
using namespace cv;

#include "defines.hpp"
#include "SPoint.h"
#include "FrameCollection.h"
#include "LabelMapper.h"

	enum KINECT_MODE
	{
		KINECT_MODE_OUTPUT,
		KINECT_MODE_PREDICT,
		KINECT_MODE_LEARNING,

		KINECT_MODE_SIZE,
	};

	static string to_string(KINECT_MODE mode)
	{
		switch (mode)
		{
		case	    KINECT_MODE_OUTPUT:
			return "KINECT_MODE_OUTPUT";
		case		KINECT_MODE_LEARNING:
			return "KINECT_MODE_LEARNING";
		case		KINECT_MODE_PREDICT:
			return "KINECT_MODE_PREDICT";
		default:
			return "ERR_NOT_MODE_NUMBER";

		}
	}

	class Kinect
	{
	private:
		KINECT_MODE mode;

		// Sensor
		ComPtr<IKinectSensor> kinect;

		// Coordinate Mapper
		ComPtr<ICoordinateMapper> coordinateMapper;

		// Reader
		ComPtr<IColorFrameReader> colorFrameReader;
		ComPtr<IBodyFrameReader> bodyFrameReader;
		ComPtr<IHighDefinitionFaceFrameReader> hdFaceFrameReader;

		// Color Buffer
		std::vector<BYTE> colorBuffer; // raw buffer
		int colorWidth, colorHeight;
		cv::Mat colorMat; // showing mat
		cv::Mat lhandMat; // left hand mat
		cv::Mat rhandMat; // right hand mat

		// Body Buffer
		array<IBody*, BODY_COUNT> bodies = { nullptr };
		std::array<cv::Vec3b, BODY_COUNT> colors;

		// HDFace Buffer
		vector<CameraSpacePoint> vertexes;
		ComPtr<IFaceModelBuilder> faceModelBuilder;
		ComPtr<IFaceAlignment> faceAlignment;
		ComPtr<IFaceModel> faceModel;
		std::array<float, FaceShapeDeformations::FaceShapeDeformations_Count> faceShapeUnits = { 0.0f };
		UINT32 vertexCount;
		UINT64 trackingId;
		int trackingCount = 0;
		bool produced = false;
		BOOLEAN tracked = false;

		/// sPoint
		float spinePx;
		std::array<SPoint, SPOINT_SIZE> sPoints;
		CameraSpacePoint addtionalPoints[11];

		/// Status Text
		double fps = 0;
		TIMESPAN lastFrameRelativeTime;
		TIMESPAN pastFrameRelativeTime;
		std::stringstream statusStream;
		cv::Scalar statusFontColor;
		FaceModelBuilderCaptureStatus faceCapture;
		FaceModelBuilderCollectionStatus faceCollection;
		double distance = 0;

		// ML data
		bool leftHandActivated = false;
		bool rightHandActivated = false;
		bool frameStacking = false;
		bool isDataready = false;
		bool completePrediction = true;

		int recorded = 0;
		FrameCollection frameCollection;
		CameraSpacePoint lHandPos;
		CameraSpacePoint rHandPos;
		TIMESPAN recordStartTime;
		int label;
		float* data;

		// cnn
		string lastPredict = "";

		// handTrack
		// ICoordinateMapper* pMapper;

	public:
		// Constructor
		Kinect(KINECT_MODE m);

		// Destructor
		~Kinect();

		// Processing
		void run_one_cycle();

		void setLabel(int l);
		void setMode(KINECT_MODE m);
		void setPredict(int l);

		inline bool isDataReady() { return isDataready; };
		inline bool isComplete() { return completePrediction; }

		void setDataBuffer(float* d) { this->data = d; }

		float* getData();

	private:
		// Initialize
		void initialize();

		void initializeSensor();

		// Initialize HDFace, FaceReader 초기화
		void initializeHDFace();

		// Color(RGB) Frame Reader 초기화
		void initializeColor();

		void initializeComponents();

		// Body Frame Reader 초기화
		void initializeBody();

		void initializeCNN();

		// Finalize
		void finalize();

		// Update Data
		void update();

		inline void updateColor();

		inline void updateBody();  // 손 활성화 여부 및 body frame -> data

		void updateSPoint();  // 관절 위치 업데이트

		void updateStatus();  // frame 속도 계산

		void updateFrame();  // frame stacking 여부 설정 및 staking, 데이터 저장

		void updateHDFace();

		void updatePredict();

		// Draw Data
		void draw();

		inline void drawColor();

		inline void drawBody();

		void drawHDFace();

		void drawSPoint();

		void drawEllipse(cv::Mat & image, const CameraSpacePoint & pos, const int radius, const cv::Vec3b & color, const int thickness = -1);

		void drawVertexes(cv::Mat& image, const std::vector<CameraSpacePoint> vertexes, const int radius, const cv::Vec3b& color, const int thickness = -1);

		void drawStatusText();

		// Show Data
		void show();

		inline void showColor();

		// etc
		void findClosestBody(const std::array<IBody*, BODY_COUNT>& bodies);

		void findLRHandPos();
		bool findLRHandPosResult();

		string status2string(const FaceModelBuilderCaptureStatus capture);

		string status2string(const FaceModelBuilderCollectionStatus collection);

		void save();
		void saveForPredict();
		void queryToServer();

		// for extract hand
		void extractHand(cv::Mat& screnn);
		// void extractLHand(cv::Mat& screnn);
		// void extractRHand(cv::Mat& screnn);
		// inline bool inRange(int x, int start, int end);
	};