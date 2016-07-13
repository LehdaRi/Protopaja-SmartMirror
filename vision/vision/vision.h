#pragma once


#include <thread>

#include "Device.h"


namespace Vision
{

	class VISION_API Vision {
	public:
		Vision(bool useCams, bool useWindow);
		~Vision(void);

		//	returns true if new event was found, false otherwise
		bool pollEvent(Event* event);

	private:
		Device		_device;
		std::thread	_mainThread;
	};

}