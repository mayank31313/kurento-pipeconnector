# - Try to find KMSCNVPIPELINE library

#=============================================================================
# Copyright 2014 Kurento
#
#=============================================================================

set(PACKAGE_VERSION "0.0.1~4.gf7b2d8d")
set(KMSCNVPIPELINE_VERSION ${PACKAGE_VERSION})

message (STATUS "Looking for KMSCNVPIPELINE: 0.0.1~4.gf7b2d8d")

include (GenericFind)

generic_find (
  REQUIRED
  LIBNAME KMSCORE
  VERSION ^6.0.0
)

generic_find (
  REQUIRED
  LIBNAME KMSELEMENTS
  VERSION ^6.0.0
)

generic_find (
  REQUIRED
  LIBNAME KMSFILTERS
  VERSION ^6.0.0
)

set (REQUIRED_VARS
  KMSCNVPIPELINE_VERSION
  KMSCNVPIPELINE_INCLUDE_DIRS
  KMSCNVPIPELINE_LIBRARY
  KMSCNVPIPELINE_LIBRARIES
)

set (KMSCNVPIPELINE_BINARY_DIR_PREFIX "build" CACHE PATH "Path prefix used to look for binary files")
set (KMSCNVPIPELINE_SOURCE_DIR_PREFIX "" CACHE PATH "Path prefix used to look for source files")

set(KMSCNVPIPELINE_INCLUDE_DIRS
  ${KMSCORE_INCLUDE_DIRS}
  ${KMSELEMENTS_INCLUDE_DIRS}
  ${KMSFILTERS_INCLUDE_DIRS}
)

if (NOT "CNVpipeline.hpp CNVpipelineInternal.hpp" STREQUAL " ")
  if (TARGET kmscnvpipelineinterface)
    set (KMSCNVPIPELINE_INTERFACE_INCLUDE_DIR "${KMSCNVPIPELINE_BINARY_DIR_PREFIX}/src/server/interface/generated-cpp")
  else ()
    find_path(KMSCNVPIPELINE_INTERFACE_INCLUDE_DIR
      NAMES
        CNVpipeline.hpp
        CNVpipelineInternal.hpp
      PATH_SUFFIXES
        ${KMSCNVPIPELINE_BINARY_DIR_PREFIX}/src/server/interface/generated-cpp
        kurento/modules/cnvpipeline
    )
  endif ()

  list (APPEND KMSCNVPIPELINE_INCLUDE_DIRS ${KMSCNVPIPELINE_INTERFACE_INCLUDE_DIR})
  list (APPEND REQUIRED_VARS KMSCNVPIPELINE_INTERFACE_INCLUDE_DIR)
endif ()

if (NOT "CNVpipelineImplFactory.hpp" STREQUAL "")
  if (TARGET kmscnvpipelineimpl)
    set (KMSCNVPIPELINE_IMPLEMENTATION_INTERNAL_INCLUDE_DIR "${KMSCNVPIPELINE_BINARY_DIR_PREFIX}/src/server/implementation/generated-cpp")
  else ()
    find_path(KMSCNVPIPELINE_IMPLEMENTATION_INTERNAL_INCLUDE_DIR
      NAMES
        CNVpipelineImplFactory.hpp
      PATH_SUFFIXES
        ${KMSCNVPIPELINE_BINARY_DIR_PREFIX}/src/server/implementation/generated-cpp
        kurento/modules/cnvpipeline
    )
  endif ()

  list (APPEND KMSCNVPIPELINE_INCLUDE_DIRS ${KMSCNVPIPELINE_IMPLEMENTATION_INTERNAL_INCLUDE_DIR})
  list (APPEND REQUIRED_VARS KMSCNVPIPELINE_IMPLEMENTATION_INTERNAL_INCLUDE_DIR)
endif ()

if (NOT "CNVpipelineImpl.hpp CNVpipelineOpenCVImpl.hpp" STREQUAL "")
  if (TARGET kmscnvpipelineimpl)
    set (KMSCNVPIPELINE_IMPLEMENTATION_GENERATED_INCLUDE_DIR "${KMSCNVPIPELINE_SOURCE_DIR_PREFIX}/src/server/implementation/objects")
  else ()
    find_path(KMSCNVPIPELINE_IMPLEMENTATION_GENERATED_INCLUDE_DIR
      NAMES
        CNVpipelineImpl.hpp CNVpipelineOpenCVImpl.hpp
      PATH_SUFFIXES
        src/server/implementation/objects
        kurento/modules/cnvpipeline
    )
  endif ()

  list (APPEND KMSCNVPIPELINE_INCLUDE_DIRS ${KMSCNVPIPELINE_IMPLEMENTATION_GENERATED_INCLUDE_DIR})
  list (APPEND REQUIRED_VARS KMSCNVPIPELINE_IMPLEMENTATION_GENERATED_INCLUDE_DIR)
endif()

if (NOT "PipeConnector.cpp" STREQUAL "")
  if (TARGET kmscnvpipelineimpl)
    set (KMSCNVPIPELINE_IMPLEMENTATION_EXTRA_INCLUDE_DIR "${KMSCNVPIPELINE_SOURCE_DIR_PREFIX}/src/server/")
  else ()
    find_path(KMSCNVPIPELINE_IMPLEMENTATION_EXTRA_INCLUDE_DIR
      NAMES
        PipeConnector.cpp
      PATH_SUFFIXES
        src/server/
        kurento/modules/cnvpipeline
    )
  endif ()

  list (APPEND KMSCNVPIPELINE_INCLUDE_DIRS ${KMSCNVPIPELINE_IMPLEMENTATION_EXTRA_INCLUDE_DIR})
  list (APPEND REQUIRED_VARS KMSCNVPIPELINE_IMPLEMENTATION_EXTRA_INCLUDE_DIR)
endif ()

if (NOT "" STREQUAL "")
  if (TARGET kmscnvpipelineinterface)
    set (KMSCNVPIPELINE_INTERFACE_EXTRA_INCLUDE_DIR "${KMSCNVPIPELINE_SOURCE_DIR_PREFIX}/")
  else ()
    find_path(KMSCNVPIPELINE_INTERFACE_EXTRA_INCLUDE_DIR
      NAMES
        
      PATH_SUFFIXES
        
        kurento/modules/cnvpipeline
    )
  endif()

  list (APPEND KMSCNVPIPELINE_INCLUDE_DIRS ${KMSCNVPIPELINE_INTERFACE_EXTRA_INCLUDE_DIR})
  list (APPEND REQUIRED_VARS KMSCNVPIPELINE_INTERFACE_EXTRA_INCLUDE_DIR)
endif ()

if (TARGET kmscnvpipelineimpl)
  set (KMSCNVPIPELINE_LIBRARY kmscnvpipelineimpl)
else ()
  find_library (KMSCNVPIPELINE_LIBRARY
    NAMES
      kmscnvpipelineimpl
    PATH_SUFFIXES
      ${KMSCNVPIPELINE_BINARY_DIR_PREFIX}/src/server
  )
endif()

set (REQUIRED_LIBS "")
foreach (LIB ${REQUIRED_LIBS})
  string(FIND ${LIB} " " POS)

  if (${POS} GREATER 0)
    string(REPLACE " " ";" REQUIRED_LIB_LIST ${LIB})
    include (CMakeParseArguments)
    cmake_parse_arguments("PARAM" "" "LIBNAME" "" ${REQUIRED_LIB_LIST})

    if (DEFINED PARAM_LIBNAME)
      generic_find (${REQUIRED_LIB_LIST} REQUIRED)
      set (LIB_NAME ${PARAM_LIBNAME})
    else()
      string (SUBSTRING ${LIB} 0 ${POS} LIB_NAME)
      string (SUBSTRING ${LIB} ${POS} -1 LIB_VERSION)
      string (STRIP ${LIB_NAME} LIB_NAME)
      string (STRIP ${LIB_VERSION} LIB_VERSION)
      generic_find (LIBNAME ${LIB_NAME} REQUIRED VERSION "${LIB_VERSION}")
    endif()
  else ()
    string (STRIP ${LIB} LIB_NAME)
    generic_find (LIBNAME ${LIB_NAME} REQUIRED)
  endif ()
  list (APPEND REQUIRED_LIBRARIES ${${LIB_NAME}_LIBRARIES})
  list (APPEND KMSCNVPIPELINE_INCLUDE_DIRS ${${LIB_NAME}_INCLUDE_DIRS})

endforeach()

set(KMSCNVPIPELINE_INCLUDE_DIRS
  ${KMSCNVPIPELINE_INCLUDE_DIRS}
  CACHE INTERNAL "Include directories for KMSCNVPIPELINE library" FORCE
)

set (KMSCNVPIPELINE_LIBRARIES
  ${KMSCNVPIPELINE_LIBRARY}
  ${KMSCORE_LIBRARIES}
  ${KMSELEMENTS_LIBRARIES}
  ${KMSFILTERS_LIBRARIES}
  ${REQUIRED_LIBRARIES}
  CACHE INTERNAL "Libraries for KMSCNVPIPELINE" FORCE
)

include (FindPackageHandleStandardArgs)

find_package_handle_standard_args(KMSCNVPIPELINE
  FOUND_VAR
    KMSCNVPIPELINE_FOUND
  REQUIRED_VARS
    ${REQUIRED_VARS}
  VERSION_VAR
    KMSCNVPIPELINE_VERSION
)

mark_as_advanced(
  KMSCNVPIPELINE_FOUND
  KMSCNVPIPELINE_VERSION
  KMSCNVPIPELINE_INTERFACE_INCLUDE_DIR
  KMSCNVPIPELINE_IMPLEMENTATION_INTERNAL_INCLUDE_DIR
  KMSCNVPIPELINE_IMPLEMENTATION_GENERATED_INCLUDE_DIR
  KMSCNVPIPELINE_IMPLEMENTATION_EXTRA_INCLUDE_DIR
  KMSCNVPIPELINE_INTERFACE_EXTRA_INCLUDE_DIR
  KMSCNVPIPELINE_INCLUDE_DIRS
  KMSCNVPIPELINE_LIBRARY
  KMSCNVPIPELINE_LIBRARIES
)
