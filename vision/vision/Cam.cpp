#include "stdafx.h"
#include "Cam.h"
#include "Texture.h"
#include "FaceRecognizer.h"


using namespace Vision;


Cam::Cam(int camId, uint32_t width, uint32_t height, double fps) :
	_running	(true),
	_camId		(camId),
	_width		(width),
	_height		(height),
	_cap		(_camId)
{
	if (!_cap.isOpened()) {
		std::cerr << "Cannot open the video cam" << std::endl;
		return;
	}

	if (!_cap.read(_frame))
		std::cout << "Cannot read a frame from video stream" << std::endl;

	_cap.set(CV_CAP_PROP_FOURCC, CV_FOURCC('M', 'J', 'P', 'G'));
	_cap.set(CV_CAP_PROP_FRAME_WIDTH, _width);
	_cap.set(CV_CAP_PROP_FRAME_HEIGHT, _height);
	_cap.set(CV_CAP_PROP_FPS, fps);

	_width = _cap.get(CV_CAP_PROP_FRAME_WIDTH);
	_height = _cap.get(CV_CAP_PROP_FRAME_HEIGHT);

	_frameData.resize(_width * _height * 3, 0);
	int fs[] = { (int)_width, (int)_height };

	_frame = cv::Mat(2, fs, CV_8UC3, &_frameData[0]);
	if (!_cap.read(_frame)) {
		std::cerr << "Cannot read a frame from video stream" << std::endl;
		return;
	}
}

void Cam::loop(void) {
	while (_running) {
		std::unique_lock<std::mutex> lock(_mutex);
		//	wait for read call
		_cv.wait(lock, [this] { return _read; });


		//  read frame from webcam
		if (!_cap.read(_frame) || _frame.empty()) { // read a new frame from video
			std::cout << "Cannot read a frame from video stream" << std::endl;
			return;
		}

		//	reading done
		_read = false;
		lock.unlock();
		_cv.notify_all();
	}
}

void Cam::terminate(void) {
	_running = false;
}

void Cam::read(void) {
	_mutex.lock();
	_read = true;
	_mutex.unlock();
	_cv.notify_all();
}

unsigned Cam::width(void) const {
	return _width;
}

unsigned Cam::height(void) const {
	return _height;
}

void Cam::writeToTexture(Texture& texture) {
	std::lock_guard<std::mutex> lock(_mutex);
	texture.update(_frame.data, GL_BGR);
}

void Cam::detectFaces(FaceRecognizer& faceRecognizer, uint64_t& nFaces, uint64_t& faceId) {
	std::lock_guard<std::mutex> lock(_mutex);
	if (_frame.empty())
		return;
	faceRecognizer.detectFaces(_frame, nFaces, faceId);
}