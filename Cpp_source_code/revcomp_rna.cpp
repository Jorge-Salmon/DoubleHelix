#include <Python.h>
#include <algorithm>
#include <functional>
#include <unordered_map>
#include <string>
using namespace std;

std::function<std::string(std::string)>
maketrans(const std::string& from, const std::string& to) {
  std::unordered_map<char, char> map;
  for (std::string::size_type i = 0; i != std::min(from.size(), to.size()); ++i) {
    map[from[i]] = to[i];
    }
  return [=](std::string s) {
    for (auto& c : s) {
      const auto mapped_c = map.find(c);
      if (mapped_c != map.end()) {
        c = mapped_c->second;
      }
    }
    return s;
  };
};


PyObject* revcomp_rna(PyObject* self, PyObject* args) {

  const char *seq;

  if (!PyArg_ParseTuple(args,"s",&seq))
  return NULL;

  string s = (strlen(seq), seq);
  const auto translate = maketrans("AUCG", "UAGC");
  string translated_s = translate(s);
  reverse(translated_s.begin(), translated_s.end());

  // convert string to const char *
  const char *c = &*translated_s.begin();

  return PyUnicode_FromString(c);
};

static PyMethodDef mainMethods[] = {
 {"revcomp_rna",revcomp_rna,METH_VARARGS,"Calculate the complement of a DNA sequence"},
 {NULL,NULL,0,NULL}
};

static PyModuleDef DoubleHelix_revcomp_rna = {
 PyModuleDef_HEAD_INIT,
 "DoubleHelix_revcomp_rna","DNA reverse complement calculation",
 -1,
 mainMethods
};

PyMODINIT_FUNC PyInit_DoubleHelix_revcomp_rna(void){
 return PyModule_Create(&DoubleHelix_revcomp_rna);
};
