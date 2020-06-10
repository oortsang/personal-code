CC = g++
OPT = -O0
WARNINGS = -Wall
DEBUG = -g3
CFLAGS = $(OPT) $(DEBUG) $(WARNINGS)
OBJS = playground.o
OUTFILE = playground
LIBS = -lGL -lGLEW -lGLU -lglfw3 -lX11 -lpthread -lXi -ldl


%.o: %.c
	$(CC) -c  -o $@ $(CFLAGS) $(LIBS)

make: $(OBJS)
	$(CC) -o $(OUTFILE) $(OBJS) $(CFLAGS) $(LIBS)
