#include "kinectProgram.h"

float* Kinect::getData()
{
	return data;
}

// Constructor
Kinect::Kinect(KINECT_MODE m)
{
	mode = m;

    // Initialize
    initialize();
}

// Destructor
Kinect::~Kinect()
{
    // Finalize
    finalize();
}

// Processing
void Kinect::run_one_cycle()
{
    // Update Data
    update();

    // Draw Data
    draw();

    // Show Data
    show();
}

void Kinect::setLabel(int l)
{
	label = l;
}

void Kinect::setMode(KINECT_MODE m)
{
	mode = m;
}

void Kinect::setPredict(int label)
{
	isDataready = false;
	this->lastPredict = LABEL(label);
	cout << label << " " << lastPredict << endl;
}

// Initialize
void Kinect::initialize()
{
    cv::setUseOptimized( true );

    // Initialize Sensor
    initializeSensor();

	// Initialize HDFace
	initializeHDFace();

    // Initialize Color
    initializeColor();

	initializeBody();

	initializeCNN();

	initializeComponents();


    // Wait a Few Seconds until begins to Retrieve Data from Sensor ( about 2000-[ms] )
    std::this_thread::sleep_for( std::chrono::seconds( 2 ) );
}

void Kinect::initializeComponents()
{
	statusFontColor = cv::Scalar(0, 0, 0, 0);

	for (int i = 0; i < SPOINT_SIZE; ++i)
	{
		sPoints[i] = SPoint((SPointsType)i); 
	}
}

// Initialize Sensor
void Kinect::initializeSensor()
{
    // Open Sensor
    ERROR_CHECK( GetDefaultKinectSensor( &kinect ) );

    ERROR_CHECK( kinect->Open() );

    // Check Open
    BOOLEAN isOpen = FALSE;
    ERROR_CHECK( kinect->get_IsOpen( &isOpen ) );
    if( !isOpen ){
        throw std::runtime_error( "failed IKinectSensor::get_IsOpen( &isOpen )" );
    }

	// Retrieve Coordinate Mapper
	ERROR_CHECK(kinect->get_CoordinateMapper(&coordinateMapper));
}


// Initialize HDFace
inline void Kinect::initializeHDFace()
{
	// Create HDFace Sources
	ComPtr<IHighDefinitionFaceFrameSource> hdFaceFrameSource;
	ERROR_CHECK(CreateHighDefinitionFaceFrameSource(kinect.Get(), &hdFaceFrameSource));

	// Open HDFace Readers
	ERROR_CHECK(hdFaceFrameSource->OpenReader(&hdFaceFrameReader));

	// Create Face Alignment
	ERROR_CHECK(CreateFaceAlignment(&faceAlignment));

	// Create Face Model and Retrieve Vertex Count
	ERROR_CHECK(CreateFaceModel(1.0f, FaceShapeDeformations::FaceShapeDeformations_Count, &faceShapeUnits[0], &faceModel));
	ERROR_CHECK(GetFaceModelVertexCount(&vertexCount)); // 1347
	vertexes = vector<CameraSpacePoint>(vertexCount);

	// Create and Start Face Model Builder
	FaceModelBuilderAttributes attribures = FaceModelBuilderAttributes::FaceModelBuilderAttributes_None;
	ERROR_CHECK(hdFaceFrameSource->OpenModelBuilder(attribures, &faceModelBuilder));
	ERROR_CHECK(faceModelBuilder->BeginFaceDataCollection());
}

// Initialize Color
void Kinect::initializeColor()
{
	uint colorBytesPerPixel;

    // Open Color Reader
    ComPtr<IColorFrameSource> colorFrameSource;
    ERROR_CHECK( kinect->get_ColorFrameSource( &colorFrameSource ) );
    ERROR_CHECK( colorFrameSource->OpenReader( &colorFrameReader ) );

    // Retrieve Color Description
    ComPtr<IFrameDescription> colorFrameDescription;
    ERROR_CHECK( colorFrameSource->CreateFrameDescription( ColorImageFormat::ColorImageFormat_Bgra, &colorFrameDescription ) );
    ERROR_CHECK( colorFrameDescription->get_Width( &colorWidth ) ); // 1920
    ERROR_CHECK( colorFrameDescription->get_Height( &colorHeight ) ); // 1080
    ERROR_CHECK( colorFrameDescription->get_BytesPerPixel( &colorBytesPerPixel ) ); // 4

    // Allocation Color Buffer
    colorBuffer.resize( colorWidth * colorHeight * colorBytesPerPixel );
}

// Initialize Body
inline void Kinect::initializeBody()
{
	// Open Body Reader
	ComPtr<IBodyFrameSource> bodyFrameSource;
	ERROR_CHECK(kinect->get_BodyFrameSource(&bodyFrameSource));
	ERROR_CHECK(bodyFrameSource->OpenReader(&bodyFrameReader));

	// Initialize Body Buffer
	Concurrency::parallel_for_each(bodies.begin(), bodies.end(), [](IBody*& body) {
		SafeRelease(body);
	});

	// Color Table for Visualization
	colors[0] = cv::Vec3b(255, 0, 0); // Blue
	colors[1] = cv::Vec3b(0, 255, 0); // Green
	colors[2] = cv::Vec3b(0, 0, 255); // Red
	colors[3] = cv::Vec3b(255, 255, 0); // Cyan
	colors[4] = cv::Vec3b(255, 0, 255); // Magenta
	colors[5] = cv::Vec3b(0, 255, 255); // Yellow
}

void Kinect::initializeCNN()
{
	// reading cnn model
	//bool ok = cnn.read("../models/test.model");
	//cout << "Reading cnn model ..." << ok << endl;
}

// Finalize
void Kinect::finalize()
{
    cv::destroyAllWindows();


	// Release Body Buffer
	Concurrency::parallel_for_each(bodies.begin(), bodies.end(), [](IBody*& body) {
		SafeRelease(body);
	});

    // Close Sensor
    if( kinect != nullptr ){
        kinect->Close();
    }
}

// Update Data
void Kinect::update()
{
    // Update Color
    updateColor();

	// Update Body
	updateBody();

	// Update HDFace
	updateHDFace();

	updateSPoint();

	updateFrame();

	updateStatus();
}

void Kinect::updatePredict()
{
}

// Update Color
inline void Kinect::updateColor()
{
    // Retrieve Color Frame
    ComPtr<IColorFrame> colorFrame;
    const HRESULT ret = colorFrameReader->AcquireLatestFrame( &colorFrame );
    if( FAILED( ret ) ){
        return;
    }		
	
	// for fps calculating
	colorFrame->get_RelativeTime(&lastFrameRelativeTime);

    // Convert Format ( YUY2 -> BGRA )
    ERROR_CHECK( colorFrame->CopyConvertedFrameDataToArray( static_cast<UINT>( colorBuffer.size() ), &colorBuffer[0], ColorImageFormat::ColorImageFormat_Bgra ) );
}

// Update Body
inline void Kinect::updateBody()
{
	// Retrieve Body Frame
	ComPtr<IBodyFrame> bodyFrame;
	const HRESULT ret = bodyFrameReader->AcquireLatestFrame(&bodyFrame);
	if (FAILED(ret)) {
		return;
	}

	// Release Previous Bodies
	Concurrency::parallel_for_each(bodies.begin(), bodies.end(), [](IBody*& body) {
		SafeRelease(body);
	});

	// Retrieve Body Data
	ERROR_CHECK(bodyFrame->GetAndRefreshBodyData(static_cast<UINT>(bodies.size()), &bodies[0]));
	//ERROR_CHECK(bodyFrame->GetAndRefreshBodyData(static_cast<UINT>(1), &bodies[0]));

	// Find Closest Body
	findClosestBody(bodies);

	findLRHandPos();

	// 손 활성화 확인
	{
		if (sPoints[SPOINT_BODY_WRIST_LEFT].getPoint().Y > sPoints[SPOINT_BODY_SPINE_BASE].getPoint().Y + spinePx / 2)
		{
			leftHandActivated = true;
		}
		else leftHandActivated = false;

		if (sPoints[SPOINT_BODY_WRIST_RIGHT].getPoint().Y > sPoints[SPOINT_BODY_SPINE_BASE].getPoint().Y + spinePx / 2)
		{
			rightHandActivated = true;
		}
		else rightHandActivated = false;
	}
}



// Update HDFace
inline void Kinect::updateHDFace()
{
	// Retrieve HDFace Frame
	ComPtr<IHighDefinitionFaceFrame> hdFaceFrame;
	const HRESULT ret = hdFaceFrameReader->AcquireLatestFrame(&hdFaceFrame);
	if (FAILED(ret)) {
		return;
	}

	// Check Traced
	ERROR_CHECK(hdFaceFrame->get_IsFaceTracked(&tracked));
	if (!tracked) {

		return;
	}
	// Retrieve Face Alignment Result
	ERROR_CHECK(hdFaceFrame->GetAndRefreshFaceAlignmentResult(faceAlignment.Get()));
}

void Kinect::updateSPoint()
{
	const ComPtr<IBody> body = bodies[trackingCount];

	// Retrieve Joint (Head), calculste spinepx
	std::array<Joint, JointType::JointType_Count> joints;
	ERROR_CHECK(body->GetJoints(static_cast<UINT>(joints.size()), &joints[0]));
	const Joint jointA = joints[JointType::JointType_SpineShoulder];
	const Joint jointB = joints[JointType::JointType_SpineMid];
	spinePx = (float)distance3d(jointA.Position, jointB.Position);

	sPoints[SPOINT_HEAD_HAIR].setPoint(vertexes[28]);
	sPoints[SPOINT_HEAD_FACE_EYE_LEFT].setPoint(vertexes[333]);
	sPoints[SPOINT_HEAD_FACE_EYE_RIGHT].setPoint(vertexes[732]);
	sPoints[SPOINT_HEAD_FACE_NOSE].setPoint(vertexes[23]);
	sPoints[SPOINT_HEAD_FACE_LIP].setPoint(vertexes[8]);
	sPoints[SPOINT_HEAD_FACE_CHEEK_LEFT].setPoint(vertexes[52]);
	sPoints[SPOINT_HEAD_FACE_CHEEK_RIGHT].setPoint(vertexes[581]);
	sPoints[SPOINT_HEAD_FACE_JAW].setPoint(vertexes[0]);

	sPoints[SPOINT_BODY_NECK].setPoint(joints[JointType::JointType_Neck].Position);
	sPoints[SPOINT_BODY_SPINE_MID].setPoint(joints[JointType::JointType_SpineMid].Position);
	sPoints[SPOINT_BODY_SPINE_BASE].setPoint(joints[JointType::JointType_SpineBase].Position);
	sPoints[SPOINT_BODY_SPINE_SHOULDER].setPoint(joints[JointType::JointType_SpineShoulder].Position);
	sPoints[SPOINT_BODY_SHOULDER_LEFT].setPoint(joints[JointType::JointType_ShoulderLeft].Position);
	sPoints[SPOINT_BODY_SHOULDER_RIGHT].setPoint(joints[JointType::JointType_ShoulderRight].Position);
	sPoints[SPOINT_BODY_ELBOW_LEFT].setPoint(joints[JointType::JointType_ElbowLeft].Position);
	sPoints[SPOINT_BODY_ELBOW_RIGHT].setPoint(joints[JointType::JointType_ElbowRight].Position);
	sPoints[SPOINT_BODY_WRIST_LEFT].setPoint(joints[JointType::JointType_WristLeft].Position);
	sPoints[SPOINT_BODY_WRIST_RIGHT].setPoint(joints[JointType::JointType_WristRight].Position);
	sPoints[SPOINT_BODY_HAND_TIP_LEFT].setPoint(joints[JointType::JointType_HandTipLeft].Position);
	sPoints[SPOINT_BODY_HAND_TIP_RIGHT].setPoint(joints[JointType::JointType_HandTipRight].Position);

	// additional points
	addtionalPoints[0].X = sPoints[SPOINT_HEAD_HAIR].getPoint().X;
	addtionalPoints[0].Y = sPoints[SPOINT_HEAD_HAIR].getPoint().Y + spinePx;
	addtionalPoints[0].Z = sPoints[SPOINT_HEAD_HAIR].getPoint().Z;
	addtionalPoints[1].X = sPoints[SPOINT_HEAD_FACE_NOSE].getPoint().X - spinePx;
	addtionalPoints[1].Y = sPoints[SPOINT_HEAD_FACE_NOSE].getPoint().Y;
	addtionalPoints[1].Z = sPoints[SPOINT_HEAD_FACE_NOSE].getPoint().Z;
	addtionalPoints[2].X = sPoints[SPOINT_HEAD_FACE_NOSE].getPoint().X + spinePx;
	addtionalPoints[2].Y = sPoints[SPOINT_HEAD_FACE_NOSE].getPoint().Y;
	addtionalPoints[2].Z = sPoints[SPOINT_HEAD_FACE_NOSE].getPoint().Z;

	sPoints[SPOINT_HEAD_TOP].setPoint(addtionalPoints[0]);
	sPoints[SPOINT_HEAD_SIDE_LEFT].setPoint(addtionalPoints[1]);
	sPoints[SPOINT_HEAD_SIDE_RIGHT].setPoint(addtionalPoints[2]);

	// version2 points
	sPoints[SPOINT_BODY_HIP_LEFT].setPoint(joints[JointType::JointType_HipLeft].Position);
	sPoints[SPOINT_BODY_HIP_RIGHT].setPoint(joints[JointType::JointType_HipRight].Position);
	sPoints[SPOINT_BODY_KNEE_LEFT].setPoint(joints[JointType::JointType_KneeLeft].Position);
	sPoints[SPOINT_BODY_KNEE_RIGHT].setPoint(joints[JointType::JointType_KneeRight].Position);
	sPoints[SPOINT_BODY_ANKLE_LEFT].setPoint(joints[JointType::JointType_AnkleLeft].Position);
	sPoints[SPOINT_BODY_ANKLE_RIGHT].setPoint(joints[JointType::JointType_AnkleRight].Position);

	// version2 addtional points
	addtionalPoints[3].X = sPoints[SPOINT_BODY_HIP_LEFT].getPoint().X - spinePx;
	addtionalPoints[3].Y = sPoints[SPOINT_BODY_HIP_LEFT].getPoint().Y;
	addtionalPoints[3].Z = sPoints[SPOINT_BODY_HIP_LEFT].getPoint().Z;
	addtionalPoints[4].X = sPoints[SPOINT_BODY_HIP_RIGHT].getPoint().X + spinePx;
	addtionalPoints[4].Y = sPoints[SPOINT_BODY_HIP_RIGHT].getPoint().Y;
	addtionalPoints[4].Z = sPoints[SPOINT_BODY_HIP_RIGHT].getPoint().Z;
	addtionalPoints[5].X = sPoints[SPOINT_BODY_SHOULDER_LEFT].getPoint().X - spinePx;
	addtionalPoints[5].Y = sPoints[SPOINT_BODY_SHOULDER_LEFT].getPoint().Y;
	addtionalPoints[5].Z = sPoints[SPOINT_BODY_SHOULDER_LEFT].getPoint().Z;
	addtionalPoints[6].X = sPoints[SPOINT_BODY_SHOULDER_RIGHT].getPoint().X + spinePx;
	addtionalPoints[6].Y = sPoints[SPOINT_BODY_SHOULDER_RIGHT].getPoint().Y;
	addtionalPoints[6].Z = sPoints[SPOINT_BODY_SHOULDER_RIGHT].getPoint().Z;
	addtionalPoints[7].X = sPoints[SPOINT_BODY_KNEE_LEFT].getPoint().X - spinePx;
	addtionalPoints[7].Y = sPoints[SPOINT_BODY_KNEE_LEFT].getPoint().Y;
	addtionalPoints[7].Z = sPoints[SPOINT_BODY_KNEE_LEFT].getPoint().Z;
	addtionalPoints[8].X = sPoints[SPOINT_BODY_KNEE_RIGHT].getPoint().X + spinePx;
	addtionalPoints[8].Y = sPoints[SPOINT_BODY_KNEE_RIGHT].getPoint().Y;
	addtionalPoints[8].Z = sPoints[SPOINT_BODY_KNEE_RIGHT].getPoint().Z;
	addtionalPoints[9].X = sPoints[SPOINT_BODY_SPINE_MID].getPoint().X - spinePx;
	addtionalPoints[9].Y = sPoints[SPOINT_BODY_SPINE_MID].getPoint().Y;
	addtionalPoints[9].Z = sPoints[SPOINT_BODY_SPINE_MID].getPoint().Z;
	addtionalPoints[10].X = sPoints[SPOINT_BODY_SPINE_MID].getPoint().X + spinePx;
	addtionalPoints[10].Y = sPoints[SPOINT_BODY_SPINE_MID].getPoint().Y;
	addtionalPoints[10].Z = sPoints[SPOINT_BODY_SPINE_MID].getPoint().Z;

	sPoints[SPOINT_BODY_HIP_SIDE_LEFT].setPoint(addtionalPoints[3]);
	sPoints[SPOINT_BODY_HIP_SIDE_RIGHT].setPoint(addtionalPoints[4]);
	sPoints[SPOINT_BODY_SHOULDER_SIDE_LEFT].setPoint(addtionalPoints[5]);
	sPoints[SPOINT_BODY_SHOULDER_SIDE_RIGHT].setPoint(addtionalPoints[6]);
	sPoints[SPOINT_BODY_KNEE_SIDE_LEFT].setPoint(addtionalPoints[7]);
	sPoints[SPOINT_BODY_KNEE_SIDE_RIGHT].setPoint(addtionalPoints[8]);
	sPoints[SPOINT_BODY_SPINE_MID_SIDE_LEFT].setPoint(addtionalPoints[9]);
	sPoints[SPOINT_BODY_SPINE_MID_SIDE_RIGHT].setPoint(addtionalPoints[10]);
}

void Kinect::updateStatus()
{

	// 초당프레임 계산
	{
		TIMESPAN dur = lastFrameRelativeTime - pastFrameRelativeTime;
		fps = (double)10000000 / dur; // sec / dur

		pastFrameRelativeTime = lastFrameRelativeTime;
	}
}

void Kinect::updateFrame()
{
	if (!frameStacking)
	{
		// 기록 시작
		if (leftHandActivated || rightHandActivated)
		{
			recordStartTime = lastFrameRelativeTime;
			frameStacking = true;
		}
	}
	else
	{
		// 기록 끝
		if (frameStacking && (!leftHandActivated && !rightHandActivated))
		{
			if (frameCollection.getCollectionSize() > 20)
			{
				switch (mode)
				{
				case KINECT_MODE_PREDICT:

					frameCollection.setStandard(recordStartTime);
					frameCollection.getData(data);
					isDataready = true;
					
					//lastPredict = lmapper.labelMap(cnn.predict_class(frameCollection.getDate()));
					break;

				case KINECT_MODE_OUTPUT:

					// record
					frameCollection.setStandard(recordStartTime);
					save();
					++recorded;
					break;
				}
			}

			frameStacking = false;
			frameCollection.clear();
		}
	}

	if (frameStacking)
	{
		Frame f;
		f.memorize(lHandPos, rHandPos, sPoints, leftHandActivated, rightHandActivated, lastFrameRelativeTime);

		frameCollection.stackFrame(f);
	}
}

void Kinect::save()
{
	frameCollection.setLabel(LABEL(label));

	stringstream sstream;
	sstream << frameCollection.toString() << endl;

	string filePath = "../data/" + currentDateTime() + "_" + frameCollection.getLabel() + ".txt";

	// write File
	ofstream writeFile(filePath.data(), std::ios_base::app);
	if (writeFile.is_open()) {
		writeFile << sstream.str();
		writeFile.close();
		static int i = 0;

		cout << "Record saving done " << ++i << endl;
	}
	else cout << "Record saving fail" << endl;
}

// Draw Data
void Kinect::draw()
{
    // Draw Color
    drawColor();

	// Draw Body
	//drawBody();

	drawHDFace(); // and update vertexs... but draw verxexs

	drawSPoint();

	drawStatusText();
}


// Draw HDFace
inline void Kinect::drawHDFace()
{
	if (colorMat.empty()) {
		return;
	}

	if (!tracked) return; 

	// status
	ERROR_CHECK(faceModelBuilder->get_CollectionStatus(&faceCollection));
	ERROR_CHECK(faceModelBuilder->get_CaptureStatus(&faceCapture));

	// Retrieve Vertexes
	ERROR_CHECK(faceModel->CalculateVerticesForAlignment(faceAlignment.Get(), vertexCount, &vertexes[0]));
	//drawVertexes(colorMat, vertexes, 1, colors[trackingCount]);
	

	/*
	// Retrieve Head Pivot Point
	CameraSpacePoint point;
	ERROR_CHECK( faceAlignment->get_HeadPivotPoint( &point ) );
	std::cout << point.X << ", " << point.Y << ", " << point.Z << std::endl;
	*/

	/*
	// Retrieve Animation Units ... Motion of Face Parts that Represent Expression (17 AUs)
	std::array<float, FaceShapeAnimations::FaceShapeAnimations_Count> animationUnits;
	ERROR_CHECK( faceAlignment->GetAnimationUnits( FaceShapeAnimations::FaceShapeAnimations_Count, &animationUnits[0] ) );
	for( const float animationUnit : animationUnits ){
	std::cout << std::to_string( animationUnit ) << std::endl;
	}
	*/

	/*
	// Retrieve Shape Units ... Deformations from Default Face Model (94 SUs)
	ERROR_CHECK( faceModel->GetFaceShapeDeformations( FaceShapeDeformations::FaceShapeDeformations_Count, &shapeUnits[0] ) );
	for( const float shapeUnit : shapeUnits ){
	std::cout << std::to_string( shapeUnit ) << std::endl;
	}
	*/

	/*
	// Retrieve Face Model Scale
	float scale;
	ERROR_CHECK( faceModel->get_Scale( &scale ) );
	std::cout << std::to_string( scale ) << std::endl;
	*/

	/*
	// Retrieve Hair Color (XBGR)
	// Set FaceModelBuilderAttributes::FaceModelBuilderAttributes_HairColor to IHighDefinitionFaceFrameSource::OpenModelBuilder()
	UINT32 hairColor;
	ERROR_CHECK( faceModel->get_HairColor( &hairColor ) );
	std::cout << ( ( hairColor & 0xff000000 ) >> 24 ) << std::endl; // X
	std::cout << ( ( hairColor & 0x00ff0000 ) >> 16 ) << std::endl; // B
	std::cout << ( ( hairColor & 0x0000ff00 ) >>  8 ) << std::endl; // G
	std::cout << ( ( hairColor & 0x000000ff ) >>  0 ) << std::endl; // R
	*/

	/*
	// Retrieve Skin Color (XBGR)
	// Set FaceModelBuilderAttributes::FaceModelBuilderAttributes_SkinColor to IHighDefinitionFaceFrameSource::OpenModelBuilder()
	UINT32 skinColor;
	ERROR_CHECK( faceModel->get_SkinColor( &skinColor ) );
	std::cout << ( ( skinColor & 0xff000000 ) >> 24 ) << std::endl; // X
	std::cout << ( ( skinColor & 0x00ff0000 ) >> 16 ) << std::endl; // B
	std::cout << ( ( skinColor & 0x0000ff00 ) >>  8 ) << std::endl; // G
	std::cout << ( ( skinColor & 0x000000ff ) >>  0 ) << std::endl; // R
	*/
}

// Draw Vertexes (HDFACE)
inline void Kinect::drawVertexes(cv::Mat& image, const std::vector<CameraSpacePoint> vertexes, const int radius, const cv::Vec3b& color, const int thickness)
{
	if (image.empty()) {
		return;
	}

	// Draw Vertex Points Converted to Color Coordinate System
	Concurrency::parallel_for_each(vertexes.begin(), vertexes.end(), [&](const CameraSpacePoint vertex) {
		ColorSpacePoint point;
		ERROR_CHECK(coordinateMapper->MapCameraPointToColorSpace(vertex, &point));
		const int x = static_cast<int>(point.X + 0.5f);
		const int y = static_cast<int>(point.Y + 0.5f);
		if ((0 <= x) && (x < image.cols) && (0 <= y) && (y < image.rows)) {
			cv::circle(image, cv::Point(x, y), radius, color, thickness, cv::LINE_AA);
		}
	});
}


// Draw Color
inline void Kinect::drawColor()
{
    // Create cv::Mat from Color Buffer
    colorMat = cv::Mat( colorHeight, colorWidth, CV_8UC4, &colorBuffer[0] );
}

// Draw Body
inline void Kinect::drawBody()
{
	// Draw Body Data to Color Data
	Concurrency::parallel_for(0, BODY_COUNT, [&](const int count) {
		const ComPtr<IBody> body = bodies[count];
		if (body == nullptr) {
			return;
		}

		// Check Body Tracked
		BOOLEAN tracked = FALSE;
		ERROR_CHECK(body->get_IsTracked(&tracked));
		if (!tracked) {
			return;
		}

		// Retrieve Joints
		std::array<Joint, JointType::JointType_Count> joints;
		ERROR_CHECK(body->GetJoints(static_cast<UINT>(joints.size()), &joints[0]));

		Concurrency::parallel_for_each(joints.begin(), joints.end(), [&](const Joint& joint) {
			// Check Joint Tracked
			if (joint.TrackingState == TrackingState::TrackingState_NotTracked) {
				return;
			}

			// Draw Joint Position
			drawEllipse(colorMat, joint.Position, 5, colors[count]);

		});

		/*
		// Retrieve Joint Orientations
		std::array<JointOrientation, JointType::JointType_Count> orientations;
		ERROR_CHECK( body->GetJointOrientations( JointType::JointType_Count, &orientations[0] ) );
		*/

		/*
		// Retrieve Amount of Body Lean
		PointF amount;
		ERROR_CHECK( body->get_Lean( &amount ) );
		*/
	});
}

void Kinect::drawSPoint()
{
	Concurrency::parallel_for_each(sPoints.begin(), sPoints.end(), [&](SPoint& sPoint)
	{
		if (!tracked && sPoint.getType() <= 10) return;

		if (leftHandActivated && sPoint.getType() == SPOINT_BODY_WRIST_LEFT)
		{
			drawEllipse(colorMat, sPoint.getPoint(), 5, cv::Vec3b(0, 255, 0));
		}
		else if (rightHandActivated && sPoint.getType() == SPOINT_BODY_WRIST_RIGHT)
		{
			drawEllipse(colorMat, sPoint.getPoint(), 5, cv::Vec3b(0, 255, 0));
		}
		else drawEllipse(colorMat, sPoint.getPoint(), 5, colors[trackingCount]);

	});



}


// Draw Ellipse
inline void Kinect::drawEllipse(cv::Mat& image, const CameraSpacePoint& pos, const int radius, const cv::Vec3b& color, const int thickness)
{
	if (image.empty()) {
		return;
	}

	// Convert Coordinate System and Draw Joint
	ColorSpacePoint colorSpacePoint;
	ERROR_CHECK(coordinateMapper->MapCameraPointToColorSpace(pos, &colorSpacePoint));
	const int x = static_cast<int>(colorSpacePoint.X + 0.5f);
	const int y = static_cast<int>(colorSpacePoint.Y + 0.5f);
	if ((0 <= x) && (x < image.cols) && (0 <= y) && (y < image.rows)) {
		cv::circle(image, cv::Point(x, y), radius, static_cast<cv::Scalar>(color), thickness, cv::LINE_AA);
	}
}

void Kinect::drawStatusText()
{
	int yd = 50;
	int fontFace = cv::FONT_HERSHEY_SIMPLEX;
	double fontScale = 1;
	int fontThickness = 2;
	cv::Point point = cv::Point(50, 50);
	cv::Mat srcMat = colorMat;

	yd = (int)(cv::getTextSize("a", fontFace, fontScale, fontThickness, nullptr).height * 1.4);
	
#ifdef Show_Status_FPS
	// Frame rate
	{
		statusStream << "ColorFrame RelativeTime : " << lastFrameRelativeTime;
		cv::putText(srcMat, statusStream.str(), point, fontFace, fontScale, statusFontColor, fontThickness);
		point.y += yd;
		statusStream.str("");

		statusStream << "FPS : " << fps;
		cv::putText(srcMat, statusStream.str(), point, fontFace, fontScale, statusFontColor, fontThickness);
		point.y += yd;
		statusStream.str("");

	}
#endif

#ifdef Show_Status_Mode
	cv::putText(srcMat, "Mode : " + to_string(mode), point, fontFace, fontScale, statusFontColor, fontThickness);
	point.y += yd;
	statusStream.str("");

	cv::putText(srcMat, "Label number : " + LABEL(label), point, fontFace, fontScale, statusFontColor, fontThickness);
	point.y += yd;
	statusStream.str("");
#endif


#ifdef Show_Status_Basic
	cv::putText(srcMat, "Distance : " + std::to_string(distance), point, fontFace, fontScale, statusFontColor, fontThickness);
	point.y += yd;
	statusStream.str("");

	cv::putText(srcMat, "Spinepx : " + std::to_string(spinePx), point, fontFace, fontScale, statusFontColor, fontThickness);
	point.y += yd;
#endif

#ifdef Show_Status_MLVar
	cv::putText(srcMat, "LHandActivated : " + std::to_string(leftHandActivated), point, fontFace, fontScale, statusFontColor, fontThickness);
	point.y += yd;
	statusStream.str("");

	cv::putText(srcMat, "RHandActivated : " + std::to_string(rightHandActivated), point, fontFace, fontScale, statusFontColor, fontThickness);
	point.y += yd;
	statusStream.str("");

	cv::putText(srcMat, "Recording : " + std::to_string(frameStacking), point, fontFace, fontScale, statusFontColor, fontThickness);
	point.y += yd;
	statusStream.str("");

	cv::putText(srcMat, "StackedCnt : " + std::to_string(frameCollection.getCollectionSize()), point, fontFace, fontScale, statusFontColor, fontThickness);
	point.y += yd;
	statusStream.str("");
	
	if (mode == KINECT_MODE_OUTPUT)
	{
		cv::putText(srcMat, "RecordedCnt : " + std::to_string(recorded), point, fontFace, fontScale, statusFontColor, fontThickness);
		point.y += yd;
		statusStream.str("");
	}

	if (mode == KINECT_MODE_PREDICT)
	{
		cv::putText(srcMat, "LastPredicted : " + std::to_string(LABEL(lastPredict)), point, fontFace, fontScale, statusFontColor, fontThickness);
		point.y += yd;
		statusStream.str("");
	}

#endif

	// SPoint
#ifdef Show_Status_PointPos
	{
		int size = SPOINT_SIZE;
		stringstream putting[SPOINT_SIZE];

		Concurrency::parallel_for_each(sPoints.begin(), sPoints.end(), [&](SPoint& sPoint) {

			cv::Point parallelPoint = cv::Point(point);
			putting[sPoint.getType()].setf(ios::showpoint);
			putting[sPoint.getType()].precision(2);
			putting[sPoint.getType()]
				<< sPoint.getName() << " : "
				<< sPoint.getPoint().X << ", "
				<< sPoint.getPoint().Y << ", "
				<< sPoint.getPoint().Z;

			parallelPoint.y += yd * sPoint.getType();
			cv::putText(srcMat, putting[sPoint.getType()].str(), parallelPoint, fontFace, fontScale, statusFontColor, fontThickness);
		});

		point.y += SPOINT_SIZE * yd;
	}
#endif

#ifdef Show_Status_DistanceFrame
	{
		array<string, Show_Status_DistanceFrame_Size> strs = frameCollection.lastFrameToString();

		for (int i = 0; i < Show_Status_DistanceFrame_Size; ++i)
		{
			cv::putText(srcMat, strs[i], point, fontFace, fontScale, statusFontColor, fontThickness);
			point.y += yd;
			statusStream.str("");
		}
	}
#endif

#ifdef Show_Status_Face
	{
		if (tracked)
		{
			cv::putText(srcMat, status2string(faceCapture), point, fontFace, fontScale, statusFontColor, fontThickness);
			point.y += yd;
			statusStream.str("");

			cv::putText(srcMat, status2string(faceCollection), point, fontFace, fontScale, statusFontColor, fontThickness);
			point.y += yd;
			statusStream.str("");
		}
	}
#endif

}

// Show Data
void Kinect::show()
{
    // Show Color
    showColor();
}

// Show Color
inline void Kinect::showColor()
{
    if( colorMat.empty() ){
        return;
    }

    // Resize Image
    cv::Mat resizeMat;
    const double scale = 0.5;
    cv::resize( colorMat, resizeMat, cv::Size(), scale, scale );

    // Show Image
    cv::imshow( "Color", resizeMat );

	/*
	if (tracked && distance < 1)
	{
		vector<int> list = vector<int>();
		list.push_back(0);
		list.push_back(8);
		list.push_back(9);
		list.push_back(10);
		ColorSpacePoint point;
		for (int i = 0; i < list.size(); ++i)
		{
			ERROR_CHECK(coordinateMapper->MapCameraPointToColorSpace(vertexes[list[i]], &point));
			cv::putText(colorMat, to_string(list[i]), cv::Point(point.X, point.Y), cv::FONT_HERSHEY_SIMPLEX, 0.5, cv::Scalar(255, 255, 255, 0));
		}

		cv::imshow("Color", colorMat);
		Beep(1200, 100);
		cvWaitKey(0);
	}*/
	
	// hdface vertex cordinate saving to image
	/*if (tracked)
	{
		static int i = 0;

		if (distance < 1)
		{
			int end = i + 5;
			for (i; i < end && i < vertexCount; ++i)
			{

				ColorSpacePoint point;
				ERROR_CHECK(coordinateMapper->MapCameraPointToColorSpace(vertexes[i], &point));
				cv::putText(colorMat, to_string(i), cv::Point(point.X, point.Y), cv::FONT_HERSHEY_SIMPLEX, 0.5, cv::Scalar(255, 255, 255, 0));

			}
			Beep(1046.502, 10);
			string name = "img/test" + to_string(i) + ".jpg";
			cv::imwrite(name, colorMat);

			if (i >= vertexCount)
			{
				Beep(1046.502, 10000);
				cvWaitKey(0);
			}
		}
	}*/
}


// Draw Face Model Builder Status

// Convert Collection Status to String
inline std::string Kinect::status2string(const FaceModelBuilderCollectionStatus collection)
{
	std::string status;
	if (collection & FaceModelBuilderCollectionStatus::FaceModelBuilderCollectionStatus_TiltedUpViewsNeeded) {
		status = "Collection Status : Needed Tilted Up Views";
	}
	else if (collection & FaceModelBuilderCollectionStatus::FaceModelBuilderCollectionStatus_RightViewsNeeded) {
		status = "Collection Status : Needed Right Views";
	}
	else if (collection & FaceModelBuilderCollectionStatus::FaceModelBuilderCollectionStatus_LeftViewsNeeded) {
		status = "Collection Status : Needed Left Views";
	}
	else if (collection & FaceModelBuilderCollectionStatus::FaceModelBuilderCollectionStatus_FrontViewFramesNeeded) {
		status = "Collection Status : Needed Front View Frames";
	}

	return status;
}

// Convert Capture Status to String
inline std::string Kinect::status2string(const FaceModelBuilderCaptureStatus capture)
{
	std::string status;
	switch (capture) {
	case FaceModelBuilderCaptureStatus::FaceModelBuilderCaptureStatus_FaceTooFar:
		status = "Capture Status : Warning Face Too Far from Camera";
		break;
	case FaceModelBuilderCaptureStatus::FaceModelBuilderCaptureStatus_FaceTooNear:
		status = "Capture Status : WWarning Face Too Near to Camera";
		break;
	case FaceModelBuilderCaptureStatus::FaceModelBuilderCaptureStatus_MovingTooFast:
		status = "Capture Status : WWarning Moving Too Fast";
		break;
	default:
		status = "";
		break;
	}

	return status;
}

// Find Closest Body
void Kinect::findClosestBody(const std::array<IBody*, BODY_COUNT>& bodies)
{
#undef max
	float closestDistance = std::numeric_limits<float>::max();
	bool findClosest = false;
	
	for (int count = 0; count < BODY_COUNT; count++)
	{
		const ComPtr<IBody> body = bodies[count];
		BOOLEAN tracked;
		ERROR_CHECK(body->get_IsTracked(&tracked));
		if (!tracked) {
			continue;
		}
#define max(a,b)	(((a) > (b)) ? (a) : (b)) // 윈도우 디파인된 max 이 성가신놈 재 디파인..

		// Retrieve Joint (Head)
		std::array<Joint, JointType::JointType_Count> joints;
		ERROR_CHECK(body->GetJoints(static_cast<UINT>(joints.size()), &joints[0]));
		const Joint joint = joints[JointType::JointType_Head];
		if (joint.TrackingState == TrackingState::TrackingState_NotTracked) {
			continue;
		}

		// Calculate Distance from Sensor ( sqrt( x^2 + y^2 + z^2 ) )
		const CameraSpacePoint point = joint.Position;
		const float distance = std::sqrt(std::pow(point.X, 2) + std::pow(point.Y, 2) + std::pow(point.Z, 2));
		if (closestDistance <= distance) {
			continue;
		}
		closestDistance = distance; findClosest = true;

		// Retrieve Tracking ID
		UINT64 trackingId;
		ERROR_CHECK(body->get_TrackingId(&trackingId));
		if (this->trackingId == trackingId) {
			continue;
		}

		// Registration Tracking ID
		ComPtr<IHighDefinitionFaceFrameSource> hdFaceFrameSource;
		ERROR_CHECK(hdFaceFrameReader->get_HighDefinitionFaceFrameSource(&hdFaceFrameSource));
		ERROR_CHECK(hdFaceFrameSource->put_TrackingId(trackingId));

		// Update Current
		this->trackingId = trackingId;
		this->trackingCount = count;
		this->produced = false;

	}
	
	if (findClosest) this->distance = closestDistance;
}

void Kinect::findLRHandPos()
{
	std::array<Joint, JointType::JointType_Count> joints;
	ERROR_CHECK(bodies[trackingCount]->GetJoints(static_cast<UINT>(joints.size()), &joints[0]));
	Joint joint = joints[HAND_RECORD_TYPE_L];
	if (joint.TrackingState == TrackingState::TrackingState_NotTracked) {
		return;
	}
	lHandPos = joint.Position;

	joint = joints[HAND_RECORD_TYPE_R];
	if (joint.TrackingState == TrackingState::TrackingState_NotTracked) {
		return;
	}
	rHandPos = joint.Position;
}