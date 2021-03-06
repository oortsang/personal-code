// Oliver Tsang, June 2020
// Just playing around to learn OpenGL


#include <stdio.h>
#include <stdlib.h>


#include <GL/glew.h>
#include <GLFW/glfw3.h> // window+keyboard

// #include <GLM/glm.hpp> // 3D math oOoOo
// using namespace glm;

int main (int argc, char **argv) {
    // initialize GLFW
    glewExperimental = true; // needed for core profile
    if (!glfwInit()) {
        fprintf(stderr, "Failed to initialize");
        return -1;
    }

    glfwWindowHint(GLFW_SAMPLES, 4); // 4x antialiasing
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 4); // OpenGL version 4.1
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 1);
    // glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE); // should only be needed for macos
    // glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILES); // don't want the old opengl

    // Open a window and create its OpenGL context
    GLFWwindow* window; // often becomes a global variable for simplicity
    window = glfwCreateWindow( 1024, 768, "Tutorial 0", NULL, NULL);

    if(window == NULL) {
        fprintf(stderr, "Failed to open GLFW window.");
        glfwTerminate();
        return -1;
    }

    glfwMakeContextCurrent(window); // Initialize GLEW
    glewExperimental = true; // needed in core profile
    if (glewInit() != GLEW_OK) {
        fprintf(stderr, "Failed to open GLFW window.");
        return -1;
    }


    // ensure we can capture the escape key
    glfwSetInputMode(window, GLFW_STICKY_KEYS,GL_TRUE);
    do {
        // clear the screen -- might cause flickering
        glClear(GL_COLOR_BUFFER_BIT);

        // not drawing anything for now

        // swap buffers
        glfwSwapBuffers(window);
        glfwPollEvents();

    } while (glfwGetKey(window, GLFW_KEY_ESCAPE) != GLFW_PRESS
             && glfwWindowShouldClose(window) == 0);
    // close the window when the escape key is pressed
    // or the window should be closed
    return 0;
}
