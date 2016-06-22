#pragma once


// vision.h - Contains declaration of Function class
#pragma once

#ifdef MATHLIBRARY_EXPORTS
#define VISION_API __declspec(dllexport) 
#else
#define VISION_API __declspec(dllimport) 
#endif

namespace Vision
{

	int VISION_API testMain(void);

	class Functions
	{
	public:
		// Returns a + b
		static VISION_API double Add(double a, double b);

		// Returns a * b
		static VISION_API double Multiply(double a, double b);

		// Returns a + (a * b)
		static VISION_API double AddMultiply(double a, double b);
	};
}