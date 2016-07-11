#pragma once


#ifdef MATHLIBRARY_EXPORTS
#define VISION_API __declspec(dllexport) 
#else
#define VISION_API __declspec(dllimport) 
#endif


namespace Vision
{

	struct Event {
		/**	type
		*	0:	invalid type
		*	1:	person entered
		*	2:	person exited
		*	3:	gesture
		*/
		int type;

		/**	data
		*	depends on type:
		*	person entered(1):	id of the person
		*	person exited(2):	id of the person
		*	gesture(3):			id of the gesture (will be specified later)
		*/
		int data;
	};


	int VISION_API testMain(void);

	void VISION_API launchVision(void);
	void VISION_API terminateVision(void);

}