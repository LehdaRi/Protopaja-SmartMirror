// vision.cpp : Defines the exported functions for the DLL application.
//

#include "stdafx.h"
#include "vision.h"

#include <opencv2/opencv.hpp>
#include <opencv/highgui.h>


using namespace cv;


namespace Vision
{
	int testMain(void) {
		Mat image;          //Create Matrix to store image
		VideoCapture cap;          //initialize capture
		cap.open(0);
		namedWindow("window", 1);          //create window to show image
		while (1) {
			cap >> image;          //copy webcam stream to image
			imshow("window", image);          //print image to screen
			waitKey(33);          //delay 33ms
		}
		return 0;
	}

	double Functions::Add(double a, double b)
	{
		return a + b;
	}

	double Functions::Multiply(double a, double b)
	{
		return a * b;
	}

	double Functions::AddMultiply(double a, double b)
	{
		return a + (a * b);
	}
}

/**
#include <opencv2/opencv.hpp>
#include <opencv/highgui.h>


using namespace cv;


int main() {
    Mat image;          //Create Matrix to store image
    VideoCapture cap;          //initialize capture
    cap.open(0);
    namedWindow("window", 1);          //create window to show image
    while (1) {
        cap >> image;          //copy webcam stream to image
        imshow("window", image);          //print image to screen
        waitKey(33);          //delay 33ms
    }
    return 0;
}
**/