#include "stdafx.h"
#include "FaceRecognizer.h"

#include <opencv2/imgproc/imgproc.hpp>
#include <chrono>
#include <iostream>


using namespace Vision;


FaceRecognizer::FaceRecognizer(double minFeatureSize) :
	_minFeatureSize(minFeatureSize, minFeatureSize)
{
	if (!_faceCascade.load("haarcascade_frontalface_alt.xml"))
		fprintf(stderr, "Error loading \"haarcascade_frontalface_alt.xml\"\n");
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

	std::chrono::time_point<std::chrono::system_clock> start, end;
	start = std::chrono::system_clock::now();

	//	Detect faces
	_faceCascade.detectMultiScale(frame, _faces, 1.1, 6, 0 | CV_HAAR_SCALE_IMAGE, _minFeatureSize);
	
	for (auto& face : _faces) {
		cv::rectangle(frame, face, cv::Scalar(0, 0, 255), 3);
	}

	printf("nFaces: %u\n", _faces.size());

	end = std::chrono::system_clock::now();
	std::chrono::duration<double> time = end - start;
	std::cout << "duration: " << time.count() << std::endl;
}