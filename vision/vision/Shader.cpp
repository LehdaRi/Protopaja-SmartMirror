#include "stdafx.h"
#include "Shader.h"

#include <cstdio>
#include <memory>


using namespace Vision;


Shader::Shader(const std::string& vsFileName, const std::string& fsFileName) {
	FILE* vsf;
	fopen_s(&vsf, vsFileName.c_str(), "rb");
	if (!vsf)
		fprintf(stderr, "Unable to open vertex shader from file\n", vsFileName.c_str());

	FILE* fsf;
	fopen_s(&fsf, fsFileName.c_str(), "rb");
	if (!fsf)
		fprintf(stderr, "Unable to open fragment shader from file\n", vsFileName.c_str());
	
	fseek(vsf, 0L, SEEK_END);
	auto vsfs = ftell(vsf);
	std::unique_ptr<char> vsBufUnique(new char[vsfs + 1]);
	fseek(vsf, 0L, SEEK_SET);
	fread(vsBufUnique.get(), sizeof(char), vsfs, vsf);
	vsBufUnique.get()[vsfs] = '\0';
	fclose(vsf);
	const char* vsSrcPtr = vsBufUnique.get();
	
	fseek(fsf, 0L, SEEK_END);
	auto fsfs = ftell(fsf);
	std::unique_ptr<char> fsBufUnique(new char[fsfs + 1]);
	fseek(fsf, 0L, SEEK_SET);
	fread(fsBufUnique.get(), sizeof(char), fsfs, fsf);
	fsBufUnique.get()[fsfs] = '\0';
	fclose(fsf);
	const char* fsSrcPtr = fsBufUnique.get();
	
	GLuint vsObjectId = glCreateShader(GL_VERTEX_SHADER);
	GLuint fsObjectId = glCreateShader(GL_FRAGMENT_SHADER);

	GLint compileStatus, infoLogLength;

	glShaderSource(vsObjectId, 1, &vsSrcPtr, NULL);
	glCompileShader(vsObjectId);

	glGetShaderiv(vsObjectId, GL_COMPILE_STATUS, &compileStatus);
	if (compileStatus == GL_FALSE) {
		glGetShaderiv(vsObjectId, GL_INFO_LOG_LENGTH, &infoLogLength);

		char* infoLog = new char[infoLogLength];
		glGetShaderInfoLog(vsObjectId, infoLogLength, NULL, &infoLog[0]);
		fprintf(stderr, "%s", infoLog);
		//throw infoLog; // TODO_EXCEPTION: throw a proper exception
	}

	glShaderSource(fsObjectId, 1, &fsSrcPtr, NULL);
	glCompileShader(fsObjectId);

	glGetShaderiv(fsObjectId, GL_COMPILE_STATUS, &compileStatus);
	if (compileStatus == GL_FALSE) {
		glGetShaderiv(fsObjectId, GL_INFO_LOG_LENGTH, &infoLogLength);

		char* infoLog = new char[infoLogLength];
		glGetShaderInfoLog(fsObjectId, infoLogLength, NULL, &infoLog[0]);
		fprintf(stderr, "%s", infoLog);
		//throw infoLog; // TODO_EXCEPTION: throw a proper exception
	}

	programId_ = glCreateProgram();

	glAttachShader(programId_, fsObjectId);
	glAttachShader(programId_, vsObjectId);

	GLint linkStatus;

	glLinkProgram(programId_);

	glGetProgramiv(programId_, GL_LINK_STATUS, &linkStatus);
	if (linkStatus == GL_FALSE) {
		glGetShaderiv(programId_, GL_INFO_LOG_LENGTH, &infoLogLength);

		char* infoLog = new char[infoLogLength];
		glGetProgramInfoLog(programId_, infoLogLength, NULL, &infoLog[0]);
		fprintf(stderr, "%s", infoLog);
		//throw infoLog; // TODO_EXCEPTION: throw a proper exception
	}

	if (vsObjectId)
		glDeleteShader(vsObjectId);

	if (fsObjectId)
		glDeleteShader(fsObjectId);
}

Shader::~Shader(void) {
	if (programId_)
		glDeleteProgram(programId_);
}

Shader::Shader(Shader&& other) :
	programId_(other.programId_)
{
	other.programId_ = 0;
}

Shader& Shader::operator=(Shader&& other) {
	if (programId_)
		glDeleteProgram(programId_);

	programId_ = other.programId_;
	other.programId_ = 0;

	return *this;
}

GLuint Shader::getId(void) const {
	return programId_;
}

void Shader::use(void) {
	glUseProgram(programId_);
}
