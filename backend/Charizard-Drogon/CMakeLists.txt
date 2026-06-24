cmake_minimum_required(VERSION 3.5)
project(CharizardDrogonServer CXX)

set(CMAKE_CXX_STANDARD 17)

# Procura a biblioteca do Drogon no sistema
find_package(Drogon REQUIRED)

add_executable(CharizardDrogonServer main.cc)

target_link_libraries(CharizardDrogonServer PRIVATE Drogon::Drogon)
