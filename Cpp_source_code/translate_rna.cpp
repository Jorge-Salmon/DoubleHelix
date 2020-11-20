#include <Python.h>
#include <algorithm>
#include <functional>
#include <unordered_map>
#include <string>
using namespace std;

unordered_map<string,string> RNA_Codons = {
   // 'M' - START, '_' - STOP
    {"GCU", "A"}, {"GCC", "A"}, {"GCA", "A"}, {"GCG", "A"},
    {"UGU", "C"}, {"UGC", "C"},
    {"GAU", "D"}, {"GAC", "D"},
    {"GAA", "E"}, {"GAG", "E"},
    {"UUU", "F"}, {"UUC", "F"},
    {"GGU", "G"}, {"GGC", "G"}, {"GGA", "G"}, {"GGG", "G"},
    {"CAU", "H"}, {"CAC", "H"},
    {"AUA", "I"}, {"AUU", "I"}, {"AUC", "I"},
    {"AAA", "K"}, {"AAG", "K"},
    {"UUA", "L"}, {"UUG", "L"}, {"CUU", "L"}, {"CUC", "L"}, {"CUA", "L"}, {"CUG", "L"},
    {"AUG", "M"},
    {"AAU", "N"}, {"AAC", "N"},
    {"CCU", "P"}, {"CCC", "P"}, {"CCA", "P"}, {"CCG", "P"},
    {"CAA", "Q"}, {"CAG", "Q"},
    {"CGU", "R"}, {"CGC", "R"}, {"CGA", "R"}, {"CGG", "R"}, {"AGA", "R"}, {"AGG", "R"},
    {"UCU", "S"}, {"UCC", "S"}, {"UCA", "S"}, {"UCG", "S"}, {"AGU", "S"}, {"AGC", "S"},
    {"ACU", "T"}, {"ACC", "T"}, {"ACA", "T"}, {"ACG", "T"},
    {"GUU", "V"}, {"GUC", "V"}, {"GUA", "V"}, {"GUG", "V"},
    {"UGG", "W"},
    {"UAU", "Y"}, {"UAC", "Y"},
    {"UAA", "_"}, {"UAG", "_"}, {"UGA", "_"}
};

PyObject* translate_RNA(PyObject* self, PyObject* args) {
  const char *seq;

  if (!PyArg_ParseTuple(args,"s",&seq))
  return NULL;

  // convert char to std::string
  string s = (strlen(seq), seq);
  string temp;
  string proteins;

  for (unsigned int i=0; i<=s.length()-2; i+=3) {
    temp.append(s, i, 3);
    proteins.append(RNA_Codons[temp]);
    temp.erase();
  }

  const char *c = &*proteins.begin();
  return PyUnicode_FromString(c);
};

static PyMethodDef mainMethods[] = {
 {"translate_RNA",translate_RNA,METH_VARARGS,"Calculate the complement of a DNA sequence"},
 {NULL,NULL,0,NULL}
};

static PyModuleDef DoubleHelix_translate_rna = {
 PyModuleDef_HEAD_INIT,
 "DoubleHelix_translate_rna","RNA sequence transcription",
 -1,
 mainMethods
};

PyMODINIT_FUNC PyInit_DoubleHelix_translate_rna(void){
 return PyModule_Create(&DoubleHelix_translate_rna);
};
