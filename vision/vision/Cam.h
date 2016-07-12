#pragma once


#include <cstdint>
#include <thread>
#include <opencv2/opencv.hpp>
#include <opencv/highgui.h>



namespace Vision {

	class Cam {
	public:
		Cam(int camId, uint32_t width, uint32_t height, double fps);

		void loop(void);
			
		void read(void);

		unsigned width(void) const;
		unsigned height(void) const;

		const cv::Mat& frame(void) const;

	private:
		std::thread				_thread;

		cv::VideoCapture		_cap;
		cv::Mat					_frame;
		unsigned				_width, _height;
		std::vector<uint8_t>	_frameData;
	};

}