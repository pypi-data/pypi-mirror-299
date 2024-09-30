// Boost.Geometry

// Copyright (c) 2019-2020, Oracle and/or its affiliates.

// Contributed and/or modified by Adam Wulkiewicz, on behalf of Oracle

// Licensed under the Boost Software License version 1.0.
// http://www.boost.org/users/license.html

#ifndef BOOST_GEOMETRY_EXTENSIONS_STRATEGIES_IO_HPP
#define BOOST_GEOMETRY_EXTENSIONS_STRATEGIES_IO_HPP


#include <boost/geometry/core/static_assert.hpp>


namespace boost { namespace geometry
{

namespace strategy { namespace io
{

namespace services
{

template <typename CSTag>
struct default_strategy
{
    BOOST_GEOMETRY_STATIC_ASSERT_FALSE(
        "Not implemented for this coordinate system.",
        CSTag);
};

} // namespace services

}} // namespace strategy::io

}} // namespace boost::geometry

#endif // BOOST_GEOMETRY_EXTENSIONS_STRATEGIES_IO_HPP
