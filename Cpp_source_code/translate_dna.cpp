#include <Python.h>
#include <algorithm>
#include <functional>
#include <unordered_map>
#include <string>
using namespace std;

unordered_map<string,string> DNA_Codons = {
  // 'M' - START, '_' - STOP
  {"GCT", "A"}, {"GCC", "A"}, {"GCA", "A"}, {"GCG", "A"},
  {"TGT", "C"}, {"TGC", "C"},
  {"GAT", "D"}, {"GAC", "D"},
  {"GAA", "E"}, {"GAG", "E"},
  {"TTT", "F"}, {"TTC", "F"},
  {"GGT", "G"}, {"GGC", "G"}, {"GGA", "G"}, {"GGG", "G"},
  {"CAT", "H"}, {"CAC", "H"},
  {"ATA", "I"}, {"ATT", "I"}, {"ATC", "I"},
  {"AAA", "K"}, {"AAG", "K"},
  {"TTA", "L"}, {"TTG", "L"}, {"CTT", "L"}, {"CTC", "L"}, {"CTA", "L"}, {"CTG", "L"},
  {"ATG", "M"},
  {"AAT", "N"}, {"AAC", "N"},
  {"CCT", "P"}, {"CCC", "P"}, {"CCA", "P"}, {"CCG", "P"},
  {"CAA", "Q"}, {"CAG", "Q"},
  {"CGT", "R"}, {"CGC", "R"}, {"CGA", "R"}, {"CGG", "R"}, {"AGA", "R"}, {"AGG", "R"},
  {"TCT", "S"}, {"TCC", "S"}, {"TCA", "S"}, {"TCG", "S"}, {"AGT", "S"}, {"AGC", "S"},
  {"ACT", "T"}, {"ACC", "T"}, {"ACA", "T"}, {"ACG", "T"},
  {"GTT", "V"}, {"GTC", "V"}, {"GTA", "V"}, {"GTG", "V"},
  {"TGG", "W"},
  {"TAT", "Y"}, {"TAC", "Y"},
  {"TAA", "_"}, {"TAG", "_"}, {"TGA", "_"}
};

PyObject* translate_DNA(PyObject* self, PyObject* args) {
  const char *seq;

  if (!PyArg_ParseTuple(args,"s",&seq))
  return NULL;

  // convert char to std::string
  string s = (strlen(seq), seq);
  string temp;
  string proteins;

  for (unsigned int i=0; i<=s.length()-2; i+=3) {
    temp.append(s, i, 3);
    proteins.append(DNA_Codons[temp]);
    temp.erase();
  }

  const char *c = &*proteins.begin();
  return PyUnicode_FromString(c);
};

static PyMethodDef mainMethods[] = {
 {"translate_DNA",translate_DNA,METH_VARARGS,"Calculate the complement of a DNA sequence"},
 {NULL,NULL,0,NULL}
};

static PyModuleDef DoubleHelix_translate_dna = {
 PyModuleDef_HEAD_INIT,
 "DoubleHelix_translate_dna","DNA sequence transcription",
 -1,
 mainMethods
};

PyMODINIT_FUNC PyInit_DoubleHelix_translate_dna(void){
 return PyModule_Create(&DoubleHelix_translate_dna);
};
