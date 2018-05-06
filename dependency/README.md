# Install & Build Guide

모든 과정은 Windows 10 64bit 환경 기준입니다. 만약 link가 깨져있거나 설치 과정에 문제가 있으면 issue 부탁드립니다.

설치 순서는 C++/C# 개발 환경, Kinect, Python 개발 환경, Tensorflow, Keras, GPU 지원 순이며 Python 이후 부터는 설치 과정이 CLI 환경에서 이뤄집니다.

-------------------------------------------------------------------

## Index

1. [Enviroment Setting](#enviroment-setting)

    - [Install Kinect](#install-kinect)

    - [Install Keras](#install-keras)

    - [GPU using](#gpu-using)

1. [Building Guide](#building-guide)

-------------------------------------------------------------------

## Enviroment Setting

### Install Kinect

1. 빌드를 위해서 VC15(Visual studio 2017)가 필요하다. (C++/C# 개발 환경 설치) -> [site](https://docs.microsoft.com/ko-kr/visualstudio/install/install-visual-studio)

1. 빌드 파일 실행을 위해서는 vc 재배포 패키지 2012 설치가 필요하다. -> [link](https://github.com/crack-love/KSL/blob/master/dependency/vcredist_x64.exe)

1. 키넥트 런타임 패키지가 설치가 필요하다. -> [link](https://drive.google.com/open?id=1_m3lO9dSzmrTBmx_6e3x4FYEU7mtPwXO)

### Install Keras

1. 파이썬 3.5.x 설치가 필요하다. -> [3.5.4 link](https://drive.google.com/open?id=1RfJEmtT12EwDFq2U43h76c5uP0uOiKzq)

    ```powershell
    $ python --version
    Python 3.5.4
    ```

    파이썬 버전이 설치한 것과 다르게 나오면 PATH 환경변수를 확인하고 수정해야 한다.

1. pip(Pip Install Package) 최신버전 업데이트가 필요하다.

    ```powershell
    python -m pip install --upgrade pip
    ```

1. tensorflow 설치가 필요하다.

    ```powershell
    python -m pip install tensorflow

    $ python
    >>> import tensorflow as tf
    >>> tf.__version__
    '1.8.0'
    ```

1. keras 설치가 필요하다.

    ```powershell
    python -m pip install keras

    python -c "import keras; print(keras.__version__)"
    ```

1. 만약 CPU가 AVX, SSE, FMA 등 연산을 지원하면 tensorflow import 시 이를 이용하기를 권고한다.

    1. AVX, SSE 등은 CPU의 SIMD 부동 소수점 연산 명령어 조합의 최신 버전이다.

    1. CPU 연산 속도가 매우 빨라짐.

    1. tensorflow는 AVX 미지원 PC의 호환성을 위해 기본 빌드에는 포함시키지 않는다.

    1. 부동 소수점 명령어를 사용하려면 tensorflow를 clnoe해서 수동으로 빌드해야 한다.

    1. 만약 GPU를 사용하면 CPU의 연산은 영향이 거의 없기 때문에 필요 없다. [ref](https://stackoverflow.com/questions/43134753/tensorflow-wasnt-compiled-to-use-sse-etc-instructions-but-these-are-availab/44984610#44984610)

    1. [How to compile tensorflow using SSE4.1, SSE4.2, and AVX.](https://github.com/tensorflow/tensorflow/issues/8037)

### GPU using

NVIDIA의 CUDA를 이용한 cuDNN을 사용하기 위해서는 GPU가 compute capabirity를 만족해야 한다. (3.0 이상) -> [Capabiritys site](https://developer.nvidia.com/cuda-gpus)

1. 최신 그래픽카드 드라이버 설치 -> [site](http://www.nvidia.com/Download/index.aspx?lang=kr)

1. CUDA 9.0 설치 -> [site](https://developer.nvidia.com/cuda-90-download-archive?target_os=Windows&target_arch=x86_64&target_version=10&target_type=exenetwork)

    1. Base Installer 다운 및 설치. 설치 옵션 중 샘플 및 기타 나이트 비전 등은 필요 없다.

    1. Path 1 다운 및 설치

    1. Path 2 다운 및 설치

1. cuDNN 설치 -> [site](https://developer.nvidia.com/rdp/form/cudnn-download-survey)

    - NVIDIA Developer Program membership 가입이 필요하다.

    - 자신의 CUDA 버전에 맞는 cuDNN을 다운로드 받아야 한다.

    - 가입 필요없이 다운로드 -> [for CUDA 9.0 link](https://drive.google.com/open?id=1QN_0RM_zDXUsKonr91hdqjdCsJ1my989)

    - 다운로드 받은 파일을 CUDA 설치 폴더에 덮어씌무면 된다. (Overwriting 없음)

        `C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v9.0`

1. Tensorflow GPU 버전으로 업그레이드

    ```powershell
    pip install --upgrade tensorflow-gpu
    ```

    처음 tensorflow를 import하면 gpu 디바이스를 확인하고 등록한다. 이 때 시간이 약간 소요된다.

    ```python
    $ python
    >>> import tensorflow as tf
    ```
    tensorflow에서 세션을 불러오면 gpu를 사용중인지 확인할 수 있는 로그(I)가 출력된다.

    ```python
    tf.Session()
    ```

    아무것도 출력되지 않으면 로그 출력 범위(I, W, E)를 확인해보거나 기계학습을 돌려보고 체감속도가 빨라졌는지 또는 GPU를 사용중인지(작업관리자) 확인해본다..

[top](#index)

-------------------------------------------------------------------

## Building guide

1. Release 된 최신 프로젝트를 다운받는다. -> [Release page](https://github.com/crack-love/KSL/releases)

1. KSL.sln 파일을 실행하여 모든  프로젝트를 빌드한다.

1. 빌드 된 Project_Interface 프로젝트의 실행 파일(.exe)을 실행한다.

1. 실행한 인터페이스 프로그램에서 Execute 버튼을 눌러 C++ / Python 을 실행한다.
    - 왼쪽 버튼은 C++ 프로그램 실행
    - 오른쪽 버튼은 Python 스크립트(do_script) 실행
    - Python 3.5.x 실행파일 위치를 지정해줘야 한다.

[top](#index)
