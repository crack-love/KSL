#pragma once

#include "Include.h"
#include "SPoint.h"
#include "FrameCollection.h"
#include "LabelMapper.h"

static enum KINECT_MODE
{
	KINECT_MODE_PREDICT,
	KINECT_MODE_LEARNING,
	KINECT_MODE_OUTPUT,

	KINECT_MODE_SIZE,
};

static string to_string(KINECT_MODE mode)
{
	switch (mode)
	{
	case    KINECT_MODE_OUTPUT:
	return "KINECT_MODE_OUTPUT";
	case    KINECT_MODE_LEARNING:
	return "KINECT_MODE_LEARNING";
	case    KINECT_MODE_PREDICT:
	return "KINECT_MODE_PREDICT";
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
    std::vector<BYTE> colorBuffer;
    int colorWidth;
    int colorHeight;
    unsigned int colorBytesPerPixel;
    cv::Mat colorMat;

	// Body Buffer
	std::array<IBody*, BODY_COUNT> bodies = { nullptr };
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
	double spinePx;
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
	int recorded = 0;
	FrameCollection frameCollection;
	CameraSpacePoint lHandPos;
	CameraSpacePoint rHandPos;
	TIMESPAN recordStartTime;
	string label;
	float* data;

	// cnn
	string lastPredict = "";

public:
	// Constructor
	Kinect(KINECT_MODE m);

	// Destructor
	~Kinect();

	// Processing
	void run_one_cycle();

	void setLabel(string l);
	void setMode(KINECT_MODE m);
	void setPredict(int l);

	inline bool isDataReady() { return isDataready; };

	void setDataBuffer(float* d) { this->data = d; }

	float* getData();


private:
    // Initialize
    void initialize();

    void initializeSensor();

	// Initialize HDFace
	void initializeHDFace();

    void initializeColor();

	void initializeComponents();

	void initializeBody();

	void initializeCNN();

    // Finalize
    void finalize();

    // Update Data
    void update();

    inline void updateColor();

	inline void updateBody();

	void updateSPoint();

	void updateStatus();

	void updateFrame();

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

	string status2string(const FaceModelBuilderCaptureStatus capture);

	string status2string(const FaceModelBuilderCollectionStatus collection);

	void save();
};