// Oliver Tsang, June 2020
// Just playing around to learn OpenGL


#include <stdio.h>
#include <stdlib.h>

#include <GL/glew.h>
#include <GLFW/glfw3.h> // window+keyboard

#include <glm/glm.hpp> // 3D math oOoOo
using namespace glm;

#include "loadShaders.h"


int main (int argc, char **argv) {
    // initialize GLFW
    glewExperimental = true; // needed for core profile
    if (!glfwInit()) {
        fprintf(stderr, "Failed to initialize\n");
        return -1;
    }

    glfwWindowHint(GLFW_SAMPLES, 4); // 4x antialiasing
    glfwWindowHint(GLFW_RESIZABLE, GL_TRUE);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 4); // OpenGL version 4.1
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 1);
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);

    // Open a window and create its OpenGL context
    GLFWwindow* window; // often becomes a global variable for simplicity
    window = glfwCreateWindow( 1024, 768, "Triangle", NULL, NULL);

    if(window == NULL) {
        fprintf(stderr, "Failed to open GLFW window.\n");
        glfwTerminate();
        return -1;
    }

    glfwMakeContextCurrent(window); // Initialize GLEW

    glewExperimental = true; // needed in core profile
    if (glewInit() != GLEW_OK) {
        fprintf(stderr, "Failed to open GLFW window.\n");
        getchar();
        glfwTerminate();
        return -1;
    }


    // ensure we can capture the escape key
    glfwSetInputMode(window, GLFW_STICKY_KEYS,GL_TRUE);

    // Set background color
    glClearColor(0.0f, 0.0f, 0.4f, 0.0f);

    // create a vertex array object
    GLuint vertexArrayID;
    glGenVertexArrays(1, &vertexArrayID);
    glBindVertexArray(vertexArrayID);

    // Create and compile our GLSL program from the shaders
    GLuint programID = loadShaders("simpleVertexShader.vertexshader",
                                   "simpleFragmentShader.fragmentshader");

    // Create the triangle
    // array w/ 3 3-vectors
    static const GLfloat g_vertex_buffer_data [] = {
        -1.0f, -1.0f, 0.0f,
         1.0f, -1.0f, 0.0f,
         0.0f,  1.0f, 0.0f,
    };
    
    // create vertex buffer
    GLuint vertexBuffer; // identifier of the buffer created
    glGenBuffers(1, &vertexBuffer);
    glBindBuffer(GL_ARRAY_BUFFER, vertexBuffer);
    // pass vertices to OpenGL
    glBufferData(GL_ARRAY_BUFFER, sizeof(g_vertex_buffer_data),
                 g_vertex_buffer_data, GL_STATIC_DRAW);


    do {
        // clear the screen -- might cause flickering otherwise
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

        // draw triangle
        // use shader
        glUseProgram(programID);

        // first attribute buffer: vertices
        glEnableVertexAttribArray(0);
        glBindBuffer(GL_ARRAY_BUFFER, vertexBuffer);
        glVertexAttribPointer(
            0,         // attribute 0
            3,         // size
            GL_FLOAT,  // type
            GL_FALSE,  // normalization
            0,         // stride
            (void *) 0 // array buffer offset
        );

        glDrawArrays(GL_TRIANGLES, 0, 3); // 3 indices starting at 0 -> 1 triangle

        glDisableVertexAttribArray(0);

        // swap buffers
        glfwSwapBuffers(window);
        glfwPollEvents();

    } while (glfwGetKey(window, GLFW_KEY_ESCAPE) != GLFW_PRESS
             && glfwWindowShouldClose(window) == 0);
    // close the window when the escape key is pressed
    // or the window should be closed

    // clean up
    glDeleteBuffers(1, &vertexBuffer);
    glDeleteVertexArrays(1, &vertexArrayID);
    glDeleteProgram(programID);

    // close window and terminate glfw
    glfwTerminate();
    
    return 0;
}
