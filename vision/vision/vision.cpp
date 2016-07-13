// vision.cpp : Defines the exported functions for the DLL application.
//

#include "stdafx.h"
#include "vision.h"

#include <SFML/Window.hpp>
#include <iostream>


using namespace std;


Vision::Vision::Vision(bool useCams, bool useWindow) :
	_device			(),
	_mainThread		(&Device::mainLoop, &_device, useCams, useWindow)
{}

Vision::Vision::~Vision(void) {
	_device.terminate();
	_mainThread.join();
}

bool Vision::Vision::pollEvent(Event* event) {
	if (event)
		return _device.pollEvent(*event);
	return false;
}