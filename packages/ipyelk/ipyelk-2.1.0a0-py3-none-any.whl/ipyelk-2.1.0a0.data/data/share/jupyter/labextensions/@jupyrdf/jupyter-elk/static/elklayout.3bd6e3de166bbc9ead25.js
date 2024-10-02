"use strict";
(self["webpackChunk_jupyrdf_jupyter_elk"] = self["webpackChunk_jupyrdf_jupyter_elk"] || []).push([["elklayout"],{

/***/ "./lib/layout_widget.js":
/*!******************************!*\
  !*** ./lib/layout_widget.js ***!
  \******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   ELKLayoutModel: () => (/* binding */ ELKLayoutModel),
/* harmony export */   ELKTextSizerModel: () => (/* reexport safe */ _measure_text__WEBPACK_IMPORTED_MODULE_4__.ELKTextSizerModel),
/* harmony export */   ELKTextSizerView: () => (/* reexport safe */ _measure_text__WEBPACK_IMPORTED_MODULE_4__.ELKTextSizerView)
/* harmony export */ });
/* harmony import */ var elkjs_lib_elk_api__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! elkjs/lib/elk-api */ "./node_modules/elkjs/lib/elk-api.js");
/* harmony import */ var elkjs_lib_elk_api__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(elkjs_lib_elk_api__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyter-widgets/base */ "webpack/sharing/consume/default/@jupyter-widgets/base");
/* harmony import */ var _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _tokens__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./tokens */ "./lib/tokens.js");
/* harmony import */ var _worker_loader_elkjs_lib_elk_worker_js__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! !!worker-loader!elkjs/lib/elk-worker.js */ "./node_modules/worker-loader/dist/cjs.js!./node_modules/elkjs/lib/elk-worker.js");
/* harmony import */ var _measure_text__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./measure_text */ "./lib/measure_text.js");
/**
 * # Copyright (c) 2024 ipyelk contributors.
 * Distributed under the terms of the Modified BSD License.
 */
// import Worker from '!!worker-loader!elkjs/lib/elk-worker.min.js';







const TheElk = new (elkjs_lib_elk_api__WEBPACK_IMPORTED_MODULE_0___default())({
    workerFactory: () => {
        _tokens__WEBPACK_IMPORTED_MODULE_5__.ELK_DEBUG && console.warn('ELK Worker created');
        return new _worker_loader_elkjs_lib_elk_worker_js__WEBPACK_IMPORTED_MODULE_3__["default"]();
    },
});
function collectProperties(node) {
    let props = new Map();
    function strip(node) {
        props[node.id] = node.properties;
        delete node['properties'];
        // children
        if (node.children) {
            node.children.map(strip);
        }
        // ports
        if (node.ports) {
            node.ports.map(strip);
        }
        // labels
        if (node.labels) {
            node.labels.map(strip);
        }
        // edges
        if (node.edges) {
            node.edges.map(strip);
        }
    }
    strip(node);
    return props;
}
function applyProperties(node, props) {
    function apply(node) {
        node.properties = props[node.id];
        // children
        if (node.children) {
            node.children.map(apply);
        }
        // ports
        if (node.ports) {
            node.ports.map(apply);
        }
        // labels
        if (node.labels) {
            node.labels.map(apply);
        }
        // edges
        if (node.edges) {
            node.edges.map(apply);
        }
    }
    apply(node);
    return node;
}
class ELKLayoutModel extends _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_2__.DOMWidgetModel {
    constructor() {
        super(...arguments);
        this.layoutUpdated = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_1__.Signal(this);
    }
    defaults() {
        let defaults = Object.assign(Object.assign({}, super.defaults()), { _view_module: _tokens__WEBPACK_IMPORTED_MODULE_5__.NAME, _model_name: ELKLayoutModel.model_name, _model_module_version: _tokens__WEBPACK_IMPORTED_MODULE_5__.VERSION, inlet: null, outlet: null });
        return defaults;
    }
    initialize(attributes, options) {
        super.initialize(attributes, options);
        // this.on('change:inlet', this.onInletChanged, this);
        // this.onInletChanged();
        this.on('msg:custom', this.handleMessage, this);
    }
    ensureElk() {
        if (this._elk == null) {
            this._elk = TheElk;
        }
    }
    handleMessage(content) {
        // check message and decide if should call `measure`
        switch (content.action) {
            case 'run':
                this.layout();
                break;
        }
    }
    async layout() {
        var _a;
        // There looks like a bug with how elkjs failing to process edge properties
        // if they are anything more than simple strings. Elkjs doesnt need to operate
        // on the information passed in `properties` from ipyelk to sprotty so this
        // will strip them before calling elk and then reapply after
        // const {rootNode} = this;
        const rootNode = (_a = this.get('inlet')) === null || _a === void 0 ? void 0 : _a.get('value');
        let outlet = this.get('outlet'); // target output
        if (rootNode == null || outlet == null) {
            return null;
        }
        let propmap = collectProperties(rootNode);
        // strip properties out
        this.ensureElk();
        let result;
        try {
            result = await this._elk.layout(rootNode);
            // reapply properties
            applyProperties(result, propmap);
        }
        catch (error) {
            result = {};
            console.error(error);
        }
        outlet.set('value', Object.assign({}, result));
        outlet.save_changes();
        return result;
    }
}
ELKLayoutModel.model_name = 'ELKLayoutModel';
ELKLayoutModel.serializers = Object.assign(Object.assign({}, _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_2__.DOMWidgetModel.serializers), { inlet: { deserialize: _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_2__.unpack_models }, outlet: { deserialize: _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_2__.unpack_models } });


/***/ }),

/***/ "./lib/measure_text.js":
/*!*****************************!*\
  !*** ./lib/measure_text.js ***!
  \*****************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   ELKTextSizerModel: () => (/* binding */ ELKTextSizerModel),
/* harmony export */   ELKTextSizerView: () => (/* binding */ ELKTextSizerView)
/* harmony export */ });
/* harmony import */ var lodash__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! lodash */ "./node_modules/lodash/lodash.js");
/* harmony import */ var lodash__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(lodash__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyter-widgets/base */ "webpack/sharing/consume/default/@jupyter-widgets/base");
/* harmony import */ var _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _tokens__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./tokens */ "./lib/tokens.js");
/**
 * # Copyright (c) 2024 ipyelk contributors.
 * Distributed under the terms of the Modified BSD License.
 */




// import { ElkNode } from './sprotty/sprotty-model';
class ELKTextSizerModel extends _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_1__.DOMWidgetModel {
    defaults() {
        let defaults = Object.assign(Object.assign({}, super.defaults()), { _model_name: ELKTextSizerModel.model_name, _model_module_version: _tokens__WEBPACK_IMPORTED_MODULE_2__.VERSION, _view_module: _tokens__WEBPACK_IMPORTED_MODULE_2__.NAME, _view_name: ELKTextSizerView.view_name, _view_module_version: _tokens__WEBPACK_IMPORTED_MODULE_2__.VERSION, id: String(Math.random()), inlet: null, outlet: null });
        return defaults;
    }
    initialize(attributes, options) {
        super.initialize(attributes, options);
        _tokens__WEBPACK_IMPORTED_MODULE_2__.ELK_DEBUG && console.warn('ELK Test Sizer Init');
        this.on('msg:custom', this.handleMessage, this);
        _tokens__WEBPACK_IMPORTED_MODULE_2__.ELK_DEBUG && console.warn('ELK Text Done Init');
    }
    make_container() {
        const el = document.createElement('div');
        const styledClass = this.get('_dom_classes').filter((dc) => dc.indexOf('styled-widget-') === 0)[0];
        el.classList.add('lm-Widget', _tokens__WEBPACK_IMPORTED_MODULE_2__.ELK_CSS.widget_class, _tokens__WEBPACK_IMPORTED_MODULE_2__.ELK_CSS.sizer_class, styledClass);
        const raw_css = this.get('namespaced_css'); //TODO should this `raw_css` string be escaped?
        el.innerHTML = `<div class="sprotty"><style>${raw_css}</style><svg class="sprotty-graph"><g></g></svg></div>`;
        return el;
    }
    /**
     * SVG Text Element for given text string
     * @param text
     */
    make_label(label) {
        var _a, _b;
        _tokens__WEBPACK_IMPORTED_MODULE_2__.ELK_DEBUG && console.warn('ELK Text Label for text', label);
        let element = createSVGElement('text');
        let classes = [_tokens__WEBPACK_IMPORTED_MODULE_2__.ELK_CSS.label];
        if (((_a = label.properties) === null || _a === void 0 ? void 0 : _a.cssClasses.length) > 0) {
            classes = classes.concat((_b = label.properties) === null || _b === void 0 ? void 0 : _b.cssClasses.split(' '));
        }
        element.classList.add(...classes);
        element.textContent = label.text;
        _tokens__WEBPACK_IMPORTED_MODULE_2__.ELK_DEBUG && console.warn('ELK Text Label', element);
        return element;
    }
    handleMessage(content) {
        // check message and decide if should call `measure`
        switch (content.action) {
            case 'run':
                this.measure();
                break;
        }
    }
    /**
     * Method to take a list of texts and build SVG Text Elements to attach to the DOM
     * @param content message measure request
     */
    measure() {
        var _a;
        const rootNode = (_a = this.get('inlet')) === null || _a === void 0 ? void 0 : _a.get('value');
        let outlet = this.get('outlet'); // target output
        if (rootNode == null || outlet == null) {
            return null;
        }
        _tokens__WEBPACK_IMPORTED_MODULE_2__.ELK_DEBUG && console.log('Root Node:', rootNode);
        let texts = get_labels(rootNode);
        _tokens__WEBPACK_IMPORTED_MODULE_2__.ELK_DEBUG && console.warn('ELK Text Sizer Measure', texts);
        const el = this.make_container();
        const view = el.getElementsByTagName('g')[0];
        const new_g = createSVGElement('g');
        texts.forEach((text) => {
            new_g.appendChild(this.make_label(text));
        });
        view.appendChild(new_g);
        _tokens__WEBPACK_IMPORTED_MODULE_2__.ELK_DEBUG && console.warn('ELK Text Sizer to add node', new_g);
        _tokens__WEBPACK_IMPORTED_MODULE_2__.ELK_DEBUG && console.warn('ELK Text Sizer node', view);
        document.body.prepend(el);
        let elements = Array.from(new_g.getElementsByTagName('text'));
        _tokens__WEBPACK_IMPORTED_MODULE_2__.ELK_DEBUG && console.warn('Sized Text');
        // Callback to take measurements and remove element from DOM
        window.requestAnimationFrame(() => {
            this.read_sizes(texts, elements);
            let output = Object.assign({}, rootNode);
            output['out'] = (0,lodash__WEBPACK_IMPORTED_MODULE_0__.random)();
            outlet.set('value', output);
            outlet.save_changes();
            if (!_tokens__WEBPACK_IMPORTED_MODULE_2__.ELK_DEBUG) {
                document.body.removeChild(el);
            }
        });
    }
    /**
     * Read the given SVG Text Elements sizes and generate TextSize Objects
     * @param texts Original list of text strings requested to size
     * @param elements List of SVG Text Elements to get their respective bounding boxes
     */
    read_sizes(labels, elements) {
        let i = 0;
        for (let element of elements) {
            _tokens__WEBPACK_IMPORTED_MODULE_2__.ELK_DEBUG && console.warn(element.innerHTML);
            const label = labels[i];
            const size = element.getBoundingClientRect();
            label.width = size.width;
            label.height = size.height;
            i++;
        }
    }
}
ELKTextSizerModel.model_name = 'ELKTextSizerModel';
ELKTextSizerModel.serializers = Object.assign(Object.assign({}, _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_1__.DOMWidgetModel.serializers), { inlet: { deserialize: _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_1__.unpack_models }, outlet: { deserialize: _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_1__.unpack_models } });
class ELKTextSizerView extends _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_1__.DOMWidgetView {
    async render() { }
}
ELKTextSizerView.view_name = 'ELKTextSizerView';
/**
 * SVG Required Namespaced Element
 */
function createSVGElement(tag) {
    return document.createElementNS('http://www.w3.org/2000/svg', tag);
}
function get_labels(el) {
    var _a, _b, _c, _d;
    let labels = [];
    if (el === null || el === void 0 ? void 0 : el.labels) {
        for (let label of el.labels) {
            // size only those labels without a width or a height set
            if (!((_b = (_a = label === null || label === void 0 ? void 0 : label.properties) === null || _a === void 0 ? void 0 : _a.shape) === null || _b === void 0 ? void 0 : _b.width) || !((_d = (_c = label === null || label === void 0 ? void 0 : label.properties) === null || _c === void 0 ? void 0 : _c.shape) === null || _d === void 0 ? void 0 : _d.height)) {
                labels.push(label);
            }
        }
    }
    for (let child of (el === null || el === void 0 ? void 0 : el.ports) || []) {
        labels.push(...get_labels(child));
    }
    for (let child of (el === null || el === void 0 ? void 0 : el.children) || []) {
        labels.push(...get_labels(child));
    }
    for (let edge of (el === null || el === void 0 ? void 0 : el.edges) || []) {
        labels.push(...get_labels(edge));
    }
    for (let label of (el === null || el === void 0 ? void 0 : el.labels) || []) {
        labels.push(...get_labels(label));
    }
    return labels;
}


/***/ })

}]);
//# sourceMappingURL=elklayout.3bd6e3de166bbc9ead25.js.map?v=3bd6e3de166bbc9ead25