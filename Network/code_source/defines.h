#pragma once

#include <iostream>
#include <stdlib.h> // system
#include <omp.h>

#define PRINT_DETAIL
#define WRITE_LOG
#define FAIL_STOP(check, msg) fail_than_stop(check, msg)

#define MOJO_AVX	// turn on AVX / SSE3 / SIMD optimizations
#define MOJO_OMP	// allow multi-threading through openmp
#define MOJO_INTERNAL_THREADING // try to speed forward pass with internal threading
#define MOJO_THREAD_THIS_LOOP(a) __pragma(omp parallel for num_threads(a))
#define MOJO_THREAD_THIS_LOOP_DYNAMIC(a) __pragma(omp parallel for schedule(dynamic) num_threads(a))

static void fail_than_stop(int t, const char *m)
{
	if (t <= 0)
	{
		std::cerr << "CRITICAL FAIL, STOP PROGRAM : " << m << std::endl;
		system("pause");
		return;
	}
}