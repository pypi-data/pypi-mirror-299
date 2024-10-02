"use strict";
(self["webpackChunk_jupyrdf_jupyter_elk"] = self["webpackChunk_jupyrdf_jupyter_elk"] || []).push([["lib_patches_js"],{

/***/ "./lib/patches.js":
/*!************************!*\
  !*** ./lib/patches.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   patchReflectMetadata: () => (/* binding */ patchReflectMetadata)
/* harmony export */ });
/* harmony import */ var _tokens__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./tokens */ "./lib/tokens.js");
/**
 * # Copyright (c) 2024 ipyelk contributors.
 * Distributed under the terms of the Modified BSD License.
 */

const KEYSTODELETE = ['defineMetadata', 'getOwnMetadata', 'metadata'];
/**
 * Address issue between reflect-metadata and fast-foundation di
 */
async function patchReflectMetadata() {
    if (Reflect.hasOwnMetadata != null) {
        console.info(`${_tokens__WEBPACK_IMPORTED_MODULE_0__.NAME}: skipping patch of Reflect.metadata`);
        return;
    }
    if (Reflect.metadata) {
        console.warn(`${_tokens__WEBPACK_IMPORTED_MODULE_0__.NAME}: patching broken fast-foundation Reflect.metadata shim`);
    }
    for (const key of KEYSTODELETE) {
        delete Reflect[key];
    }
    await __webpack_require__.e(/*! import() */ "webpack_sharing_consume_default_reflect-metadata_reflect-metadata").then(__webpack_require__.t.bind(__webpack_require__, /*! reflect-metadata */ "webpack/sharing/consume/default/reflect-metadata/reflect-metadata?ea26", 23));
}


/***/ })

}]);
//# sourceMappingURL=lib_patches_js.ce4418755bbba9c4d4b3.js.map?v=ce4418755bbba9c4d4b3