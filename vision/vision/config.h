#pragma once


#ifdef NDEBUG
#define VISION_API __declspec(dllexport) 
#else
#define VISION_API __declspec(dllimport) 
#endif

//	minimum size of face features relative to frame height
#define	VISION_DEVICE_MINFEATURESIZESCALE	0.15