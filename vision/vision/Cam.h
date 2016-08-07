#pragma once


#include <cstdint>
#include <mutex>
#include <atomic>
#include <condition_variable>
#include <opencv2/opencv.hpp>
#include <opencv/highgui.h>



namespace Vision {

	class Texture;
	class FaceRecognizer;

	class Cam {
	public:
		Cam(int camId, uint32_t width, uint32_t height, double fps);

		void loop(void);
		void terminate(void);
			
		void read(void);

		unsigned width(void) const;
		unsigned height(void) const;

		void writeToTexture(Texture& texture);
		void detectFaces(FaceRecognizer& faceRecognizer, uint64_t& nFaces, uint64_t& faceId);

	private:
		std::atomic<bool>		_running;
		std::condition_variable	_cv;
		std::mutex				_mutex;
		bool					_read;

		int						_camId;
		unsigned				_width, _height;

		cv::VideoCapture		_cap;
		cv::Mat					_frame;

		std::vector<uint8_t>	_frameData;
	};

}