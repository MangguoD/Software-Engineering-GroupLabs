# Makefile for Lab1 DirectedGraph project

CXX      := g++
CXXFLAGS := -std=c++17 -O2 -Wall -I.
TARGET   := lab1
SRC      := lab1.cpp
HDR      := lab1.h

.PHONY: all run clean

all: $(TARGET)

$(TARGET): $(SRC) $(HDR)
	$(CXX) $(CXXFLAGS) $(SRC) -o $(TARGET)

run: all
	./$(TARGET)

clean:
	rm -f $(TARGET) *.o *.dot *.png