#pragma once


#include "config.h"


extern "C" {

	struct VISION_API Event {
		/**	type
		*	0:	invalid type
		*	1:	person entered
		*	2:	person exited
		*	3:	gesture
		*	4:	face added to image
		*	5:	image added to database
		*/
		int type;

		/**	data
		*	depends on type:
		*	person entered(1):	id of the person
		*	person exited(2):	id of the person
		*	gesture(3):			id of the gesture (will be specified later)
		*	face added(4):		id of the face in image (0-255)
		*	image added(5):		id of the face in database
		*/
		int data;
	};

}