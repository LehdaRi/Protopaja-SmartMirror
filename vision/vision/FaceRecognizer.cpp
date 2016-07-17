#include "stdafx.h"
#include "FaceRecognizer.hpp"

#include <opencv2/imgproc/imgproc.hpp>
#include <chrono>
#include <iostream>


using namespace Vision;


FaceRecognizer::FaceRecognizer(void) {
	if (!_faceCascade.load("haarcascade_frontalface_alt.xml"))
		fprintf(stderr, "Error loading \"haarcascade_frontalface_alt.xml\"\n");
}

void FaceRecognizer::detectFaces(cv::Mat& frame) {
	if (frame.empty())
		printf("Frame empty");

	cv::cvtColor(frame, _grayFrame, CV_BGR2GRAY);
	cv::equalizeHist(_grayFrame, _grayFrame);

	std::chrono::time_point<std::chrono::system_clock> start, end;
	start = std::chrono::system_clock::now();

	//-- Detect faces
	_faceCascade.detectMultiScale(frame, _faces, 1.15, 3, 0 | CV_HAAR_SCALE_IMAGE, cv::Size(100, 100));

	for (auto& face : _faces) {
		cv::rectangle(frame, face, cv::Scalar(255, 0, 0), 3);
	}

	printf("nFaces: %u\n", _faces.size());

	end = std::chrono::system_clock::now();
	std::chrono::duration<double> time = end - start;
	std::cout << "duration: " << time.count() << std::endl;
}