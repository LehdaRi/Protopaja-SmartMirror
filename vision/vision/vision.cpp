// vision.cpp : Defines the exported functions for the DLL application.
//

#include "stdafx.h"
#include "vision.h"

#include <SFML/Window.hpp>
#include <iostream>


using namespace std;


Vision::Vision::Vision(void) :
	_device			(),
	_mainThread		(&Device::mainLoop, &_device, true)
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