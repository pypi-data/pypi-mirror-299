"use strict";
(self["webpackChunk_jupyrdf_jupyter_elk"] = self["webpackChunk_jupyrdf_jupyter_elk"] || []).push([["style_index_css"],{

/***/ "./node_modules/css-loader/dist/cjs.js!./style/diagram.css":
/*!*****************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./style/diagram.css ***!
  \*****************************************************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/sourceMaps.js */ "./node_modules/css-loader/dist/runtime/sourceMaps.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/api.js */ "./node_modules/css-loader/dist/runtime/api.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__);
// Imports


var ___CSS_LOADER_EXPORT___ = _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default()((_node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0___default()));
// Module
___CSS_LOADER_EXPORT___.push([module.id, `/**
 * # Copyright (c) 2024 ipyelk contributors.
 * Distributed under the terms of the Modified BSD License.
 */

/*
  CSS for in-DOM or standalone viewing: all selectors should tolerate having
  \`.jp-ElkView\` stripped.
*/
:root {
  --jp-elk-stroke-width: 1;

  --jp-elk-node-fill: var(--jp-layout-color1);
  --jp-elk-node-stroke: var(--jp-border-color0);

  --jp-elk-edge-stroke: var(--jp-border-color0);

  --jp-elk-port-fill: var(--jp-layout-color1);
  --jp-elk-port-stroke: var(--jp-border-color0);

  --jp-elk-label-color: var(--jp-ui-font-color0);
  --jp-elk-label-font: var(--jp-content-font-family);
  --jp-elk-label-font-size: var(--jp-ui-font-size0);

  /* stable states */
  --jp-elk-color-selected: var(--jp-brand-color2);
  --jp-elk-stroke-width-selected: 3;

  /* interactive states */
  --jp-elk-stroke-hover: var(--jp-brand-color3);
  --jp-elk-stroke-width-hover: 2;

  --jp-elk-stroke-hover-selected: var(--jp-warn-color3);

  /* sugar */
  --jp-elk-transition: 0.1s ease-in;
}

/* firefox doesnt apply style correctly with the addition of .jp-ElkView */
symbol.elksymbol {
  overflow: visible;
}

.jp-ElkView .elknode {
  stroke: var(--jp-elk-node-stroke);
  stroke-width: var(--jp-elk-stroke-width);
  fill: var(--jp-elk-node-fill);
}

.jp-ElkView .elkport {
  stroke: var(--jp-elk-port-stroke);
  stroke-width: var(--jp-elk-stroke-width);
  fill: var(--jp-elk-port-fill);
}

.jp-ElkView .elkedge {
  fill: none;
  stroke: var(--jp-elk-edge-stroke);
  stroke-width: var(--jp-elk-stroke-width);
}

.jp-ElkView .elklabel {
  stroke-width: 0;
  stroke: var(--jp-elk-label-color);
  fill: var(--jp-elk-label-color);
  font-family: var(--jp-elk-label-font);
  font-size: var(--jp-elk-label-font-size);
  dominant-baseline: hanging;
}

.jp-ElkView .elkjunction {
  stroke: none;
  fill: var(--jp-elk-edge-stroke);
}

/* stable states */
.jp-ElkView .elknode.selected,
.jp-ElkView .elkport.selected,
.jp-ElkView .elkedge.selected,
.jp-ElkView .elkedge.selected .elkarrow {
  stroke: var(--jp-elk-color-selected);
  stroke-width: var(--jp-elk-stroke-width-selected);
  transition: stroke stroke-width var(--jp-elk-transition);
}

.jp-ElkView .elklabel.selected {
  fill: var(--jp-elk-color-selected);
  transition: fill var(--jp-elk-transition);
}

/* interactive states: elklabel does not have a mouseover selector/ancestor */
.jp-ElkView .elknode.mouseover,
.jp-ElkView .elkport.mouseover,
.jp-ElkView .elkedge.mouseover {
  stroke: var(--jp-elk-stroke-hover);
  stroke-width: var(--jp-elk-stroke-width-hover);
  transition: stroke stroke-width var(--jp-elk-transition);
}

.jp-ElkView .elklabel.mouseover {
  fill: var(--jp-elk-stroke-hover);
  transition: fill stroke var(--jp-elk-transition);
}

.jp-ElkView .elknode.selected.mouseover,
.jp-ElkView .elkport.selected.mouseover,
.jp-ElkView .elkedge.selected.mouseover,
.jp-ElkView .elkedge.selected.mouseover .elkarrow {
  stroke-width: var(--jp-elk-stroke-width-hover);
  stroke: var(--jp-elk-stroke-hover-selected);
  transition: fill stroke var(--jp-elk-transition);
}

.jp-ElkView .elklabel.selected.mouseover {
  fill: var(--jp-elk-stroke-hover-selected);
  transition: fill stroke var(--jp-elk-transition);
}

.elkcontainer.widget {
  overflow: hidden;
}

.elkcontainer.widget .jupyter-widgets {
  transition: transform 0.5s;
}
`, "",{"version":3,"sources":["webpack://./style/diagram.css"],"names":[],"mappings":"AAAA;;;EAGE;;AAEF;;;CAGC;AACD;EACE,wBAAwB;;EAExB,2CAA2C;EAC3C,6CAA6C;;EAE7C,6CAA6C;;EAE7C,2CAA2C;EAC3C,6CAA6C;;EAE7C,8CAA8C;EAC9C,kDAAkD;EAClD,iDAAiD;;EAEjD,kBAAkB;EAClB,+CAA+C;EAC/C,iCAAiC;;EAEjC,uBAAuB;EACvB,6CAA6C;EAC7C,8BAA8B;;EAE9B,qDAAqD;;EAErD,UAAU;EACV,iCAAiC;AACnC;;AAEA,0EAA0E;AAC1E;EACE,iBAAiB;AACnB;;AAEA;EACE,iCAAiC;EACjC,wCAAwC;EACxC,6BAA6B;AAC/B;;AAEA;EACE,iCAAiC;EACjC,wCAAwC;EACxC,6BAA6B;AAC/B;;AAEA;EACE,UAAU;EACV,iCAAiC;EACjC,wCAAwC;AAC1C;;AAEA;EACE,eAAe;EACf,iCAAiC;EACjC,+BAA+B;EAC/B,qCAAqC;EACrC,wCAAwC;EACxC,0BAA0B;AAC5B;;AAEA;EACE,YAAY;EACZ,+BAA+B;AACjC;;AAEA,kBAAkB;AAClB;;;;EAIE,oCAAoC;EACpC,iDAAiD;EACjD,wDAAwD;AAC1D;;AAEA;EACE,kCAAkC;EAClC,yCAAyC;AAC3C;;AAEA,6EAA6E;AAC7E;;;EAGE,kCAAkC;EAClC,8CAA8C;EAC9C,wDAAwD;AAC1D;;AAEA;EACE,gCAAgC;EAChC,gDAAgD;AAClD;;AAEA;;;;EAIE,8CAA8C;EAC9C,2CAA2C;EAC3C,gDAAgD;AAClD;;AAEA;EACE,yCAAyC;EACzC,gDAAgD;AAClD;;AAEA;EACE,gBAAgB;AAClB;;AAEA;EACE,0BAA0B;AAC5B","sourcesContent":["/**\n * # Copyright (c) 2024 ipyelk contributors.\n * Distributed under the terms of the Modified BSD License.\n */\n\n/*\n  CSS for in-DOM or standalone viewing: all selectors should tolerate having\n  `.jp-ElkView` stripped.\n*/\n:root {\n  --jp-elk-stroke-width: 1;\n\n  --jp-elk-node-fill: var(--jp-layout-color1);\n  --jp-elk-node-stroke: var(--jp-border-color0);\n\n  --jp-elk-edge-stroke: var(--jp-border-color0);\n\n  --jp-elk-port-fill: var(--jp-layout-color1);\n  --jp-elk-port-stroke: var(--jp-border-color0);\n\n  --jp-elk-label-color: var(--jp-ui-font-color0);\n  --jp-elk-label-font: var(--jp-content-font-family);\n  --jp-elk-label-font-size: var(--jp-ui-font-size0);\n\n  /* stable states */\n  --jp-elk-color-selected: var(--jp-brand-color2);\n  --jp-elk-stroke-width-selected: 3;\n\n  /* interactive states */\n  --jp-elk-stroke-hover: var(--jp-brand-color3);\n  --jp-elk-stroke-width-hover: 2;\n\n  --jp-elk-stroke-hover-selected: var(--jp-warn-color3);\n\n  /* sugar */\n  --jp-elk-transition: 0.1s ease-in;\n}\n\n/* firefox doesnt apply style correctly with the addition of .jp-ElkView */\nsymbol.elksymbol {\n  overflow: visible;\n}\n\n.jp-ElkView .elknode {\n  stroke: var(--jp-elk-node-stroke);\n  stroke-width: var(--jp-elk-stroke-width);\n  fill: var(--jp-elk-node-fill);\n}\n\n.jp-ElkView .elkport {\n  stroke: var(--jp-elk-port-stroke);\n  stroke-width: var(--jp-elk-stroke-width);\n  fill: var(--jp-elk-port-fill);\n}\n\n.jp-ElkView .elkedge {\n  fill: none;\n  stroke: var(--jp-elk-edge-stroke);\n  stroke-width: var(--jp-elk-stroke-width);\n}\n\n.jp-ElkView .elklabel {\n  stroke-width: 0;\n  stroke: var(--jp-elk-label-color);\n  fill: var(--jp-elk-label-color);\n  font-family: var(--jp-elk-label-font);\n  font-size: var(--jp-elk-label-font-size);\n  dominant-baseline: hanging;\n}\n\n.jp-ElkView .elkjunction {\n  stroke: none;\n  fill: var(--jp-elk-edge-stroke);\n}\n\n/* stable states */\n.jp-ElkView .elknode.selected,\n.jp-ElkView .elkport.selected,\n.jp-ElkView .elkedge.selected,\n.jp-ElkView .elkedge.selected .elkarrow {\n  stroke: var(--jp-elk-color-selected);\n  stroke-width: var(--jp-elk-stroke-width-selected);\n  transition: stroke stroke-width var(--jp-elk-transition);\n}\n\n.jp-ElkView .elklabel.selected {\n  fill: var(--jp-elk-color-selected);\n  transition: fill var(--jp-elk-transition);\n}\n\n/* interactive states: elklabel does not have a mouseover selector/ancestor */\n.jp-ElkView .elknode.mouseover,\n.jp-ElkView .elkport.mouseover,\n.jp-ElkView .elkedge.mouseover {\n  stroke: var(--jp-elk-stroke-hover);\n  stroke-width: var(--jp-elk-stroke-width-hover);\n  transition: stroke stroke-width var(--jp-elk-transition);\n}\n\n.jp-ElkView .elklabel.mouseover {\n  fill: var(--jp-elk-stroke-hover);\n  transition: fill stroke var(--jp-elk-transition);\n}\n\n.jp-ElkView .elknode.selected.mouseover,\n.jp-ElkView .elkport.selected.mouseover,\n.jp-ElkView .elkedge.selected.mouseover,\n.jp-ElkView .elkedge.selected.mouseover .elkarrow {\n  stroke-width: var(--jp-elk-stroke-width-hover);\n  stroke: var(--jp-elk-stroke-hover-selected);\n  transition: fill stroke var(--jp-elk-transition);\n}\n\n.jp-ElkView .elklabel.selected.mouseover {\n  fill: var(--jp-elk-stroke-hover-selected);\n  transition: fill stroke var(--jp-elk-transition);\n}\n\n.elkcontainer.widget {\n  overflow: hidden;\n}\n\n.elkcontainer.widget .jupyter-widgets {\n  transition: transform 0.5s;\n}\n"],"sourceRoot":""}]);
// Exports
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (___CSS_LOADER_EXPORT___);


/***/ }),

/***/ "./node_modules/css-loader/dist/cjs.js!./style/index.css":
/*!***************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./style/index.css ***!
  \***************************************************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/sourceMaps.js */ "./node_modules/css-loader/dist/runtime/sourceMaps.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/api.js */ "./node_modules/css-loader/dist/runtime/api.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _node_modules_css_loader_dist_cjs_js_diagram_css__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! -!../node_modules/css-loader/dist/cjs.js!./diagram.css */ "./node_modules/css-loader/dist/cjs.js!./style/diagram.css");
/* harmony import */ var _node_modules_css_loader_dist_cjs_js_pipe_status_css__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! -!../node_modules/css-loader/dist/cjs.js!./pipe_status.css */ "./node_modules/css-loader/dist/cjs.js!./style/pipe_status.css");
// Imports




var ___CSS_LOADER_EXPORT___ = _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default()((_node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0___default()));
___CSS_LOADER_EXPORT___.i(_node_modules_css_loader_dist_cjs_js_diagram_css__WEBPACK_IMPORTED_MODULE_2__["default"]);
___CSS_LOADER_EXPORT___.i(_node_modules_css_loader_dist_cjs_js_pipe_status_css__WEBPACK_IMPORTED_MODULE_3__["default"]);
// Module
___CSS_LOADER_EXPORT___.push([module.id, `/**
 * # Copyright (c) 2024 ipyelk contributors.
 * Distributed under the terms of the Modified BSD License.
 */

.jp-ElkView,
.jp-ElkView .sprotty {
  height: 100%;
  display: flex;
  flex-direction: column;
  flex: 1;
}

.jp-ElkView .sprotty text {
  user-select: none;
}

/* Root View */
.jp-ElkView .sprotty-root {
  flex: 1;
  display: flex;
}
.jp-ElkView .sprotty > .sprotty-root > svg.sprotty-graph {
  width: 100%;
  height: 100%;
  flex: 1;
}

.jp-ElkView .sprotty > .sprotty-root > div.sprotty-overlay {
  width: 100%;
  height: 100%;
  flex: 1;
  position: absolute;
  top: 0;
  left: 0;
  transform-origin: top left;
  pointer-events: none;
}
.jp-ElkView .sprotty > .sprotty-root > div.sprotty-overlay > div.elkcontainer {
  pointer-events: all;
  position: absolute;
}

/* Toolbar Styling */
.jp-ElkApp .jp-ElkToolbar {
  width: 100%;
  visibility: hidden;
  position: absolute;
  opacity: 0;
  transition: all var(--jp-elk-transition);
  transform: translateY(calc(0px - var(--jp-widgets-inline-height)));
}

.jp-ElkApp:hover .jp-ElkToolbar {
  visibility: visible;
  opacity: 0.25;
  transform: translateY(0);
}

.jp-ElkApp:hover .jp-ElkToolbar:hover {
  opacity: 1;
}

.jp-ElkToolbar .close-btn {
  display: block;
  margin-left: auto;
  width: var(--jp-widgets-inline-height);
  padding: 0;
  background: inherit;
  border: inherit;
  outline: inherit;
}
.jp-ElkToolbar .close-btn:hover {
  box-shadow: inherit;
  color: var(--jp-warn-color0);
}

.jp-ElkSizer {
  visibility: hidden;
  z-index: -9999;
  pointer-events: none;
}
`, "",{"version":3,"sources":["webpack://./style/index.css"],"names":[],"mappings":"AAAA;;;EAGE;;AAKF;;EAEE,YAAY;EACZ,aAAa;EACb,sBAAsB;EACtB,OAAO;AACT;;AAEA;EACE,iBAAiB;AACnB;;AAEA,cAAc;AACd;EACE,OAAO;EACP,aAAa;AACf;AACA;EACE,WAAW;EACX,YAAY;EACZ,OAAO;AACT;;AAEA;EACE,WAAW;EACX,YAAY;EACZ,OAAO;EACP,kBAAkB;EAClB,MAAM;EACN,OAAO;EACP,0BAA0B;EAC1B,oBAAoB;AACtB;AACA;EACE,mBAAmB;EACnB,kBAAkB;AACpB;;AAEA,oBAAoB;AACpB;EACE,WAAW;EACX,kBAAkB;EAClB,kBAAkB;EAClB,UAAU;EACV,wCAAwC;EACxC,kEAAkE;AACpE;;AAEA;EACE,mBAAmB;EACnB,aAAa;EACb,wBAAwB;AAC1B;;AAEA;EACE,UAAU;AACZ;;AAEA;EACE,cAAc;EACd,iBAAiB;EACjB,sCAAsC;EACtC,UAAU;EACV,mBAAmB;EACnB,eAAe;EACf,gBAAgB;AAClB;AACA;EACE,mBAAmB;EACnB,4BAA4B;AAC9B;;AAEA;EACE,kBAAkB;EAClB,cAAc;EACd,oBAAoB;AACtB","sourcesContent":["/**\n * # Copyright (c) 2024 ipyelk contributors.\n * Distributed under the terms of the Modified BSD License.\n */\n\n@import url('./diagram.css');\n@import url('./pipe_status.css');\n\n.jp-ElkView,\n.jp-ElkView .sprotty {\n  height: 100%;\n  display: flex;\n  flex-direction: column;\n  flex: 1;\n}\n\n.jp-ElkView .sprotty text {\n  user-select: none;\n}\n\n/* Root View */\n.jp-ElkView .sprotty-root {\n  flex: 1;\n  display: flex;\n}\n.jp-ElkView .sprotty > .sprotty-root > svg.sprotty-graph {\n  width: 100%;\n  height: 100%;\n  flex: 1;\n}\n\n.jp-ElkView .sprotty > .sprotty-root > div.sprotty-overlay {\n  width: 100%;\n  height: 100%;\n  flex: 1;\n  position: absolute;\n  top: 0;\n  left: 0;\n  transform-origin: top left;\n  pointer-events: none;\n}\n.jp-ElkView .sprotty > .sprotty-root > div.sprotty-overlay > div.elkcontainer {\n  pointer-events: all;\n  position: absolute;\n}\n\n/* Toolbar Styling */\n.jp-ElkApp .jp-ElkToolbar {\n  width: 100%;\n  visibility: hidden;\n  position: absolute;\n  opacity: 0;\n  transition: all var(--jp-elk-transition);\n  transform: translateY(calc(0px - var(--jp-widgets-inline-height)));\n}\n\n.jp-ElkApp:hover .jp-ElkToolbar {\n  visibility: visible;\n  opacity: 0.25;\n  transform: translateY(0);\n}\n\n.jp-ElkApp:hover .jp-ElkToolbar:hover {\n  opacity: 1;\n}\n\n.jp-ElkToolbar .close-btn {\n  display: block;\n  margin-left: auto;\n  width: var(--jp-widgets-inline-height);\n  padding: 0;\n  background: inherit;\n  border: inherit;\n  outline: inherit;\n}\n.jp-ElkToolbar .close-btn:hover {\n  box-shadow: inherit;\n  color: var(--jp-warn-color0);\n}\n\n.jp-ElkSizer {\n  visibility: hidden;\n  z-index: -9999;\n  pointer-events: none;\n}\n"],"sourceRoot":""}]);
// Exports
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (___CSS_LOADER_EXPORT___);


/***/ }),

/***/ "./node_modules/css-loader/dist/cjs.js!./style/pipe_status.css":
/*!*********************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./style/pipe_status.css ***!
  \*********************************************************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/sourceMaps.js */ "./node_modules/css-loader/dist/runtime/sourceMaps.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/api.js */ "./node_modules/css-loader/dist/runtime/api.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__);
// Imports


var ___CSS_LOADER_EXPORT___ = _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default()((_node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0___default()));
// Module
___CSS_LOADER_EXPORT___.push([module.id, `/**
 * # Copyright (c) 2024 ipyelk contributors.
 * Distributed under the terms of the Modified BSD License.
 */

/*
  Styling elk pipe status widget
*/
.elk-pipe span {
  display: inline-block;
  margin-left: var(--jp-widgets-margin);
  margin-right: var(--jp-widgets-margin);
}

.elk-pipe-badge > svg {
  height: var(--jp-widgets-font-size);
}

.elk-pipe-elapsed,
.elk-pipe-status {
  width: 60px;
}

.elk-pipe-name {
  width: 180px;
}

.elk-pipe-disposition-waiting .elk-pipe-badge {
  stroke: var(--jp-info-color3);
  fill: none;
  stroke-width: 2px;
  color: var(--jp-info-color3);
}

.elk-pipe-disposition-waiting,
.elk-pipe-accessor {
  color: var(--jp-border-color1);
}

.elk-pipe-disposition-finished .elk-pipe-badge {
  fill: var(--jp-success-color1);
}

.elk-pipe-disposition-running .elk-pipe-badge {
  fill: var(--jp-info-color1);
}

.elk-pipe-disposition-error .elk-pipe-badge {
  fill: var(--jp-warn-color0);
}

.elk-pipe-disposition-error .elk-pipe-error {
  display: block;
}

.elk-pipe-disposition-error .elk-pipe-error > code {
  background-color: var(--jp-error-color3);
  width: 335px;
  display: inline-block;
}

.widget-button.elk-pipe-toggle-btn,
.elk-pipe-space {
  width: 2em;
  padding: 0px;
  margin: 0px;
  margin-bottom: auto;
  background-color: unset;
  height: var(--jp-code-line-height);
  line-height: var(--jp-code-line-height);
}
.widget-button.elk-pipe-toggle-btn i {
  transition: all 1s;
}
.elk-pipe-toggle-btn.elk-pipe-closed i {
  transform: rotate(-90deg);
}
`, "",{"version":3,"sources":["webpack://./style/pipe_status.css"],"names":[],"mappings":"AAAA;;;EAGE;;AAEF;;CAEC;AACD;EACE,qBAAqB;EACrB,qCAAqC;EACrC,sCAAsC;AACxC;;AAEA;EACE,mCAAmC;AACrC;;AAEA;;EAEE,WAAW;AACb;;AAEA;EACE,YAAY;AACd;;AAEA;EACE,6BAA6B;EAC7B,UAAU;EACV,iBAAiB;EACjB,4BAA4B;AAC9B;;AAEA;;EAEE,8BAA8B;AAChC;;AAEA;EACE,8BAA8B;AAChC;;AAEA;EACE,2BAA2B;AAC7B;;AAEA;EACE,2BAA2B;AAC7B;;AAEA;EACE,cAAc;AAChB;;AAEA;EACE,wCAAwC;EACxC,YAAY;EACZ,qBAAqB;AACvB;;AAEA;;EAEE,UAAU;EACV,YAAY;EACZ,WAAW;EACX,mBAAmB;EACnB,uBAAuB;EACvB,kCAAkC;EAClC,uCAAuC;AACzC;AACA;EACE,kBAAkB;AACpB;AACA;EACE,yBAAyB;AAC3B","sourcesContent":["/**\n * # Copyright (c) 2024 ipyelk contributors.\n * Distributed under the terms of the Modified BSD License.\n */\n\n/*\n  Styling elk pipe status widget\n*/\n.elk-pipe span {\n  display: inline-block;\n  margin-left: var(--jp-widgets-margin);\n  margin-right: var(--jp-widgets-margin);\n}\n\n.elk-pipe-badge > svg {\n  height: var(--jp-widgets-font-size);\n}\n\n.elk-pipe-elapsed,\n.elk-pipe-status {\n  width: 60px;\n}\n\n.elk-pipe-name {\n  width: 180px;\n}\n\n.elk-pipe-disposition-waiting .elk-pipe-badge {\n  stroke: var(--jp-info-color3);\n  fill: none;\n  stroke-width: 2px;\n  color: var(--jp-info-color3);\n}\n\n.elk-pipe-disposition-waiting,\n.elk-pipe-accessor {\n  color: var(--jp-border-color1);\n}\n\n.elk-pipe-disposition-finished .elk-pipe-badge {\n  fill: var(--jp-success-color1);\n}\n\n.elk-pipe-disposition-running .elk-pipe-badge {\n  fill: var(--jp-info-color1);\n}\n\n.elk-pipe-disposition-error .elk-pipe-badge {\n  fill: var(--jp-warn-color0);\n}\n\n.elk-pipe-disposition-error .elk-pipe-error {\n  display: block;\n}\n\n.elk-pipe-disposition-error .elk-pipe-error > code {\n  background-color: var(--jp-error-color3);\n  width: 335px;\n  display: inline-block;\n}\n\n.widget-button.elk-pipe-toggle-btn,\n.elk-pipe-space {\n  width: 2em;\n  padding: 0px;\n  margin: 0px;\n  margin-bottom: auto;\n  background-color: unset;\n  height: var(--jp-code-line-height);\n  line-height: var(--jp-code-line-height);\n}\n.widget-button.elk-pipe-toggle-btn i {\n  transition: all 1s;\n}\n.elk-pipe-toggle-btn.elk-pipe-closed i {\n  transform: rotate(-90deg);\n}\n"],"sourceRoot":""}]);
// Exports
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (___CSS_LOADER_EXPORT___);


/***/ }),

/***/ "./node_modules/css-loader/dist/runtime/api.js":
/*!*****************************************************!*\
  !*** ./node_modules/css-loader/dist/runtime/api.js ***!
  \*****************************************************/
/***/ ((module) => {



/*
  MIT License http://www.opensource.org/licenses/mit-license.php
  Author Tobias Koppers @sokra
*/
module.exports = function (cssWithMappingToString) {
  var list = [];

  // return the list of modules as css string
  list.toString = function toString() {
    return this.map(function (item) {
      var content = "";
      var needLayer = typeof item[5] !== "undefined";
      if (item[4]) {
        content += "@supports (".concat(item[4], ") {");
      }
      if (item[2]) {
        content += "@media ".concat(item[2], " {");
      }
      if (needLayer) {
        content += "@layer".concat(item[5].length > 0 ? " ".concat(item[5]) : "", " {");
      }
      content += cssWithMappingToString(item);
      if (needLayer) {
        content += "}";
      }
      if (item[2]) {
        content += "}";
      }
      if (item[4]) {
        content += "}";
      }
      return content;
    }).join("");
  };

  // import a list of modules into the list
  list.i = function i(modules, media, dedupe, supports, layer) {
    if (typeof modules === "string") {
      modules = [[null, modules, undefined]];
    }
    var alreadyImportedModules = {};
    if (dedupe) {
      for (var k = 0; k < this.length; k++) {
        var id = this[k][0];
        if (id != null) {
          alreadyImportedModules[id] = true;
        }
      }
    }
    for (var _k = 0; _k < modules.length; _k++) {
      var item = [].concat(modules[_k]);
      if (dedupe && alreadyImportedModules[item[0]]) {
        continue;
      }
      if (typeof layer !== "undefined") {
        if (typeof item[5] === "undefined") {
          item[5] = layer;
        } else {
          item[1] = "@layer".concat(item[5].length > 0 ? " ".concat(item[5]) : "", " {").concat(item[1], "}");
          item[5] = layer;
        }
      }
      if (media) {
        if (!item[2]) {
          item[2] = media;
        } else {
          item[1] = "@media ".concat(item[2], " {").concat(item[1], "}");
          item[2] = media;
        }
      }
      if (supports) {
        if (!item[4]) {
          item[4] = "".concat(supports);
        } else {
          item[1] = "@supports (".concat(item[4], ") {").concat(item[1], "}");
          item[4] = supports;
        }
      }
      list.push(item);
    }
  };
  return list;
};

/***/ }),

/***/ "./node_modules/css-loader/dist/runtime/sourceMaps.js":
/*!************************************************************!*\
  !*** ./node_modules/css-loader/dist/runtime/sourceMaps.js ***!
  \************************************************************/
/***/ ((module) => {



module.exports = function (item) {
  var content = item[1];
  var cssMapping = item[3];
  if (!cssMapping) {
    return content;
  }
  if (typeof btoa === "function") {
    var base64 = btoa(unescape(encodeURIComponent(JSON.stringify(cssMapping))));
    var data = "sourceMappingURL=data:application/json;charset=utf-8;base64,".concat(base64);
    var sourceMapping = "/*# ".concat(data, " */");
    return [content].concat([sourceMapping]).join("\n");
  }
  return [content].join("\n");
};

/***/ }),

/***/ "./style/index.css":
/*!*************************!*\
  !*** ./style/index.css ***!
  \*************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/styleDomAPI.js */ "./node_modules/style-loader/dist/runtime/styleDomAPI.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/insertBySelector.js */ "./node_modules/style-loader/dist/runtime/insertBySelector.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js */ "./node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/insertStyleElement.js */ "./node_modules/style-loader/dist/runtime/insertStyleElement.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/styleTagTransform.js */ "./node_modules/style-loader/dist/runtime/styleTagTransform.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _node_modules_css_loader_dist_cjs_js_index_css__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! !!../node_modules/css-loader/dist/cjs.js!./index.css */ "./node_modules/css-loader/dist/cjs.js!./style/index.css");

      
      
      
      
      
      
      
      
      

var options = {};

options.styleTagTransform = (_node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5___default());
options.setAttributes = (_node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3___default());

      options.insert = _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2___default().bind(null, "head");
    
options.domAPI = (_node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1___default());
options.insertStyleElement = (_node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4___default());

var update = _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default()(_node_modules_css_loader_dist_cjs_js_index_css__WEBPACK_IMPORTED_MODULE_6__["default"], options);




       /* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (_node_modules_css_loader_dist_cjs_js_index_css__WEBPACK_IMPORTED_MODULE_6__["default"] && _node_modules_css_loader_dist_cjs_js_index_css__WEBPACK_IMPORTED_MODULE_6__["default"].locals ? _node_modules_css_loader_dist_cjs_js_index_css__WEBPACK_IMPORTED_MODULE_6__["default"].locals : undefined);


/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js":
/*!****************************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js ***!
  \****************************************************************************/
/***/ ((module) => {



var stylesInDOM = [];
function getIndexByIdentifier(identifier) {
  var result = -1;
  for (var i = 0; i < stylesInDOM.length; i++) {
    if (stylesInDOM[i].identifier === identifier) {
      result = i;
      break;
    }
  }
  return result;
}
function modulesToDom(list, options) {
  var idCountMap = {};
  var identifiers = [];
  for (var i = 0; i < list.length; i++) {
    var item = list[i];
    var id = options.base ? item[0] + options.base : item[0];
    var count = idCountMap[id] || 0;
    var identifier = "".concat(id, " ").concat(count);
    idCountMap[id] = count + 1;
    var indexByIdentifier = getIndexByIdentifier(identifier);
    var obj = {
      css: item[1],
      media: item[2],
      sourceMap: item[3],
      supports: item[4],
      layer: item[5]
    };
    if (indexByIdentifier !== -1) {
      stylesInDOM[indexByIdentifier].references++;
      stylesInDOM[indexByIdentifier].updater(obj);
    } else {
      var updater = addElementStyle(obj, options);
      options.byIndex = i;
      stylesInDOM.splice(i, 0, {
        identifier: identifier,
        updater: updater,
        references: 1
      });
    }
    identifiers.push(identifier);
  }
  return identifiers;
}
function addElementStyle(obj, options) {
  var api = options.domAPI(options);
  api.update(obj);
  var updater = function updater(newObj) {
    if (newObj) {
      if (newObj.css === obj.css && newObj.media === obj.media && newObj.sourceMap === obj.sourceMap && newObj.supports === obj.supports && newObj.layer === obj.layer) {
        return;
      }
      api.update(obj = newObj);
    } else {
      api.remove();
    }
  };
  return updater;
}
module.exports = function (list, options) {
  options = options || {};
  list = list || [];
  var lastIdentifiers = modulesToDom(list, options);
  return function update(newList) {
    newList = newList || [];
    for (var i = 0; i < lastIdentifiers.length; i++) {
      var identifier = lastIdentifiers[i];
      var index = getIndexByIdentifier(identifier);
      stylesInDOM[index].references--;
    }
    var newLastIdentifiers = modulesToDom(newList, options);
    for (var _i = 0; _i < lastIdentifiers.length; _i++) {
      var _identifier = lastIdentifiers[_i];
      var _index = getIndexByIdentifier(_identifier);
      if (stylesInDOM[_index].references === 0) {
        stylesInDOM[_index].updater();
        stylesInDOM.splice(_index, 1);
      }
    }
    lastIdentifiers = newLastIdentifiers;
  };
};

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/insertBySelector.js":
/*!********************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/insertBySelector.js ***!
  \********************************************************************/
/***/ ((module) => {



var memo = {};

/* istanbul ignore next  */
function getTarget(target) {
  if (typeof memo[target] === "undefined") {
    var styleTarget = document.querySelector(target);

    // Special case to return head of iframe instead of iframe itself
    if (window.HTMLIFrameElement && styleTarget instanceof window.HTMLIFrameElement) {
      try {
        // This will throw an exception if access to iframe is blocked
        // due to cross-origin restrictions
        styleTarget = styleTarget.contentDocument.head;
      } catch (e) {
        // istanbul ignore next
        styleTarget = null;
      }
    }
    memo[target] = styleTarget;
  }
  return memo[target];
}

/* istanbul ignore next  */
function insertBySelector(insert, style) {
  var target = getTarget(insert);
  if (!target) {
    throw new Error("Couldn't find a style target. This probably means that the value for the 'insert' parameter is invalid.");
  }
  target.appendChild(style);
}
module.exports = insertBySelector;

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/insertStyleElement.js":
/*!**********************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/insertStyleElement.js ***!
  \**********************************************************************/
/***/ ((module) => {



/* istanbul ignore next  */
function insertStyleElement(options) {
  var element = document.createElement("style");
  options.setAttributes(element, options.attributes);
  options.insert(element, options.options);
  return element;
}
module.exports = insertStyleElement;

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js":
/*!**********************************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js ***!
  \**********************************************************************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {



/* istanbul ignore next  */
function setAttributesWithoutAttributes(styleElement) {
  var nonce =  true ? __webpack_require__.nc : 0;
  if (nonce) {
    styleElement.setAttribute("nonce", nonce);
  }
}
module.exports = setAttributesWithoutAttributes;

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/styleDomAPI.js":
/*!***************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/styleDomAPI.js ***!
  \***************************************************************/
/***/ ((module) => {



/* istanbul ignore next  */
function apply(styleElement, options, obj) {
  var css = "";
  if (obj.supports) {
    css += "@supports (".concat(obj.supports, ") {");
  }
  if (obj.media) {
    css += "@media ".concat(obj.media, " {");
  }
  var needLayer = typeof obj.layer !== "undefined";
  if (needLayer) {
    css += "@layer".concat(obj.layer.length > 0 ? " ".concat(obj.layer) : "", " {");
  }
  css += obj.css;
  if (needLayer) {
    css += "}";
  }
  if (obj.media) {
    css += "}";
  }
  if (obj.supports) {
    css += "}";
  }
  var sourceMap = obj.sourceMap;
  if (sourceMap && typeof btoa !== "undefined") {
    css += "\n/*# sourceMappingURL=data:application/json;base64,".concat(btoa(unescape(encodeURIComponent(JSON.stringify(sourceMap)))), " */");
  }

  // For old IE
  /* istanbul ignore if  */
  options.styleTagTransform(css, styleElement, options.options);
}
function removeStyleElement(styleElement) {
  // istanbul ignore if
  if (styleElement.parentNode === null) {
    return false;
  }
  styleElement.parentNode.removeChild(styleElement);
}

/* istanbul ignore next  */
function domAPI(options) {
  if (typeof document === "undefined") {
    return {
      update: function update() {},
      remove: function remove() {}
    };
  }
  var styleElement = options.insertStyleElement(options);
  return {
    update: function update(obj) {
      apply(styleElement, options, obj);
    },
    remove: function remove() {
      removeStyleElement(styleElement);
    }
  };
}
module.exports = domAPI;

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/styleTagTransform.js":
/*!*********************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/styleTagTransform.js ***!
  \*********************************************************************/
/***/ ((module) => {



/* istanbul ignore next  */
function styleTagTransform(css, styleElement) {
  if (styleElement.styleSheet) {
    styleElement.styleSheet.cssText = css;
  } else {
    while (styleElement.firstChild) {
      styleElement.removeChild(styleElement.firstChild);
    }
    styleElement.appendChild(document.createTextNode(css));
  }
}
module.exports = styleTagTransform;

/***/ })

}]);
//# sourceMappingURL=style_index_css.07eb2d7c46f10fb2e0da.js.map?v=07eb2d7c46f10fb2e0da