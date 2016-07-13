#pragma once


#ifdef NDEBUG
#define VISION_API __declspec(dllexport) 
#else
#define VISION_API __declspec(dllimport) 
#endif