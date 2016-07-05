#pragma once


#ifdef MATHLIBRARY_EXPORTS
#define VISION_API __declspec(dllexport) 
#else
#define VISION_API __declspec(dllimport) 
#endif


namespace Vision
{

	int VISION_API testMain(void);

}