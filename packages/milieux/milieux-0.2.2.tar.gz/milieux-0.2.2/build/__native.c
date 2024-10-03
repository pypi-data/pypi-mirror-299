#include "init.c"
#include "getargs.c"
#include "getargsfast.c"
#include "int_ops.c"
#include "float_ops.c"
#include "str_ops.c"
#include "bytes_ops.c"
#include "list_ops.c"
#include "dict_ops.c"
#include "set_ops.c"
#include "tuple_ops.c"
#include "exc_ops.c"
#include "misc_ops.c"
#include "generic_ops.c"
#include "__native.h"
#include "__native_internal.h"
static PyMethodDef module_methods[] = {
    {"mysum", (PyCFunction)CPyPy_mysum, METH_FASTCALL | METH_KEYWORDS, NULL /* docstring */},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef module = {
    PyModuleDef_HEAD_INIT,
    "tmp",
    NULL, /* docstring */
    -1,       /* size of per-interpreter state of the module,
                 or -1 if the module keeps state in global variables. */
    module_methods
};

PyMODINIT_FUNC PyInit_tmp(void)
{
    PyObject* modname = NULL;
    if (CPyModule_tmp_internal) {
        Py_INCREF(CPyModule_tmp_internal);
        return CPyModule_tmp_internal;
    }
    CPyModule_tmp_internal = PyModule_Create(&module);
    if (unlikely(CPyModule_tmp_internal == NULL))
        goto fail;
    modname = PyObject_GetAttrString((PyObject *)CPyModule_tmp_internal, "__name__");
    CPyStatic_globals = PyModule_GetDict(CPyModule_tmp_internal);
    if (unlikely(CPyStatic_globals == NULL))
        goto fail;
    if (CPyGlobalsInit() < 0)
        goto fail;
    char result = CPyDef___top_level__();
    if (result == 2)
        goto fail;
    Py_DECREF(modname);
    return CPyModule_tmp_internal;
    fail:
    Py_CLEAR(CPyModule_tmp_internal);
    Py_CLEAR(modname);
    return NULL;
}

CPyTagged CPyDef_mysum(CPyTagged cpy_r_n) {
    CPyTagged cpy_r_x;
    CPyTagged cpy_r_r0;
    CPyTagged cpy_r_i;
    int64_t cpy_r_r1;
    char cpy_r_r2;
    int64_t cpy_r_r3;
    char cpy_r_r4;
    char cpy_r_r5;
    char cpy_r_r6;
    CPyTagged cpy_r_r7;
    CPyTagged cpy_r_r8;
    cpy_r_x = 0;
    cpy_r_r0 = 0;
    CPyTagged_INCREF(cpy_r_r0);
    cpy_r_i = cpy_r_r0;
CPyL1: ;
    cpy_r_r1 = cpy_r_r0 & 1;
    cpy_r_r2 = cpy_r_r1 != 0;
    if (cpy_r_r2) goto CPyL3;
    cpy_r_r3 = cpy_r_n & 1;
    cpy_r_r4 = cpy_r_r3 != 0;
    if (!cpy_r_r4) goto CPyL4;
CPyL3: ;
    cpy_r_r5 = CPyTagged_IsLt_(cpy_r_r0, cpy_r_n);
    if (cpy_r_r5) {
        goto CPyL5;
    } else
        goto CPyL8;
CPyL4: ;
    cpy_r_r6 = (Py_ssize_t)cpy_r_r0 < (Py_ssize_t)cpy_r_n;
    if (!cpy_r_r6) goto CPyL8;
CPyL5: ;
    cpy_r_r7 = CPyTagged_Add(cpy_r_x, cpy_r_i);
    CPyTagged_DECREF(cpy_r_x);
    CPyTagged_DECREF(cpy_r_i);
    cpy_r_x = cpy_r_r7;
    cpy_r_r8 = CPyTagged_Add(cpy_r_r0, 2);
    CPyTagged_DECREF(cpy_r_r0);
    CPyTagged_INCREF(cpy_r_r8);
    cpy_r_r0 = cpy_r_r8;
    cpy_r_i = cpy_r_r8;
    goto CPyL1;
CPyL7: ;
    return cpy_r_x;
CPyL8: ;
    CPyTagged_DECREF(cpy_r_r0);
    CPyTagged_DECREF(cpy_r_i);
    goto CPyL7;
}

PyObject *CPyPy_mysum(PyObject *self, PyObject *const *args, size_t nargs, PyObject *kwnames) {
    static const char * const kwlist[] = {"n", 0};
    static CPyArg_Parser parser = {"O:mysum", kwlist, 0};
    PyObject *obj_n;
    if (!CPyArg_ParseStackAndKeywordsOneArg(args, nargs, kwnames, &parser, &obj_n)) {
        return NULL;
    }
    CPyTagged arg_n;
    if (likely(PyLong_Check(obj_n)))
        arg_n = CPyTagged_BorrowFromObject(obj_n);
    else {
        CPy_TypeError("int", obj_n); goto fail;
    }
    CPyTagged retval = CPyDef_mysum(arg_n);
    if (retval == CPY_INT_TAG) {
        return NULL;
    }
    PyObject *retbox = CPyTagged_StealAsObject(retval);
    return retbox;
fail: ;
    CPy_AddTraceback("tmp.py", "mysum", 1, CPyStatic_globals);
    return NULL;
}

char CPyDef___top_level__(void) {
    PyObject *cpy_r_r0;
    PyObject *cpy_r_r1;
    char cpy_r_r2;
    PyObject *cpy_r_r3;
    PyObject *cpy_r_r4;
    char cpy_r_r5;
    cpy_r_r0 = CPyModule_builtins;
    cpy_r_r1 = (PyObject *)&_Py_NoneStruct;
    cpy_r_r2 = cpy_r_r0 != cpy_r_r1;
    if (cpy_r_r2) goto CPyL3;
    cpy_r_r3 = CPyStatics[3]; /* 'builtins' */
    cpy_r_r4 = PyImport_Import(cpy_r_r3);
    if (unlikely(cpy_r_r4 == NULL)) {
        CPy_AddTraceback("tmp.py", "<module>", -1, CPyStatic_globals);
        goto CPyL4;
    }
    CPyModule_builtins = cpy_r_r4;
    CPy_INCREF(CPyModule_builtins);
    CPy_DECREF(cpy_r_r4);
CPyL3: ;
    return 1;
CPyL4: ;
    cpy_r_r5 = 2;
    return cpy_r_r5;
}

int CPyGlobalsInit(void)
{
    static int is_initialized = 0;
    if (is_initialized) return 0;
    
    CPy_Init();
    CPyModule_tmp = Py_None;
    CPyModule_builtins = Py_None;
    if (CPyStatics_Initialize(CPyStatics, CPyLit_Str, CPyLit_Bytes, CPyLit_Int, CPyLit_Float, CPyLit_Complex, CPyLit_Tuple, CPyLit_FrozenSet) < 0) {
        return -1;
    }
    is_initialized = 1;
    return 0;
}

PyObject *CPyStatics[4];
const char * const CPyLit_Str[] = {
    "\001\bbuiltins",
    "",
};
const char * const CPyLit_Bytes[] = {
    "",
};
const char * const CPyLit_Int[] = {
    "",
};
const double CPyLit_Float[] = {0};
const double CPyLit_Complex[] = {0};
const int CPyLit_Tuple[] = {0};
const int CPyLit_FrozenSet[] = {0};
CPyModule *CPyModule_tmp_internal = NULL;
CPyModule *CPyModule_tmp;
PyObject *CPyStatic_globals;
CPyModule *CPyModule_builtins;
CPyTagged CPyDef_mysum(CPyTagged cpy_r_n);
PyObject *CPyPy_mysum(PyObject *self, PyObject *const *args, size_t nargs, PyObject *kwnames);
char CPyDef___top_level__(void);
