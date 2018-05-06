#pragma once

#define _WINSOCKAPI_ 
#include "MainTransaction.h"

int main(int argc, char* argv[])
{
	MainTransaction m;
	m.run();

	//system("pause");
	return 0;
}