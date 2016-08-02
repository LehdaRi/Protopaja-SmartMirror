#include "stdafx.h"
#include "FaceRecognizer.h"

#include <opencv2/imgproc/imgproc.hpp>
#include <chrono>
#include <iostream>


using namespace Vision;


FaceRecognizer::FaceRecognizer(double minFeatureSize) :
	_minFeatureSize(minFeatureSize, minFeatureSize),
	_faceCNN("res/cnn/facesbinary.cnn")
{
	if (!_faceCascade.load("cascades/haarcascade_frontalface_alt.xml"))
		fprintf(stderr, "Error loading \"cascades/haarcascade_frontalface_alt.xml\"\n");
}

void FaceRecognizer::setMinFeatureSize(double minFeatureSize) {
	_minFeatureSize = cv::Size(minFeatureSize, minFeatureSize);
	printf("minFeatureSize: %0.2f", minFeatureSize);
}

void FaceRecognizer::detectFaces(cv::Mat& frame) {
	if (frame.empty()) {
		printf("Frame empty");
		return;
	}

	cv::cvtColor(frame, _grayFrame, CV_BGR2GRAY);
	cv::equalizeHist(_grayFrame, _grayFrame);

	//	BEGIN OF TEMP
	/*std::chrono::time_point<std::chrono::system_clock> start, end;
	start = std::chrono::system_clock::now();
	*///	END OF TEMP

	//	Detect faces
	_faceCascade.detectMultiScale(frame, _faceRects, 1.1, 6, 0 | CV_HAAR_SCALE_IMAGE, _minFeatureSize);
	
	if (_faceMats.size() < _faceRects.size())
		_faceMats.resize(_faceRects.size(), cv::Mat(64, 64, CV_8UC3));

	for (auto i = 0u; i < _faceRects.size(); ++i) {
		cv::rectangle(frame, _faceRects[i], cv::Scalar(0, 0, 255), 3);
		cv::resize(frame(_faceRects[i]), _faceMats[i], cv::Size(64, 64));
	}

	if (_faceRects.size() > 0) {
		auto& p = _faceCNN(_faceMats[0]);

		int maxIdPrediction = 0;
		for (auto i = 0u; i < 5; ++i) {
			if (p[i] > p[maxIdPrediction])
				maxIdPrediction = i;
		}

		switch (maxIdPrediction) {
		case 0:
			printf("Akseli\n");
			break;
		case 1:
			printf("Joonas\n");
			break;
		case 2:
			printf("Miika\n");
			break;
		case 3:
			printf("Maarek\n");
			break;
		case 4:
			printf("Karl\n");
			break;
		}
	}

	//	BEGIN OF TEMP
	/*
	printf("nFaces: %u\n", _faces.size());

	end = std::chrono::system_clock::now();
	std::chrono::duration<double> time = end - start;
	std::cout << "duration: " << time.count() << std::endl;
	*///	END OF TEMP

}
