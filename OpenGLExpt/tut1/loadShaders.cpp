// from http://www.opengl-tutorial.org/beginners-tutorials/tutorial-2-the-first-triangle/


#include <stdio.h>
#include <vector>
#include <string>
#include <fstream>
#include <iostream>
#include <sstream>
using namespace std;

#include <stdlib.h>
#include <string.h>

#include <GL/glew.h>

#include "loadShaders.h"

GLuint loadShaders(const char *vertexFilePath, const char *fragmentFilePath) {
    // Create shaders
    GLuint vertexShaderID = glCreateShader(GL_VERTEX_SHADER);
    GLuint fragmentShaderID = glCreateShader(GL_FRAGMENT_SHADER);

    // Read vertex shader code from file
    std::string vertexShaderCode;
    std::ifstream vertexShaderStream(vertexFilePath, std::ios::in);
    if (vertexShaderStream.is_open()) {
        std::stringstream sstr;
        sstr << vertexShaderStream.rdbuf();
        vertexShaderCode = sstr.str();
        vertexShaderStream.close();
    } else {
        fprintf(stderr, "Unable to open %s.\n", vertexFilePath);
        getchar();
        return 0;
    }

    // Read fragment shader code from the file
    std::string fragmentShaderCode;
    std::ifstream fragmentShaderStream(fragmentFilePath, std::ios::in);
    if (fragmentShaderStream.is_open()) {
        std::stringstream sstr;
        sstr << fragmentShaderStream.rdbuf();
        fragmentShaderCode = sstr.str();
        fragmentShaderStream.close();
    }

    GLint result = GL_FALSE;
    int infoLogLength;


    // Compile vertex shader
    printf("Compiling shader: %s\n", vertexFilePath);
    char const *vertexSourcePointer = vertexShaderCode.c_str();
    glShaderSource(vertexShaderID, 1, &vertexSourcePointer, NULL);
    glCompileShader(vertexShaderID);

    // Check Vertex Shader
    glGetShaderiv(vertexShaderID, GL_COMPILE_STATUS, &result);
    glGetShaderiv(vertexShaderID, GL_INFO_LOG_LENGTH, &infoLogLength);
    if (infoLogLength > 0) {
        std::vector<char> vertexShaderErrorMessage(infoLogLength+1);
        glGetShaderInfoLog(vertexShaderID, infoLogLength, NULL,
                           &vertexShaderErrorMessage[0]);
        fprintf(stderr, "%s\n", &vertexShaderErrorMessage[0]);
    }

    // Compile Fragment Shader
    printf("Compiling shader: %s\n", fragmentFilePath);
    char const *fragmentSourcePointer = fragmentShaderCode.c_str();
    glShaderSource(fragmentShaderID, 1, &fragmentSourcePointer, NULL);
    glCompileShader(fragmentShaderID);

    // Check Fragment Shader
    glGetShaderiv(fragmentShaderID, GL_COMPILE_STATUS, &result);
    glGetShaderiv(fragmentShaderID, GL_INFO_LOG_LENGTH, &infoLogLength);
    if (infoLogLength > 0) {
        std::vector<char> fragmentShaderErrorMessage(infoLogLength+1);
        glGetShaderInfoLog(fragmentShaderID, infoLogLength, NULL,
                           &fragmentShaderErrorMessage[0]);
        fprintf(stderr, "%s\n", &fragmentShaderErrorMessage[0]);
    }

    // Link the program
    printf("Linking program\n");
    GLuint programID = glCreateProgram();
    glAttachShader(programID, vertexShaderID);
    glAttachShader(programID, fragmentShaderID);
    glLinkProgram(programID);

    // Check the program
    glGetProgramiv(programID, GL_LINK_STATUS, &result);
    glGetProgramiv(programID, GL_INFO_LOG_LENGTH, &infoLogLength);
    if (infoLogLength > 0) {
        std::vector<char> programErrorMessage(infoLogLength+1);
        glGetProgramInfoLog(programID, infoLogLength, NULL,
                            &programErrorMessage[0]);
        fprintf(stderr, "%s\n", &programErrorMessage[0]);
    }

    glDetachShader(programID, vertexShaderID);
    glDetachShader(programID, fragmentShaderID);

    glDeleteShader(vertexShaderID);
    glDeleteShader(fragmentShaderID);

    return programID;
}
