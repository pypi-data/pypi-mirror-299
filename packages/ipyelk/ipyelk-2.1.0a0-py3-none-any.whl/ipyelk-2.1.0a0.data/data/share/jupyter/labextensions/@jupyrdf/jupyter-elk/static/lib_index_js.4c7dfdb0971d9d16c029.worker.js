"use strict";
(self["webpackChunk_jupyrdf_jupyter_elk"] = self["webpackChunk_jupyrdf_jupyter_elk"] || []).push([["lib_index_js"],{

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   ELK_CSS: () => (/* reexport safe */ _tokens__WEBPACK_IMPORTED_MODULE_0__.ELK_CSS),
/* harmony export */   ELK_DEBUG: () => (/* reexport safe */ _tokens__WEBPACK_IMPORTED_MODULE_0__.ELK_DEBUG),
/* harmony export */   NAME: () => (/* reexport safe */ _tokens__WEBPACK_IMPORTED_MODULE_0__.NAME),
/* harmony export */   VERSION: () => (/* reexport safe */ _tokens__WEBPACK_IMPORTED_MODULE_0__.VERSION)
/* harmony export */ });
/* harmony import */ var _tokens__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./tokens */ "./lib/tokens.js");
/**
 * # Copyright (c) 2024 ipyelk contributors.
 * Distributed under the terms of the Modified BSD License.
 */



/***/ }),

/***/ "./lib/tokens.js":
/*!***********************!*\
  !*** ./lib/tokens.js ***!
  \***********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   ELK_CSS: () => (/* binding */ ELK_CSS),
/* harmony export */   ELK_DEBUG: () => (/* binding */ ELK_DEBUG),
/* harmony export */   NAME: () => (/* binding */ NAME),
/* harmony export */   VERSION: () => (/* binding */ VERSION)
/* harmony export */ });
/* harmony import */ var _package_json__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../package.json */ "./package.json");
/**
 * # Copyright (c) 2024 ipyelk contributors.
 * Distributed under the terms of the Modified BSD License.
 */

const NAME = _package_json__WEBPACK_IMPORTED_MODULE_0__.name;
const VERSION = _package_json__WEBPACK_IMPORTED_MODULE_0__.version;
const ELK_DEBUG = window.location.hash.indexOf('ELK_DEBUG') > -1;
const ELK_CSS = {
    label: 'elklabel',
    widget_class: 'jp-ElkView',
    sizer_class: 'jp-ElkSizer',
};


/***/ }),

/***/ "./package.json":
/*!**********************!*\
  !*** ./package.json ***!
  \**********************/
/***/ ((module) => {

module.exports = /*#__PURE__*/JSON.parse('{"name":"@jupyrdf/jupyter-elk","version":"2.1.0-alpha0","description":"ElkJS widget for Jupyter","license":"BSD-3-Clause","author":"Dane Freeman","homepage":"https://github.com/jupyrdf/ipyelk","repository":{"type":"git","url":"https://github.com/jupyrdf/ipyelk"},"bugs":{"url":"https://github.com/jupyrdf/ipyelk/issues"},"main":"lib/index.js","files":["COPYRIGHT.md","third-party/**/*","{lib,style}/**/*.{.ts,eot,gif,html,jpg,js,js.map,json,png,svg,woff2,ttf,css}"],"scripts":{"bootstrap":"jlpm --prefer-offline --ignore-optional --ignore-scripts && jlpm clean && jlpm schema && jlpm lint && jlpm build","build":"jlpm build:ts && jlpm build:ext","build:ext":"jupyter labextension build . --debug","build:ts":"tsc -b js","clean":"rimraf ./lib ./src/ipyelk/schema/elkschema.json ./src/ipyelk/_d","lint":"jlpm lint:prettier","lint:prettier":"prettier-package-json --write package.json && prettier --cache --cache-location build/.prettiercache --write --list-different \\"*.{json,yml,md,js}\\" \\"{js,style,lite,src,.github,examples,docs}/**/*.{ts,tsx,js,jsx,css,json,md,yml,yaml}\\"","schema":"jlpm schema:build && jlpm schema:prettier","schema:build":"cd js && ts-json-schema-generator --tsconfig ./tsconfig.json --type AnyElkNode --no-type-check --expose all --path ./elkschema.ts -o ../src/ipyelk/schema/elkschema.json","schema:prettier":"prettier --write src/ipyelk/schema/elkschema.json","watch":"run watch:lib && run watch:ext","watch:ext":"jupyter labextension watch .","watch:lib":"jlpm build:ts --watch --preserveWatchOutput"},"sideEffects":["style/*.css"],"types":"lib/index.d.ts","resolutions":{"verdaccio":"file:./scripts/not-a-package","@types/react":"file:./scripts/not-a-package","typescript":"5.2.2","prettier":"^3.3.0","elkjs":"0.9.3","source-map-loader":"^5.0.0"},"dependencies":{"@jupyter-widgets/base":"^6.0.10","@jupyter-widgets/controls":"^5.0.11","@jupyter-widgets/jupyterlab-manager":"^5.0.13","@jupyterlab/application":"^4.2.5","@jupyterlab/apputils":"^4.3.5","elkjs":"0.9.3","inversify":"~6.0.2","reflect-metadata":"^0.1.13","sprotty":"1.3.0","sprotty-elk":"1.3.0","sprotty-protocol":"^1.3.0"},"devDependencies":{"@jupyterlab/builder":"^4.2.5","@jupyterlab/theme-dark-extension":"4","@jupyterlab/theme-light-extension":"4","@trivago/prettier-plugin-sort-imports":"^4.0.0","@types/lodash":"^4.14.162","circular-dependency-plugin":"^5.2.2","prettier":"^3.3.0","prettier-package-json":"^2.8.0","prettier-plugin-sort-json":"^4.0","raw-loader":"^4.0.2","rimraf":"^6.0.1","source-map-loader":"^5.0.0","ts-json-schema-generator":"^2.3.0","typescript":"5.2.2","yarn-berry-deduplicate":"^6.1.1"},"keywords":["jupyter","jupyterlab","jupyterlab-extension","widgets"],"jupyterlab":{"extension":"lib/plugin","webpackConfig":"./webpack.config.js","outputDir":"./src/_d/share/jupyter/labextensions/@jupyrdf/jupyter-elk","sharedPackages":{"elkjs":{"bundled":true,"singleton":true},"sprotty-elk":{"bundled":true,"singleton":true},"@jupyter-widgets/base":{"bundled":false,"singleton":true},"@jupyter-widgets/controls":{"bundled":false,"singleton":true},"inversify":{"bundled":true,"singleton":true},"sprotty":{"bundled":true,"singleton":true},"sprotty-protocol":{"bundled":true,"singleton":true}}},"prettier":{"singleQuote":true,"proseWrap":"always","printWidth":88,"plugins":["@trivago/prettier-plugin-sort-imports"],"importOrder":["^inversify.*$","^sprotty-protocol.*$","^sprotty.*$","^@lumino/(.*)$","^@jupyterlab/(.*)$","^@jupyter-widgets/(.*)$","^[.]{2}/","^[./]","^!"],"importOrderSeparation":true,"importOrderSortSpecifiers":true,"importOrderParserPlugins":["classProperties","decorators-legacy","jsx","typescript"]},"style":"style/index.css"}');

/***/ })

}]);
//# sourceMappingURL=lib_index_js.4c7dfdb0971d9d16c029.worker.js.map?v=4c7dfdb0971d9d16c029