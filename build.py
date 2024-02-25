#!/usr/bin/python3
import argparse
import subprocess
import logging
import os
import datetime
import shutil
import sys

logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)

if os.name == 'nt': _ = "\\"
else: _ = "/"

class __LastBuildTime():
    build_time_file_name : str = "__build_time"
    __LAST_BUILD_TIME = None

    @classmethod
    def time(cls) -> str:
        if cls.__LAST_BUILD_TIME == None:
            cls.__get_last_build_time()

        if not cls.__LAST_BUILD_TIME:
            cls.__LAST_BUILD_TIME = str(datetime.datetime.now())

        return datetime.datetime.strptime(cls.__LAST_BUILD_TIME, "%Y-%m-%d %H:%M:%S.%f")

    @classmethod
    def update(cls):
        cls.__LAST_BUILD_TIME = datetime.datetime.now()
        cls.__set_last_build_time()

    @classmethod
    def __get_last_build_time(cls):
        with open(cls.build_time_file_name, "r+") as file:
            cls.__LAST_BUILD_TIME = file.read()
            file.close()

    @classmethod
    def __set_last_build_time(cls):
        with open(cls.build_time_file_name, "w+") as file:
            file.write(str(cls.__LAST_BUILD_TIME))
            file.close()


def __execute(command : str, dir : str = ".") -> str:
    logging.info(command)
    return subprocess.check_output(command, cwd=dir, shell=True)\
                     .decode("utf-8")

def __modifid(file: str) -> bool:
    return datetime.datetime.fromtimestamp(os.path.getmtime(file)) > __LastBuildTime.time()

def __exists(file: str) -> bool:
    return os.path.exists(file)

def __get_files_recursive(path : str) -> list[str]:
    result = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".cpp"):
                result.append(os.path.join(root, file))
    return result

def __get_files(path: str) -> list[str]:
    result = []
    for file in os.listdir(path):
        if file.endswith(".cpp"):
            result.append(os.path.join(path, file))
    return result


CC = "clang++"
CCFLAGS = "-std=c++20 -stdlib=libc++ -O1 -g -Wall -Wextra -Wpedantic "
CCFLAGS += "-Wno-c99-extensions -Wno-unused-parameter -Wno-vla-extension "
CCFLAGS += "-Wno-c++11-extensions -Wno-gnu-statement-expression "
CCFLAGS += "-Wno-gnu-zero-variadic-macro-arguments -Wno-nested-anon-types "
CCFLAGS += "-Wno-gnu-anonymous-struct "

ROOT_DIR = "."
SRC_DIR = f"{ROOT_DIR}{_}src"
LIBS_DIR = f"{ROOT_DIR}{_}libs"
BUILD_DIR = f"{ROOT_DIR}{_}build"

OBJ_NAME = "main"

GLEW_LIB = "-lGLEW"
GLFW_LIB = "-lglfw"
SPDLOG_LIB = "-lspdlog"

GLEW_PATH = f"{LIBS_DIR}{_}glew"
GLFW_PATH = f"{LIBS_DIR}{_}glfw"
GLM_PATH = f"{LIBS_DIR}{_}glm"
SPDLOG_PATH = f"{LIBS_DIR}{_}spdlog"

CCFLAGS += f"-I{GLEW_PATH}{_}include -I{GLFW_PATH}{_}include -I{GLM_PATH} -I{SPDLOG_PATH}{_}include"
LDFLAFS = f"-L{ROOT_DIR}/bin -L{SPDLOG_PATH}/src"

LDLIBS = f"{GLEW_LIB} {GLFW_LIB} -lX11 -lm -ldl -lpthread -framework OpenGL -Wl,-rpath,./bin"

def init():
    if not os.path.isdir("build"):
        os.mkdir("build")
    if not os.path.isdir("bin"):
        os.mkdir("bin")
        
    print(__execute("cmake -DBUILD_SHARED_LIBS=ON .", dir=f".{_}libs{_}glfw"))
    print(__execute("make", dir=f".{_}libs{_}glfw"))
    
    print(__execute("make", dir=f".{_}libs{_}glew{_}auto"))
    print(__execute("make", dir=f".{_}libs{_}glew"))
    
    # print(__execute("cmake . -DSPDLOG_BUILD_SHARED=ON", dir=f".{_}libs{_}spdlog"))
    # print(__execute("make", dir=f".{_}libs{_}spdlog"))
    
    for el in [f".{_}libs{_}glfw" ,f".{_}libs{_}glew"]:
        for root, directory, files in os.walk(el):
            for name in files:
                if name.endswith(".dylib") or name.endswith(".dll") or name.endswith(".so") or name.endswith(".a"):
                    path = os.path.join(root, name)
                    shutil.move(path, f".{_}bin")

def clear():
    __execute(f"rm -rf {BUILD_DIR}{_}* {OBJ_NAME} {__LastBuildTime.build_time_file_name}")

def all():
    exe_files = [el [2:] for el in __get_files(f"{ROOT_DIR}")]
    src_files = [el[2:] for el in __get_files_recursive(f"{SRC_DIR}")]
    objs_files = [f"{BUILD_DIR[2:]}{_}{el.split(_)[-1].replace('.cpp', '.o')}" for el in src_files]

    src_files += exe_files
    objs_files += [f"{BUILD_DIR[2:]}{_}{el.replace('.cpp', '.o')}" for el in exe_files]

    for idx, el in enumerate(src_files):
        if __modifid(f".{_}{el}") or not __exists(f"./{objs_files[idx]}"):
            __execute(f"{CC} {CCFLAGS} -c {el} -o {objs_files[idx]}")

    for el in exe_files:
        __execute(f"{CC} {CCFLAGS} {LDFLAFS} {LDLIBS} {' '.join(objs_files)} -o {OBJ_NAME}")

if __name__ == "__main__":
    if not os.path.isfile("__build_time"):
        logging.error("File __build_time non trovato")
        sys.exit(0)
    parser = argparse.ArgumentParser()
    parser.add_argument("action", type=str, default="all", nargs="?")
    args = parser.parse_args()
    funs = locals()
    if args.action in funs: funs[args.action]()
    else: logging.error(f"Action '{args.action}' doesn't declared")
    __LastBuildTime.update()

