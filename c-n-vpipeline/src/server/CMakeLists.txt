cmake_minimum_required(VERSION 2.8)


include(CodeGenerator)
include_directories(implementation/objects/iorconnectors)

set(HEADER_FILES_CONNECTOR 
	${CMAKE_CURRENT_SOURCE_DIR}/implementation/objects/iorconnectors/base64.h
	${CMAKE_CURRENT_SOURCE_DIR}/implementation/objects/iorconnectors/PipeConnector.hpp
)

set(SOURCE_FILES_CONNECTOR
	${CMAKE_CURRENT_SOURCE_DIR}/implementation/objects/iorconnectors/PipeConnector.cpp
)

generate_code(
  MODELS ${CMAKE_CURRENT_SOURCE_DIR}/interface
  SERVER_STUB_DESTINATION ${CMAKE_CURRENT_SOURCE_DIR}/implementation/objects
  SERVER_IMPL_LIB_EXTRA_LIBRARIES cppzmq
  SERVER_IMPL_LIB_EXTRA_SOURCES ${HEADER_FILES_CONNECTOR}
  SERVER_IMPL_LIB_EXTRA_HEADERS ${SOURCE_FILES_CONNECTOR}
)
