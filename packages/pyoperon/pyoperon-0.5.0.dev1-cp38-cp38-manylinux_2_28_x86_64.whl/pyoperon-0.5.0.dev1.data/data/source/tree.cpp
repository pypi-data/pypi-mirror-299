// SPDX-License-Identifier: MIT
// SPDX-FileCopyrightText: Copyright 2019-2021 Heal Research

#include "pyoperon/pyoperon.hpp"
#include <operon/core/subtree.hpp>
#include <operon/core/tree.hpp>

void InitTree(nb::module_ &m)
{
    // tree
    nb::class_<Operon::Tree>(m, "Tree")
        // .def(nb::init<std::initializer_list<Operon::Node>>())
        .def(nb::init<Operon::Vector<Operon::Node>>())
        .def(nb::init<Operon::Tree const&>())
        .def("UpdateNodes", &Operon::Tree::UpdateNodes)
        .def("Sort", &Operon::Tree::Sort)
        .def("Hash", &Operon::Tree::Hash)
        .def("Reduce", &Operon::Tree::Reduce)
        .def("SetEnabled", &Operon::Tree::SetEnabled)
        .def("SetCoefficients", [](Operon::Tree& tree, nb::ndarray<Operon::Scalar const> coefficients){
            tree.SetCoefficients(MakeSpan(coefficients));
        }, nb::arg("coefficients"))
        .def("GetCoefficients", &Operon::Tree::GetCoefficients)
        .def_prop_ro("CoefficientsCount", &Operon::Tree::CoefficientsCount)
        .def_prop_ro("Nodes", [](Operon::Tree const& tree) { return tree.Nodes(); } )
        // .def_prop_ro("Nodes", static_cast<Operon::Vector<Operon::Node> const& (Operon::Tree::*)() const&>(&Operon::Tree::Nodes))
        // .def_prop_ro("Nodes", static_cast<Operon::Vector<Operon::Node> const& (Operon::Tree::*)() const&>(&Operon::Tree::Nodes))
        //.def_prop_ro("Nodes", static_cast<Operon::Vector<Operon::Node>&& (Operon::Tree::*)() &&>(&Operon::Tree::Nodes))
        .def_prop_ro("Indices", [](Operon::Tree const& tree, std::size_t i) { return tree.Indices(i); })
        .def_prop_ro("Children", nb::overload_cast<std::size_t>(&Operon::Tree::Children))
        .def_prop_ro("Children", nb::overload_cast<std::size_t>(&Operon::Tree::Children, nb::const_))
        .def_prop_ro("Length", &Operon::Tree::Length, nb::call_guard<nb::gil_scoped_release>())
        .def_prop_ro("VisitationLength", &Operon::Tree::VisitationLength)
        .def_prop_ro("Depth", static_cast<size_t (Operon::Tree::*)() const>(&Operon::Tree::Depth))
        .def_prop_ro("Empty", &Operon::Tree::Empty)
        .def_prop_ro("HashValue", &Operon::Tree::HashValue)
        .def("__getitem__", nb::overload_cast<size_t>(&Operon::Tree::operator[]))
        .def("__getitem__", nb::overload_cast<size_t>(&Operon::Tree::operator[], nb::const_))
        .def("__getstate__",
            [](Operon::Tree const& tree) {
                return std::make_tuple(tree.Nodes());
            })
        .def("__setstate__",
            [](Operon::Tree& tree, std::tuple<std::vector<Operon::Node>> const& t) {
                static_assert(std::tuple_size_v<std::remove_cvref_t<decltype(t)>> == 1, "Operon::Tree: invalid state");
                new (&tree) Operon::Tree(std::get<0>(t));
            }
        );

}
