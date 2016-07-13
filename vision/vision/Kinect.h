#pragma once


#include <Windows.h>
#include <Kinect.h>
#include <vector>

#include "Texture.h"


namespace Vision {

	
	class Kinect {
	public:
		Kinect(void);
		~Kinect(void);

		Kinect(const Kinect&)				= delete;
		Kinect& operator=(const Kinect&)	= delete;

		void operator()(Texture* depthTexture, Texture* colorTexture);

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
		std::vector<uint8_t>	_colorFrameDataConverted;
	};


}