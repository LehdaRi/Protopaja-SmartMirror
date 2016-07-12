#pragma once


#include <thread>

#include "Device.h"


#ifdef MATHLIBRARY_EXPORTS
#define VISION_API __declspec(dllexport) 
#else
#define VISION_API __declspec(dllimport) 
#endif


namespace Vision
{

	class VISION_API Vision {
	public:
		Vision(void);
		~Vision(void);

		//	returns true if new event was found, 
		bool pollEvent(Event* event);

	private:
		Device		_device;
		std::thread	_mainThread;
	};
}