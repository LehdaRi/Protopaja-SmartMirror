#pragma once


#include <Windows.h>
#include <Kinect.h>
#include <opencv2/opencv.hpp>
#include <vector>

#include "Texture.h"


namespace Vision {

	class FaceRecognizer;
	
	class Kinect {
	public:
		Kinect(void);
		~Kinect(void);

		Kinect(const Kinect&)				= delete;
		Kinect& operator=(const Kinect&)	= delete;

		void operator()(Texture* depthTexture);

		void writeColorToTexture(Texture& texture);
		void detectFaces(FaceRecognizer& faceRecognizer);

	private:
		IKinectSensor*			_sensor;

		IDepthFrameSource*		_depthFrameSource;
		IDepthFrameReader*		_depthFrameReader;
		IDepthFrame*			_depthFrameData;
		IFrameDescription*		_depthFrameDescription;

		IColorFrameSource*		_colorFrameSource;
		IColorFrameReader*		_colorFrameReader;
		IColorFrame*			_colorFrameData;
		IFrameDescription*		_colorFrameDescription;
		cv::Mat					_colorFrameMat;
	};


}