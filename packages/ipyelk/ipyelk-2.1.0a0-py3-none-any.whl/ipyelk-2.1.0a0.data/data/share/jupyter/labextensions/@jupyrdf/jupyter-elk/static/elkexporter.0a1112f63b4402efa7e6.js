"use strict";
(self["webpackChunk_jupyrdf_jupyter_elk"] = self["webpackChunk_jupyrdf_jupyter_elk"] || []).push([["elkexporter"],{

/***/ "./node_modules/raw-loader/dist/cjs.js!./style/diagram.css":
/*!*****************************************************************!*\
  !*** ./node_modules/raw-loader/dist/cjs.js!./style/diagram.css ***!
  \*****************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ("/**\n * # Copyright (c) 2024 ipyelk contributors.\n * Distributed under the terms of the Modified BSD License.\n */\n\n/*\n  CSS for in-DOM or standalone viewing: all selectors should tolerate having\n  `.jp-ElkView` stripped.\n*/\n:root {\n  --jp-elk-stroke-width: 1;\n\n  --jp-elk-node-fill: var(--jp-layout-color1);\n  --jp-elk-node-stroke: var(--jp-border-color0);\n\n  --jp-elk-edge-stroke: var(--jp-border-color0);\n\n  --jp-elk-port-fill: var(--jp-layout-color1);\n  --jp-elk-port-stroke: var(--jp-border-color0);\n\n  --jp-elk-label-color: var(--jp-ui-font-color0);\n  --jp-elk-label-font: var(--jp-content-font-family);\n  --jp-elk-label-font-size: var(--jp-ui-font-size0);\n\n  /* stable states */\n  --jp-elk-color-selected: var(--jp-brand-color2);\n  --jp-elk-stroke-width-selected: 3;\n\n  /* interactive states */\n  --jp-elk-stroke-hover: var(--jp-brand-color3);\n  --jp-elk-stroke-width-hover: 2;\n\n  --jp-elk-stroke-hover-selected: var(--jp-warn-color3);\n\n  /* sugar */\n  --jp-elk-transition: 0.1s ease-in;\n}\n\n/* firefox doesnt apply style correctly with the addition of .jp-ElkView */\nsymbol.elksymbol {\n  overflow: visible;\n}\n\n.jp-ElkView .elknode {\n  stroke: var(--jp-elk-node-stroke);\n  stroke-width: var(--jp-elk-stroke-width);\n  fill: var(--jp-elk-node-fill);\n}\n\n.jp-ElkView .elkport {\n  stroke: var(--jp-elk-port-stroke);\n  stroke-width: var(--jp-elk-stroke-width);\n  fill: var(--jp-elk-port-fill);\n}\n\n.jp-ElkView .elkedge {\n  fill: none;\n  stroke: var(--jp-elk-edge-stroke);\n  stroke-width: var(--jp-elk-stroke-width);\n}\n\n.jp-ElkView .elklabel {\n  stroke-width: 0;\n  stroke: var(--jp-elk-label-color);\n  fill: var(--jp-elk-label-color);\n  font-family: var(--jp-elk-label-font);\n  font-size: var(--jp-elk-label-font-size);\n  dominant-baseline: hanging;\n}\n\n.jp-ElkView .elkjunction {\n  stroke: none;\n  fill: var(--jp-elk-edge-stroke);\n}\n\n/* stable states */\n.jp-ElkView .elknode.selected,\n.jp-ElkView .elkport.selected,\n.jp-ElkView .elkedge.selected,\n.jp-ElkView .elkedge.selected .elkarrow {\n  stroke: var(--jp-elk-color-selected);\n  stroke-width: var(--jp-elk-stroke-width-selected);\n  transition: stroke stroke-width var(--jp-elk-transition);\n}\n\n.jp-ElkView .elklabel.selected {\n  fill: var(--jp-elk-color-selected);\n  transition: fill var(--jp-elk-transition);\n}\n\n/* interactive states: elklabel does not have a mouseover selector/ancestor */\n.jp-ElkView .elknode.mouseover,\n.jp-ElkView .elkport.mouseover,\n.jp-ElkView .elkedge.mouseover {\n  stroke: var(--jp-elk-stroke-hover);\n  stroke-width: var(--jp-elk-stroke-width-hover);\n  transition: stroke stroke-width var(--jp-elk-transition);\n}\n\n.jp-ElkView .elklabel.mouseover {\n  fill: var(--jp-elk-stroke-hover);\n  transition: fill stroke var(--jp-elk-transition);\n}\n\n.jp-ElkView .elknode.selected.mouseover,\n.jp-ElkView .elkport.selected.mouseover,\n.jp-ElkView .elkedge.selected.mouseover,\n.jp-ElkView .elkedge.selected.mouseover .elkarrow {\n  stroke-width: var(--jp-elk-stroke-width-hover);\n  stroke: var(--jp-elk-stroke-hover-selected);\n  transition: fill stroke var(--jp-elk-transition);\n}\n\n.jp-ElkView .elklabel.selected.mouseover {\n  fill: var(--jp-elk-stroke-hover-selected);\n  transition: fill stroke var(--jp-elk-transition);\n}\n\n.elkcontainer.widget {\n  overflow: hidden;\n}\n\n.elkcontainer.widget .jupyter-widgets {\n  transition: transform 0.5s;\n}\n");

/***/ }),

/***/ "./lib/exporter.js":
/*!*************************!*\
  !*** ./lib/exporter.js ***!
  \*************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   ELKExporterModel: () => (/* binding */ ELKExporterModel),
/* harmony export */   ELKExporterView: () => (/* binding */ ELKExporterView)
/* harmony export */ });
/* harmony import */ var _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyter-widgets/base */ "webpack/sharing/consume/default/@jupyter-widgets/base");
/* harmony import */ var _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _display_widget__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./display_widget */ "./lib/display_widget.js");
/* harmony import */ var _tokens__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./tokens */ "./lib/tokens.js");
/* harmony import */ var _raw_loader_style_diagram_css__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! !!raw-loader!../style/diagram.css */ "./node_modules/raw-loader/dist/cjs.js!./style/diagram.css");
/* harmony import */ var _raw_loader_jupyterlab_apputils_style_materialcolors_css__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! !!raw-loader!@jupyterlab/apputils/style/materialcolors.css */ "./node_modules/raw-loader/dist/cjs.js!./node_modules/@jupyterlab/apputils/style/materialcolors.css");
/* harmony import */ var _raw_loader_jupyterlab_theme_light_extension_style_variables_css__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! !!raw-loader!@jupyterlab/theme-light-extension/style/variables.css */ "./node_modules/raw-loader/dist/cjs.js!./node_modules/@jupyterlab/theme-light-extension/style/variables.css");
/**
 * # Copyright (c) 2024 ipyelk contributors.
 * Distributed under the terms of the Modified BSD License.
 */







const STANDALONE_CSS = `
  ${_raw_loader_jupyterlab_apputils_style_materialcolors_css__WEBPACK_IMPORTED_MODULE_2__["default"]}
  ${_raw_loader_jupyterlab_theme_light_extension_style_variables_css__WEBPACK_IMPORTED_MODULE_3__["default"]}
  ${_raw_loader_style_diagram_css__WEBPACK_IMPORTED_MODULE_1__["default"]}
`
    .replace(/\/\*(.|\n)*?\*\//gm, ' ')
    .replace(/.jp-ElkView /g, '')
    .replace(/\n/g, ' ')
    .replace(/\s+/g, ' ')
    .replace(/\}/g, '}\n');
const XML_HEADER = '<?xml version="1.0" standalone="no"?>';
class ELKExporterModel extends _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_0__.WidgetModel {
    defaults() {
        let defaults = Object.assign(Object.assign({}, super.defaults()), { _model_name: ELKExporterModel.model_name, _model_module_version: _tokens__WEBPACK_IMPORTED_MODULE_4__.VERSION, _view_module: _tokens__WEBPACK_IMPORTED_MODULE_4__.NAME, _view_name: ELKExporterView.view_name, _view_module_version: _tokens__WEBPACK_IMPORTED_MODULE_4__.VERSION, viewer: null, value: null, enabled: true, extra_css: '', padding: 20, diagram: null, strip_ids: true, add_xml_header: true });
        return defaults;
    }
    get enabled() {
        return this.get('enabled') || true;
    }
    get viewer() {
        return this.get('viewer');
    }
    get diagram() {
        return this.get('diagram');
    }
    get diagram_raw_css() {
        var _a;
        return ((_a = this.diagram) === null || _a === void 0 ? void 0 : _a.get('raw_css')) || [];
    }
    initialize(attributes, options) {
        super.initialize(attributes, options);
        this.on('change:viewer', this._on_viewer_changed, this);
        this.on('change:diagram', this._on_diagram_changed, this);
        this._on_viewer_changed();
        this._on_diagram_changed();
    }
    _on_viewer_changed() {
        var _a;
        _tokens__WEBPACK_IMPORTED_MODULE_4__.ELK_DEBUG && console.warn('[export] viewer changed', arguments);
        if (((_a = this.viewer) === null || _a === void 0 ? void 0 : _a.diagramUpdated) == null) {
            return;
        }
        this.viewer.diagramUpdated.connect(this._schedule_update, this);
        if (!this.enabled) {
            return;
        }
        this._schedule_update();
    }
    is_an_elkmodel(model) {
        return model instanceof _display_widget__WEBPACK_IMPORTED_MODULE_5__.ELKViewerModel;
    }
    _on_diagram_changed() {
        _tokens__WEBPACK_IMPORTED_MODULE_4__.ELK_DEBUG && console.warn('[export] diagram changed', arguments);
        const { diagram } = this;
        if ((diagram === null || diagram === void 0 ? void 0 : diagram.on) != null) {
            diagram.on('change:raw_css', this._schedule_update, this);
            const children = diagram.get('children') || [];
            const viewers = children.filter(this.is_an_elkmodel);
            if (viewers.length && viewers[0].diagramUpdated) {
                viewers[0].diagramUpdated.connect(this._schedule_update, this);
            }
            else {
                _tokens__WEBPACK_IMPORTED_MODULE_4__.ELK_DEBUG && console.warn('[export] no diagram ready', children);
            }
        }
    }
    async a_view() {
        var _a;
        if (!this.enabled) {
            return;
        }
        let views = this.viewer.views;
        if ((_a = this.diagram) === null || _a === void 0 ? void 0 : _a.views) {
            views = Object.assign(Object.assign({}, views), this.diagram.views);
        }
        if (!Object.keys(views).length) {
            return;
        }
        for (const promise of Object.values(views)) {
            const view = (await promise);
            if (view.el) {
                await view.displayed;
                return view;
            }
        }
    }
    _schedule_update() {
        if (!this.enabled) {
            return;
        }
        if (this._update_timeout != null) {
            window.clearInterval(this._update_timeout);
            this._update_timeout = null;
        }
        // does weird stuff with `this` apparently
        this._update_timeout = setTimeout(() => this._on_layout_updated(), 1000);
    }
    async _on_layout_updated() {
        var _a;
        if (!this.enabled) {
            return;
        }
        const view = await this.a_view();
        const svg = (_a = view === null || view === void 0 ? void 0 : view.el) === null || _a === void 0 ? void 0 : _a.querySelector('svg');
        if (svg == null) {
            this._schedule_update();
            return;
        }
        const { outerHTML } = svg;
        const padding = this.get('padding');
        const strip_ids = this.get('strip_ids');
        const add_xml_header = this.get('add_xml_header');
        const raw_diagram_css = this.diagram_raw_css;
        const rawStyle = `
        ${STANDALONE_CSS}
        ${raw_diagram_css.join('\n')}
        ${this.get('extra_css') || ''}
    `;
        const style = `
      <style type="text/css">
        <![CDATA[
          ${rawStyle}
        ]]>
      </style>`;
        const g = svg.querySelector('g');
        if (g == null) {
            // bail if not g
            return;
        }
        const transform = g.attributes['transform'].value;
        let scaleFactor = 1.0;
        const scale = transform.match(/scale\((.*?)\)/);
        if (scale != null) {
            scaleFactor = parseFloat(scale[1]);
        }
        const { width, height } = g.getBoundingClientRect();
        let withCSS = outerHTML
            .replace(/<svg([^>]+)>/, `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${width / scaleFactor + padding} ${height / scaleFactor + padding}" $1>
          ${style}
        `)
            .replace(/ transform=".*?"/, '');
        if (strip_ids) {
            withCSS = withCSS.replace(/\s*id="[^"]*"\s*/g, ' ');
        }
        if (add_xml_header) {
            withCSS = `${XML_HEADER}\n${withCSS}`;
        }
        this.set({ value: withCSS });
        this.save_changes(view.callbacks);
    }
}
ELKExporterModel.model_name = 'ELKExporterModel';
ELKExporterModel.serializers = Object.assign(Object.assign({}, _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_0__.WidgetModel.serializers), { viewer: { deserialize: _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_0__.unpack_models }, diagram: { deserialize: _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_0__.unpack_models } });
class ELKExporterView extends _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_0__.WidgetView {
}
ELKExporterView.view_name = 'ELKExporterView';


/***/ })

}]);
//# sourceMappingURL=elkexporter.0a1112f63b4402efa7e6.js.map?v=0a1112f63b4402efa7e6