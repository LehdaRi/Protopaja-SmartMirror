#pragma once


#include "Cam.h"
#include "Shader.h"
#include "Texture.h"
#include "Kinect.h"


#define QUAD(xPos, yPos, xSize, ySize) xPos, yPos, 0.0f,\
                                       xPos+xSize, yPos, 0.0f,\
                                       xPos, yPos+ySize, 0.0f,\
                                       xPos, yPos+ySize, 0.0f,\
                                       xPos+xSize, yPos, 0.0f,\
                                       xPos+xSize, yPos+ySize, 0.0f


namespace Vision {

	class Canvas {
	public:
		Canvas(void);

		void draw(void);
		void updateShader(void);

	private:
		GLuint		_vertexArrayId;
		GLuint		_vertexBufferId;

		Shader		_shader;

		Texture		_camTexture1;
		Texture		_camTexture2;
		Texture		_depthTexture;
		Texture		_colorTexture;

		Cam			_cam1;
		Cam			_cam2;
		Kinect		_kinect;
	};

}