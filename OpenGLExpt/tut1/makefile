CC = g++
OPT = -O0
WARNINGS = -Wall
DEBUG = -g3
CFLAGS = $(OPT) $(DEBUG) $(WARNINGS)
OBJS = main.o loadShaders.o
DEPS = loadShaders.h
OUTFILE = main
LIBS = -lGL -lGLEW -lGLU -lglfw3 -lX11 -lpthread -lXi -ldl

%.o: %.c
	$(CC) -c -o $@  $(DEPS) $(CFLAGS) $(LIBS)

make: $(OBJS)
	$(CC) -o $(OUTFILE) $(OBJS) $(DEPS) $(CFLAGS) $(LIBS)
