#include <Python.h>
#include <algorithm>
#include <functional>
#include <unordered_map>
#include <string>
using namespace std;

PyObject* transcript_DNA(PyObject* self, PyObject* args) {
  const char *seq;

  if (!PyArg_ParseTuple(args,"s",&seq))
  return NULL;

  string seq_str = (1, seq);
  replace(seq_str.begin(), seq_str.end(), 'T', 'U');
  const char *c = &*seq_str.begin();

  return PyUnicode_FromString(c);
};

static PyMethodDef mainMethods[] = {
 {"transcript_DNA",transcript_DNA,METH_VARARGS,"Calculate the complement of a DNA sequence"},
 {NULL,NULL,0,NULL}
};

static PyModuleDef DoubleHelix_transcript = {
 PyModuleDef_HEAD_INIT,
 "DoubleHelix_transcript","DNA sequence transcription",
 -1,
 mainMethods
};

PyMODINIT_FUNC PyInit_DoubleHelix_transcript(void){
 return PyModule_Create(&DoubleHelix_transcript);
};
