# ---- Developer mode ----

# Developer mode enables targets and code paths in the CMake scripts that are
# only relevant for the developer(s) of pyoperon
# Targets necessary to build the project must be provided unconditionally, so
# consumers can trivially build and package the project
if(PROJECT_IS_TOP_LEVEL)
  option(pyoperon_DEVELOPER_MODE "Enable developer mode" OFF)
  option(BUILD_SHARED_LIBS "Build shared libs." ON)

  set(CMAKE_EXPORT_COMPILE_COMMANDS ON CACHE INTERNAL "")
  if(CMAKE_EXPORT_COMPILE_COMMANDS)
      set(CMAKE_CXX_STANDARD_INCLUDE_DIRECTORIES ${CMAKE_CXX_IMPLICIT_INCLUDE_DIRECTORIES})
  endif()
endif()

# ---- Suppress C4251 on Windows ----

# Please see include/pyoperon/pyoperon.hpp for more details
set(pragma_suppress_c4251 "#define PYOPERON_SUPPRESS_C4251")
if(MSVC)
  string(APPEND pragma_suppress_c4251 [[ _Pragma("warning(suppress:4251)")]])
endif()


# ---- Warning guard ----

# target_include_directories with the SYSTEM modifier will request the compiler
# to omit warnings from the provided paths, if the compiler supports that
# This is to provide a user experience similar to find_package when
# add_subdirectory or FetchContent is used to consume this project
set(pyoperon_warning_guard "")
if(NOT PROJECT_IS_TOP_LEVEL)
  option(
      pyoperon_INCLUDES_WITH_SYSTEM
      "Use SYSTEM modifier for pyoperon's includes, disabling warnings"
      ON
  )
  mark_as_advanced(pyoperon_INCLUDES_WITH_SYSTEM)
  if(pyoperon_INCLUDES_WITH_SYSTEM)
    set(pyoperon_warning_guard SYSTEM)
  endif()
endif()
