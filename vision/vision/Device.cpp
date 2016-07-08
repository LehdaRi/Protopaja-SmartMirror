#include "stdafx.h"
#include "Device.h"


using namespace Vision;


Device::Device(void) :
	_vertexArrayId	(0),
	_vertexBufferId	(0),
	_shader			("shaders/VS_Texture.glsl", "shaders/FS_Texture.glsl"),
	_camTexture1	(1920, 1080),
	_camTexture2	(1920, 1080),
	_depthTexture	(512, 424),
	_colorTexture	(1920, 1080),
	_cam1			(0, 1920, 1080, 30.0),
	_cam2			(1, 1920, 1080, 30.0)
{
	const GLfloat quads[] = {
		QUAD(-1.0f, -1.0f, 2.0f, 2.0f)
	};

	glGenVertexArrays(1, &_vertexArrayId);
	glBindVertexArray(_vertexArrayId);

	glGenBuffers(1, &_vertexBufferId);
	glBindBuffer(GL_ARRAY_BUFFER, _vertexBufferId);
	glBufferData(GL_ARRAY_BUFFER, sizeof(quads), quads, GL_STATIC_DRAW);

	glEnableVertexAttribArray(0);
	glBindBuffer(GL_ARRAY_BUFFER, _vertexBufferId);
	glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, (void*)0);

	glBindVertexArray(0);

	//_texture1.loadFromFile("test6a.png");
}

void Device::draw(void) {
	//	update textures
	_cam1.read();
	_cam2.read();
	//printf("%u ", _cam1.frame().data[20000]);
	_camTexture1.updateFromCam(_cam1);
	_camTexture2.updateFromCam(_cam2);

	_shader.use();
	_kinect(_depthTexture, _colorTexture);

	glBindVertexArray(_vertexArrayId);

	glActiveTexture(GL_TEXTURE0);
	glBindTexture(GL_TEXTURE_2D, (GLuint)_camTexture1);
	glUniform1i(glGetUniformLocation(_shader.getId(), "camTex1"), 0);
	glActiveTexture(GL_TEXTURE1);
	glBindTexture(GL_TEXTURE_2D, (GLuint)_camTexture2);
	glUniform1i(glGetUniformLocation(_shader.getId(), "camTex2"), 1);
	glActiveTexture(GL_TEXTURE2);
	glBindTexture(GL_TEXTURE_2D, (GLuint)_depthTexture);
	glUniform1i(glGetUniformLocation(_shader.getId(), "depthTex"), 2);
	glActiveTexture(GL_TEXTURE3);
	glBindTexture(GL_TEXTURE_2D, (GLuint)_colorTexture);
	glUniform1i(glGetUniformLocation(_shader.getId(), "colorTex"), 3);
	glDrawArrays(GL_TRIANGLES, 0, 6);

	glBindVertexArray(0);
	glBindTexture(GL_TEXTURE_2D, 0);
}

void Device::updateShader(void) {
	_shader = Shader("shaders/VS_Texture.glsl", "shaders/FS_Texture.glsl");
}