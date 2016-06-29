#include "stdafx.h"
#include "Cam.h"


using namespace Vision;


Cam::Cam(int camId, uint32_t width, uint32_t height, double fps) :
	_cap(camId),
	_width(0), _height(0)
{
	if (!_cap.isOpened()) {
		std::cerr << "Cannot open the video cam" << std::endl;
		return;
	}

	_cap.set(CV_CAP_PROP_FRAME_WIDTH, _width);
	_cap.set(CV_CAP_PROP_FRAME_HEIGHT, _height);
	//cap.set(CV_CAP_PROP_FOURCC,CV_FOURCC('M','J','P','G'));
	_cap.set(CV_CAP_PROP_FPS, fps);

	_width = _cap.get(CV_CAP_PROP_FRAME_WIDTH);
	_height = _cap.get(CV_CAP_PROP_FRAME_HEIGHT);

	//_frameData.resize(0, _width * _height * 3);
	int fs[] = { (int)_width, (int)_height };

	_frame = cv::Mat(2, fs, CV_8UC3, &_frameData[0]);
	if (!_cap.read(_frame)) {
		std::cerr << "Cannot read a frame from video stream" << std::endl;
		return;
	}

	//texture_ = Texture<>(_width, _height, GL_RGB, GL_REPEAT, GL_REPEAT, _frame.data, GL_BGR);
}

void Cam::read(void) {
	//  read frame from webcam
	if (!_cap.read(_frame)) { // read a new frame from video
		std::cerr << "Cannot read a frame from video stream" << std::endl;
		return;
	}
}

unsigned Cam::width(void) const {
	return _width;
}

unsigned Cam::height(void) const {
	return _height;
}

const cv::Mat& Cam::frame(void) const {
	return _frame;
}