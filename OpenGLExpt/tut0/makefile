FILE = playground.cpp
CC = g++
OPT = -O0
WARNINGS = -Wall
DEBUG = -g3
CFLAGS = $(OPT) $(DEBUG) $(WARNINGS)
OBJS = playground.o
OUTFILE = playground

# LIBS = -L glfw3 -lGLEW -lGL
LIBS = -lGL -lGLEW -lGLU -lglfw3 -lX11 -lpthread -lXi -ldl
INCLUDE = -I /usr/local/include


%.o: %.c
	$(CC) -c  -o $@ $(INCLUDE) $(LIBS) $(CFLAGS)

make:
	$(CC) -o $(OUTFILE) $(OBJS) $(CFLAGS) $(LIBS)
