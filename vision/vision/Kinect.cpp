#include "stdafx.h"
#include "Kinect.h"
#include "FaceRecognizer.h"

#include <chrono>
#include <iostream>


using namespace Vision;


Kinect::Kinect(void) :
	_sensor						(nullptr),
	_depthFrameSource			(nullptr),
	_depthFrameReader			(nullptr),
	_depthFrameData				(nullptr),
	_depthFrameDescription		(nullptr),
	_colorFrameSource			(nullptr),
	_colorFrameReader			(nullptr),
	_colorFrameData				(nullptr),
	_colorFrameDescription		(nullptr),
	_colorFrameMat				(cv::Size(1920, 1080), CV_8UC4)
	//_colorFrameDataConverted	(1920*1080*4, 0)
{
	//	Kinect sensor
	if (!SUCCEEDED(GetDefaultKinectSensor(&_sensor)))
		fprintf(stderr, "Error in kinect sensor initialization\n");
	if (!SUCCEEDED(_sensor->Open()))
		fprintf(stderr, "Error when opening kinect sensor data stream\n");
	
	//	Depth frame source
	if (!SUCCEEDED(_sensor->get_DepthFrameSource(&_depthFrameSource)))
		fprintf(stderr, "Error initializing depth frame source\n");
	//	Depth frame reader
	if (!SUCCEEDED(_depthFrameSource->OpenReader(&_depthFrameReader)))
		fprintf(stderr, "Error initializing depth frame reader\n");

	//	Color frame source
	if (!SUCCEEDED(_sensor->get_ColorFrameSource(&_colorFrameSource)))
		fprintf(stderr, "Error initializing color frame source\n");
	//	Color frame reader
	if (!SUCCEEDED(_colorFrameSource->OpenReader(&_colorFrameReader)))
		fprintf(stderr, "Error initializing color frame reader\n");
}

Kinect::~Kinect(void) {
	if (_depthFrameReader && !SUCCEEDED(_depthFrameReader->Release()))
		fprintf(stderr, "Error when releasing depth frame reader\n");

	if (_depthFrameSource && !SUCCEEDED(_depthFrameSource->Release()))
		fprintf(stderr, "Error when releasing depth frame source\n");

	if (_colorFrameReader && !SUCCEEDED(_colorFrameReader->Release()))
		fprintf(stderr, "Error when releasing color frame reader\n");

	if (_colorFrameSource && !SUCCEEDED(_colorFrameSource->Release()))
		fprintf(stderr, "Error when releasing color frame source\n");

	if (!SUCCEEDED(_sensor->Close()))
		fprintf(stderr, "Error when closing kinect sensor\n");
}

void Kinect::operator()(Texture* depthTexture) {
	//std::chrono::time_point<std::chrono::system_clock> start, end;
	//start = std::chrono::system_clock::now();

	//	depth 
	HRESULT hr = -1;
	USHORT nDepthMinReliableDistance = 0;
	USHORT nDepthMaxReliableDistance = 0;
	UINT		depthBufferCapacity;
	uint16_t*	depthBuffer;
	int depthFrameWidth = 512;
	int depthFrameHeight = 424;

	hr = _depthFrameReader->AcquireLatestFrame(&_depthFrameData);

	if (SUCCEEDED(hr)) hr = _depthFrameData->get_FrameDescription(&_depthFrameDescription);
	if (SUCCEEDED(hr)) hr = _depthFrameData->get_DepthMinReliableDistance(&nDepthMinReliableDistance);
	if (SUCCEEDED(hr)) hr = _depthFrameData->get_DepthMaxReliableDistance(&nDepthMaxReliableDistance);

	if (SUCCEEDED(hr) && depthTexture) {
		if (SUCCEEDED(_depthFrameDescription->get_Height(&depthFrameHeight)) &&
			SUCCEEDED(_depthFrameDescription->get_Width(&depthFrameWidth))) {
			
			hr = _depthFrameData->AccessUnderlyingBuffer(&depthBufferCapacity, &depthBuffer);
			if (SUCCEEDED(hr)) {
				glBindTexture(GL_TEXTURE_2D, *depthTexture);
				glTexImage2D(GL_TEXTURE_2D, 0, GL_R16, depthFrameWidth, depthFrameHeight, 0,
							 GL_RED, GL_UNSIGNED_SHORT, depthBuffer);
			}
			else
				fprintf(stderr, "Unable to read depth buffer\n");
		}
	}

	//	color 
	hr = -1;
	//BYTE*	colorBuffer;
	UINT	colorBufferCapacity = 0;
	int colorFrameWidth = 0;
	int colorFrameHeight = 0;

	hr = _colorFrameReader->AcquireLatestFrame(&_colorFrameData);

	if (SUCCEEDED(hr)) hr = _colorFrameData->get_FrameDescription(&_colorFrameDescription);

	if (SUCCEEDED(hr)) {
		if (SUCCEEDED(_colorFrameDescription->get_Height(&colorFrameHeight)) &&
			SUCCEEDED(_colorFrameDescription->get_Width(&colorFrameWidth))) {


			hr = _colorFrameData->CopyConvertedFrameDataToArray(colorFrameWidth * colorFrameHeight * 4 * sizeof(unsigned char),
				 _colorFrameMat.data, ColorImageFormat_Bgra);
			/*if (SUCCEEDED(hr)) {
				glBindTexture(GL_TEXTURE_2D, *colorTexture);
				glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, colorFrameWidth, colorFrameHeight, 0,
					GL_RGBA, GL_UNSIGNED_BYTE, _colorFrameMat.data);
			}
			else
				fprintf(stderr, "Unable to read color buffer\n");*/
		}
	}

	//	release
	if (_colorFrameDescription) {
		if (SUCCEEDED(_colorFrameDescription->Release()))
			_colorFrameDescription = nullptr;
		else
			fprintf(stderr, "Error when releasing depth color description\n");
	}
	if (_colorFrameData) {
		if (SUCCEEDED(_colorFrameData->Release()))
			_colorFrameData = nullptr;
		else
			fprintf(stderr, "Error when releasing color frame data\n");
	}
	if (_depthFrameDescription) {
		if (SUCCEEDED(_depthFrameDescription->Release()))
			_depthFrameDescription = nullptr;
		else
			fprintf(stderr, "Error when releasing depth frame description\n");
	}
	if (_depthFrameData) {
		if (SUCCEEDED(_depthFrameData->Release()))
			_depthFrameData = nullptr;
		else
			fprintf(stderr, "Error when releasing depth frame data\n");
	}

	//end = std::chrono::system_clock::now();
	//std::chrono::duration<double> time = end - start;
	//std::cout << "capturing kinect frames took: " << time.count() << "s\n";
}

void Kinect::writeColorToTexture(Texture& texture) {
	texture.update(_colorFrameMat.data, GL_BGRA);
}

void Kinect::detectFaces(FaceRecognizer& faceRecognizer) {
	if (_colorFrameMat.empty())
		return;
	faceRecognizer.detectFaces(_colorFrameMat);
}
