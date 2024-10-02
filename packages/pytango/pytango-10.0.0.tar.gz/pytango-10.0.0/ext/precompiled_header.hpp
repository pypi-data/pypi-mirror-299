/******************************************************************************
  This file is part of PyTango (http://pytango.rtfd.io)

  Copyright 2006-2012 CELLS / ALBA Synchrotron, Bellaterra, Spain
  Copyright 2013-2014 European Synchrotron Radiation Facility, Grenoble, France

  Distributed under the terms of the GNU Lesser General Public License,
  either version 3 of the License, or (at your option) any later version.
  See LICENSE.txt for more info.
******************************************************************************/

// These files are really basic, used everywere within the project
// but they take a while (seconds!) to process.
// We don't want to waste those seconds for each cpp file, so we
// use this precompiled header.

#define BOOST_BIND_GLOBAL_PLACEHOLDERS
#define BOOST_ALLOW_DEPRECATED_HEADERS

#include <boost/python.hpp>
#include <boost/version.hpp>
#include <boost/python/copy_const_reference.hpp>
#include <boost/python/copy_non_const_reference.hpp>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>
#include <boost/python/return_value_policy.hpp>
#include <boost/python/handle.hpp>
#include <boost/mpl/if.hpp>
#include <cassert>
#include <iostream>
#include <string>
#include <sstream>
#include <memory>

namespace bopy = boost::python;

// #include <tango/tango.h>
