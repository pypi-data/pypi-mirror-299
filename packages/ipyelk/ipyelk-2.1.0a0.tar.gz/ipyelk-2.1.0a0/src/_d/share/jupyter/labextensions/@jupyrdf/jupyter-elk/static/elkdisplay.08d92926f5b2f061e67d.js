"use strict";
(self["webpackChunk_jupyrdf_jupyter_elk"] = self["webpackChunk_jupyrdf_jupyter_elk"] || []).push([["elkdisplay"],{

/***/ "./lib/display_widget.js":
/*!*******************************!*\
  !*** ./lib/display_widget.js ***!
  \*******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   ELKControlModel: () => (/* binding */ ELKControlModel),
/* harmony export */   ELKViewerModel: () => (/* binding */ ELKViewerModel),
/* harmony export */   ELKViewerView: () => (/* binding */ ELKViewerView)
/* harmony export */ });
/* harmony import */ var lodash_difference__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! lodash/difference */ "./node_modules/lodash/difference.js");
/* harmony import */ var lodash_difference__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(lodash_difference__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var sprotty_protocol__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! sprotty-protocol */ "webpack/sharing/consume/default/sprotty-protocol/sprotty-protocol");
/* harmony import */ var sprotty_protocol__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(sprotty_protocol__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var sprotty__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! sprotty */ "webpack/sharing/consume/default/sprotty/sprotty");
/* harmony import */ var sprotty__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(sprotty__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @jupyter-widgets/base */ "webpack/sharing/consume/default/@jupyter-widgets/base");
/* harmony import */ var _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _sprotty_di_config__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./sprotty/di-config */ "./lib/sprotty/di-config.js");
/* harmony import */ var _tokens__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./tokens */ "./lib/tokens.js");
/* harmony import */ var _tools__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./tools */ "./lib/tools/select.js");
/* harmony import */ var _tools__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ./tools */ "./lib/tools/expand.js");
/* harmony import */ var _tools_types__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./tools/types */ "./lib/tools/types.js");
/**
 * # Copyright (c) 2024 ipyelk contributors.
 * Distributed under the terms of the Modified BSD License.
 */


// import { WidgetManager } from '@jupyter-widgets/jupyterlab-manager';
// import { ManagerBase } from '@jupyter-widgets/base';





// import { VNode } from 'snabbdom';



const POLL = 300;
class ELKControlModel extends _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_5__.DOMWidgetModel {
    defaults() {
        let defaults = Object.assign(Object.assign({}, super.defaults()), { _model_name: ELKControlModel.model_name, _model_module_version: _tokens__WEBPACK_IMPORTED_MODULE_6__.VERSION, 
            //    _view_module: NAME,
            //    _view_name: ELKViewerView.view_name,
            //    _view_module_version: VERSION,
            overlay: null });
        return defaults;
    }
}
ELKControlModel.model_name = 'ELKControlModel';
ELKControlModel.serializers = Object.assign(Object.assign({}, _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_5__.DOMWidgetModel.serializers), { overlay: { deserialize: _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_5__.unpack_models } });
class ELKViewerModel extends _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_5__.DOMWidgetModel {
    constructor() {
        super(...arguments);
        this.layoutUpdated = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_4__.Signal(this);
        this.diagramUpdated = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_4__.Signal(this);
    }
    defaults() {
        let defaults = Object.assign(Object.assign({}, super.defaults()), { _model_name: ELKViewerModel.model_name, _model_module_version: _tokens__WEBPACK_IMPORTED_MODULE_6__.VERSION, _view_module: _tokens__WEBPACK_IMPORTED_MODULE_6__.NAME, _view_name: ELKViewerView.view_name, _view_module_version: _tokens__WEBPACK_IMPORTED_MODULE_6__.VERSION, symbols: {}, source: null, control_overlay: null });
        return defaults;
    }
    initialize(attributes, options) {
        super.initialize(attributes, options);
    }
}
ELKViewerModel.model_name = 'ELKViewerModel';
ELKViewerModel.serializers = Object.assign(Object.assign({}, _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_5__.DOMWidgetModel.serializers), { source: { deserialize: _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_5__.unpack_models }, selection: { deserialize: _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_5__.unpack_models }, hover: { deserialize: _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_5__.unpack_models }, painter: { deserialize: _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_5__.unpack_models }, zoom: { deserialize: _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_5__.unpack_models }, pan: { deserialize: _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_5__.unpack_models }, control_overlay: { deserialize: _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_5__.unpack_models } });
class ELKViewerView extends _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_5__.DOMWidgetView {
    constructor() {
        super(...arguments);
        this.was_shown = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_3__.PromiseDelegate();
        this.wait_for_visible = (initial = false) => {
            if (!this.luminoWidget.isVisible) {
                this.was_shown.resolve();
            }
            else {
                setTimeout(this.wait_for_visible, initial ? 0 : POLL);
            }
        };
        this.resize = (width = -1, height = -1) => {
            if (width === -1 || height === -1) {
                const rect = this.el.getBoundingClientRect();
                width = rect.width;
                height = rect.height;
            }
            this.source.resize({ width, height, x: 0, y: 0 });
        };
    }
    initialize(parameters) {
        super.initialize(parameters);
        this.luminoWidget.addClass(_tokens__WEBPACK_IMPORTED_MODULE_6__.ELK_CSS.widget_class);
        this.on('change:source', this.on_source_changed, this);
        this.on_source_changed();
    }
    async on_source_changed() {
        // TODO disconnect old ones
        let source = this.model.get('source');
        if (source) {
            source.on('change:value', this.diagramLayout, this);
            this.diagramLayout();
        }
    }
    async render() {
        const root = this.el;
        const sprottyDiv = document.createElement('div');
        this.div_id = sprottyDiv.id = Private.next_id();
        root.appendChild(sprottyDiv);
        // don't bother initializing sprotty until actually on the page
        // schedule it
        this.initSprotty().catch(console.warn);
        this.wait_for_visible(true);
    }
    async initSprotty() {
        await this.was_shown.promise;
        // Create Sprotty viewer
        const container = (0,_sprotty_di_config__WEBPACK_IMPORTED_MODULE_7__["default"])(this.div_id, this);
        this.container = container;
        this.source = container.get(sprotty__WEBPACK_IMPORTED_MODULE_2__.TYPES.ModelSource);
        this.source.diagramWidget = this;
        this.source.widget_manager = this.model.widget_manager;
        this.source.factory = container.get(sprotty__WEBPACK_IMPORTED_MODULE_2__.TYPES.IModelFactory);
        // this.toolManager = container.get<ToolManager>(TYPES.IToolManager);
        this.registry = container.get(sprotty__WEBPACK_IMPORTED_MODULE_2__.ActionHandlerRegistry);
        this.actionDispatcher = container.get(sprotty__WEBPACK_IMPORTED_MODULE_2__.TYPES.IActionDispatcher);
        this.feedbackDispatcher = container.get(_tools_types__WEBPACK_IMPORTED_MODULE_8__.ToolTYPES.IFeedbackActionDispatcher);
        // this.model.on('change:mark_layout', this.diagramLayout, this);
        this.model.on('change:selection', this.updateSelectedTool, this);
        this.model.on('change:hover', this.updateHoverTool, this);
        this.model.on('change:interaction', this.interaction_mode_changed, this);
        this.model.on('msg:custom', this.handleMessage, this);
        this.model.on('change:symbols', this.diagramLayout, this);
        this.model.on('change:control_overlay', this.updateControlOverlay, this);
        // init for the first time
        this.updateSelectedTool();
        this.updateHoverTool();
        this.updateControlOverlay();
        this.touch(); //to sync back the diagram state
        // Register Action Handlers
        this.registry.register(sprotty_protocol__WEBPACK_IMPORTED_MODULE_1__.SelectAction.KIND, this);
        this.registry.register(sprotty_protocol__WEBPACK_IMPORTED_MODULE_1__.SelectionResult.KIND, this); //sprotty complains if doesn't have a SelectionResult handler
        this.registry.register(sprotty_protocol__WEBPACK_IMPORTED_MODULE_1__.HoverFeedbackAction.KIND, this);
        // getting hook for
        this.registry.register(sprotty_protocol__WEBPACK_IMPORTED_MODULE_1__.SetModelAction.KIND, this);
        this.registry.register(sprotty_protocol__WEBPACK_IMPORTED_MODULE_1__.UpdateModelAction.KIND, this);
        // Register Tools
        // this.toolManager.registerDefaultTools(
        container.resolve(_tools__WEBPACK_IMPORTED_MODULE_9__.NodeSelectTool).enable();
        container.resolve(_tools__WEBPACK_IMPORTED_MODULE_10__.NodeExpandTool).enable();
        // );
        // this.toolManager.enableDefaultTools();
        this.diagramLayout().catch((err) => console.warn('ELK Failed initial view render', err));
        // timeout is ugly workaround for gh issue #94. Still potential for bounding
        // box being stale but added resize call to the `fit` and `center` actions
        // as additional protection.
        setTimeout(() => {
            // this.resize();
            this.handleMessage({
                action: 'fit',
                animate: false,
                padding: 0,
            });
        }, 10 * POLL);
    }
    updateControlOverlay() {
        let overlay = this.model.get('control_overlay');
        this.source.control_overlay = overlay;
    }
    processPhosphorMessage(msg) {
        this.processLuminoMessage(msg);
    }
    processLuminoMessage(msg) {
        super.processLuminoMessage(msg);
        switch (msg.type) {
            case 'resize':
                const resizeMessage = msg;
                let { width, height } = resizeMessage;
                this.resize(width, height);
                break;
            case 'after-show':
                this.resize();
                break;
        }
    }
    handle(action) {
        switch (action.kind) {
            case sprotty_protocol__WEBPACK_IMPORTED_MODULE_1__.SelectAction.KIND:
                this.source.getSelection().then((selection) => {
                    let ids = [];
                    let nodes = [];
                    selection.forEach((node, i) => {
                        ids.push(node.id);
                        nodes.push(node);
                    });
                    let selectionTool = this.model.get('selection');
                    if (selectionTool != null) {
                        selectionTool.set('ids', ids);
                        selectionTool.save_changes();
                        this.setSelectedNodes(ids);
                        this.model.diagramUpdated.emit(void 0);
                    }
                });
                break;
            case sprotty_protocol__WEBPACK_IMPORTED_MODULE_1__.SelectionResult.KIND:
                break;
            case sprotty_protocol__WEBPACK_IMPORTED_MODULE_1__.HoverFeedbackAction.KIND:
                let hoverFeedback = action;
                if (hoverFeedback.mouseIsOver) {
                    let hover = this.model.get('hover');
                    if (hover != null) {
                        hover.set('ids', hoverFeedback.mouseoverElement);
                        hover.save_changes();
                        this.model.diagramUpdated.emit(void 0);
                    }
                }
                break;
            case sprotty_protocol__WEBPACK_IMPORTED_MODULE_1__.SetModelAction.KIND:
                let setModelAction = action;
                const { newRoot } = setModelAction;
                if (newRoot) {
                    this.currentRoot = newRoot;
                }
                break;
            case sprotty_protocol__WEBPACK_IMPORTED_MODULE_1__.UpdateModelAction.KIND:
                break;
            default:
                break;
        }
    }
    updateSelectedTool() {
        let selection = this.model.get('selection');
        if (selection != null) {
            selection.on('change:ids', this.updateSelected, this);
        }
    }
    async updateSelected() {
        let selection = this.model.get('selection');
        if (selection != null) {
            let selected = selection.get('ids');
            let old_selected = selection.previous('ids');
            let exiting = lodash_difference__WEBPACK_IMPORTED_MODULE_0___default()(old_selected, selected);
            let entering = lodash_difference__WEBPACK_IMPORTED_MODULE_0___default()(selected, old_selected);
            await this.actionDispatcher.dispatch(sprotty_protocol__WEBPACK_IMPORTED_MODULE_1__.SelectAction.create({
                selectedElementsIDs: entering,
                deselectedElementsIDs: exiting,
            }));
            this.setSelectedNodes(selected);
            this.model.diagramUpdated.emit(void 0);
        }
    }
    /*
     * Keep reference of the current selected nodes on the selection widget
     */
    async setSelectedNodes(selected) {
        this.source.selectedNodes = selected.map((id) => this.source.index.getById(id));
    }
    updateHoverTool() {
        let hover = this.model.get('hover');
        if (hover != null) {
            hover.on('change:ids', this.updateHover, this);
        }
    }
    async updateHover() {
        let hover = this.model.get('hover');
        if (hover != null) {
            let hovered = hover.get('ids');
            let old_hovered = hover.previous('ids');
            await this.actionDispatcher.dispatchAll([
                sprotty_protocol__WEBPACK_IMPORTED_MODULE_1__.HoverFeedbackAction.create({ mouseoverElement: hovered, mouseIsOver: true }),
                sprotty_protocol__WEBPACK_IMPORTED_MODULE_1__.HoverFeedbackAction.create({
                    mouseoverElement: old_hovered,
                    mouseIsOver: false,
                }),
            ]);
            this.model.diagramUpdated.emit(void 0);
        }
    }
    async interaction_mode_changed() {
        // let interaction = this.model.get('interaction');
    }
    async diagramLayout() {
        var _a;
        let layout = (_a = this.model.get('source')) === null || _a === void 0 ? void 0 : _a.get('value');
        let symbols = this.model.get('symbols');
        if (layout == null || symbols == null || this.source == null) {
            // bailing
            return null;
        }
        await this.source.updateLayout(layout, symbols, this.div_id);
        this.model.layoutUpdated.emit();
        this.model.diagramUpdated.emit();
    }
    normalizeElementIds(model_id) {
        let elementIds = [];
        if (model_id != null) {
            if (!Array.isArray(model_id)) {
                elementIds = [model_id];
            }
            else {
                elementIds = model_id;
            }
        }
        return elementIds;
    }
    handleMessage(content) {
        switch (content.action) {
            case 'center':
                this.resize(); // ensure bounds are accurate before centering
                this.source.center(this.normalizeElementIds(content.model_id), content.animate, content.retain_zoom);
                break;
            case 'fit':
                this.resize(); // ensure bounds are accurate before fitting
                this.source.fit(this.normalizeElementIds(content.model_id), content.padding == null ? 0 : content.padding, content.max_zoom == null ? Infinity : content.max_zoom, content.animate == null ? true : content.animate);
                break;
            default:
                console.warn('ELK unhandled message', content);
                break;
        }
    }
}
ELKViewerView.view_name = 'ELKViewerView';
var Private;
(function (Private) {
    let _next_id = 0;
    function next_id() {
        return `sprotty_${_next_id++}`;
    }
    Private.next_id = next_id;
})(Private || (Private = {}));


/***/ }),

/***/ "./lib/sprotty/di-config.js":
/*!**********************************!*\
  !*** ./lib/sprotty/di-config.js ***!
  \**********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var inversify__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! inversify */ "webpack/sharing/consume/default/inversify/inversify");
/* harmony import */ var inversify__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(inversify__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var sprotty__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! sprotty */ "webpack/sharing/consume/default/sprotty/sprotty");
/* harmony import */ var sprotty__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(sprotty__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _tools_feedback__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ../tools/feedback */ "./lib/tools/feedback/di.config.js");
/* harmony import */ var _diagram_server__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./diagram-server */ "./lib/sprotty/diagram-server.js");
/* harmony import */ var _renderer__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./renderer */ "./lib/sprotty/renderer.js");
/* harmony import */ var _sprotty_model__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./sprotty-model */ "./lib/sprotty/sprotty-model.js");
/* harmony import */ var _update__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./update */ "./lib/sprotty/update/index.js");
/* harmony import */ var _viewportModule__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ./viewportModule */ "./lib/sprotty/viewportModule.js");
/* harmony import */ var _views__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./views */ "./lib/sprotty/views/graph_views.js");
/* harmony import */ var _views__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./views */ "./lib/sprotty/views/node_views.js");
/* harmony import */ var _views__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./views */ "./lib/sprotty/views/edge_views.js");
/* harmony import */ var _views__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./views */ "./lib/sprotty/views/symbol_views.js");
/**
 * # Copyright (c) 2024 ipyelk contributors.
 * Distributed under the terms of the Modified BSD License.
 */
/*******************************************************************************
 * Copyright (c) 2017 TypeFox GmbH (http://www.typefox.io) and others.
 * All rights reserved. This program and the accompanying materials
 * are made available under the terms of the Eclipse Public License v1.0
 * which accompanies this distribution, and is available at
 * http://www.eclipse.org/legal/epl-v10.html
 *******************************************************************************/









class FilteringSvgExporter extends sprotty__WEBPACK_IMPORTED_MODULE_1__.SvgExporter {
    isExported(styleSheet) {
        return (styleSheet.href != null &&
            (styleSheet.href.endsWith('diagram.css') ||
                styleSheet.href.endsWith('sprotty.css')));
    }
}
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ((containerId, view) => {
    const elkGraphModule = new inversify__WEBPACK_IMPORTED_MODULE_0__.ContainerModule((bind, unbind, isBound, rebind) => {
        bind(sprotty__WEBPACK_IMPORTED_MODULE_1__.TYPES.ModelSource).to(_diagram_server__WEBPACK_IMPORTED_MODULE_2__.JLModelSource).inSingletonScope();
        rebind(sprotty__WEBPACK_IMPORTED_MODULE_1__.TYPES.ILogger).to(sprotty__WEBPACK_IMPORTED_MODULE_1__.ConsoleLogger).inSingletonScope();
        rebind(sprotty__WEBPACK_IMPORTED_MODULE_1__.TYPES.LogLevel).toConstantValue(sprotty__WEBPACK_IMPORTED_MODULE_1__.LogLevel.warn);
        rebind(sprotty__WEBPACK_IMPORTED_MODULE_1__.TYPES.SvgExporter).to(FilteringSvgExporter).inSingletonScope();
        const context = { bind, unbind, isBound, rebind };
        // Initialize model element views
        (0,sprotty__WEBPACK_IMPORTED_MODULE_1__.configureModelElement)(context, 'graph', sprotty__WEBPACK_IMPORTED_MODULE_1__.SGraphImpl, _views__WEBPACK_IMPORTED_MODULE_3__.SGraphView);
        (0,sprotty__WEBPACK_IMPORTED_MODULE_1__.configureModelElement)(context, 'node', _sprotty_model__WEBPACK_IMPORTED_MODULE_4__.ElkNode, _views__WEBPACK_IMPORTED_MODULE_5__.ElkNodeView);
        (0,sprotty__WEBPACK_IMPORTED_MODULE_1__.configureModelElement)(context, 'node:use', _sprotty_model__WEBPACK_IMPORTED_MODULE_4__.ElkNode, _views__WEBPACK_IMPORTED_MODULE_5__.ElkUseNodeView);
        (0,sprotty__WEBPACK_IMPORTED_MODULE_1__.configureModelElement)(context, 'node:diamond', _sprotty_model__WEBPACK_IMPORTED_MODULE_4__.ElkNode, _views__WEBPACK_IMPORTED_MODULE_5__.ElkDiamondNodeView);
        (0,sprotty__WEBPACK_IMPORTED_MODULE_1__.configureModelElement)(context, 'node:round', _sprotty_model__WEBPACK_IMPORTED_MODULE_4__.ElkNode, _views__WEBPACK_IMPORTED_MODULE_5__.ElkRoundNodeView);
        (0,sprotty__WEBPACK_IMPORTED_MODULE_1__.configureModelElement)(context, 'node:image', _sprotty_model__WEBPACK_IMPORTED_MODULE_4__.ElkNode, _views__WEBPACK_IMPORTED_MODULE_5__.ElkImageNodeView);
        (0,sprotty__WEBPACK_IMPORTED_MODULE_1__.configureModelElement)(context, 'node:comment', _sprotty_model__WEBPACK_IMPORTED_MODULE_4__.ElkNode, _views__WEBPACK_IMPORTED_MODULE_5__.ElkCommentNodeView);
        (0,sprotty__WEBPACK_IMPORTED_MODULE_1__.configureModelElement)(context, 'node:path', _sprotty_model__WEBPACK_IMPORTED_MODULE_4__.ElkNode, _views__WEBPACK_IMPORTED_MODULE_5__.ElkPathNodeView);
        (0,sprotty__WEBPACK_IMPORTED_MODULE_1__.configureModelElement)(context, 'node:svg', _sprotty_model__WEBPACK_IMPORTED_MODULE_4__.ElkNode, _views__WEBPACK_IMPORTED_MODULE_5__.ElkSVGNodeView);
        (0,sprotty__WEBPACK_IMPORTED_MODULE_1__.configureModelElement)(context, 'node:html', _sprotty_model__WEBPACK_IMPORTED_MODULE_4__.ElkNode, _views__WEBPACK_IMPORTED_MODULE_5__.ElkJLNodeView);
        (0,sprotty__WEBPACK_IMPORTED_MODULE_1__.configureModelElement)(context, 'node:widget', _sprotty_model__WEBPACK_IMPORTED_MODULE_4__.ElkNode, _views__WEBPACK_IMPORTED_MODULE_5__.ElkJLNodeView);
        (0,sprotty__WEBPACK_IMPORTED_MODULE_1__.configureModelElement)(context, 'node:compartment', _sprotty_model__WEBPACK_IMPORTED_MODULE_4__.ElkNode, _views__WEBPACK_IMPORTED_MODULE_5__.ElkCompartmentNodeView);
        (0,sprotty__WEBPACK_IMPORTED_MODULE_1__.configureModelElement)(context, 'node:foreignobject', _sprotty_model__WEBPACK_IMPORTED_MODULE_4__.ElkNode, _views__WEBPACK_IMPORTED_MODULE_5__.ElkForeignObjectNodeView);
        (0,sprotty__WEBPACK_IMPORTED_MODULE_1__.configureModelElement)(context, 'port', _sprotty_model__WEBPACK_IMPORTED_MODULE_4__.ElkPort, _views__WEBPACK_IMPORTED_MODULE_5__.ElkPortView);
        (0,sprotty__WEBPACK_IMPORTED_MODULE_1__.configureModelElement)(context, 'edge', _sprotty_model__WEBPACK_IMPORTED_MODULE_4__.ElkEdge, _views__WEBPACK_IMPORTED_MODULE_6__.ElkEdgeView);
        (0,sprotty__WEBPACK_IMPORTED_MODULE_1__.configureModelElement)(context, 'label', _sprotty_model__WEBPACK_IMPORTED_MODULE_4__.ElkLabel, _views__WEBPACK_IMPORTED_MODULE_5__.ElkLabelView);
        (0,sprotty__WEBPACK_IMPORTED_MODULE_1__.configureModelElement)(context, 'label:icon', _sprotty_model__WEBPACK_IMPORTED_MODULE_4__.ElkLabel, _views__WEBPACK_IMPORTED_MODULE_5__.ElkLabelView);
        (0,sprotty__WEBPACK_IMPORTED_MODULE_1__.configureModelElement)(context, 'junction', _sprotty_model__WEBPACK_IMPORTED_MODULE_4__.ElkJunction, _views__WEBPACK_IMPORTED_MODULE_6__.JunctionView);
        (0,sprotty__WEBPACK_IMPORTED_MODULE_1__.configureViewerOptions)(context, {
            needsClientLayout: false,
            baseDiv: containerId,
        });
        // Hover
        (0,sprotty__WEBPACK_IMPORTED_MODULE_1__.configureCommand)(context, sprotty__WEBPACK_IMPORTED_MODULE_1__.HoverFeedbackCommand);
        // Model elements for symbols
        (0,sprotty__WEBPACK_IMPORTED_MODULE_1__.configureModelElement)(context, 'symbol', _sprotty_model__WEBPACK_IMPORTED_MODULE_4__.SymbolNode, _views__WEBPACK_IMPORTED_MODULE_7__.SymbolNodeView);
        // Expose extracted path and connector offset to the rendering context
        rebind(sprotty__WEBPACK_IMPORTED_MODULE_1__.TYPES.ModelRendererFactory).toFactory((ctx) => (targetKind, processors, args) => {
            const viewRegistry = ctx.container.get(sprotty__WEBPACK_IMPORTED_MODULE_1__.TYPES.ViewRegistry);
            const modelSource = ctx.container.get(sprotty__WEBPACK_IMPORTED_MODULE_1__.TYPES.ModelSource);
            const renderer = new _renderer__WEBPACK_IMPORTED_MODULE_8__.ElkModelRenderer(viewRegistry, targetKind, processors, modelSource, args);
            return renderer;
        });
        rebind(sprotty__WEBPACK_IMPORTED_MODULE_1__.TYPES.IModelFactory).to(_renderer__WEBPACK_IMPORTED_MODULE_8__.SSymbolModelFactory).inSingletonScope();
    });
    const container = new inversify__WEBPACK_IMPORTED_MODULE_0__.Container();
    container.load(sprotty__WEBPACK_IMPORTED_MODULE_1__.defaultModule, sprotty__WEBPACK_IMPORTED_MODULE_1__.boundsModule, sprotty__WEBPACK_IMPORTED_MODULE_1__.moveModule, sprotty__WEBPACK_IMPORTED_MODULE_1__.fadeModule, 
    // //    hoverModule,
    _update__WEBPACK_IMPORTED_MODULE_9__["default"], sprotty__WEBPACK_IMPORTED_MODULE_1__.undoRedoModule, _viewportModule__WEBPACK_IMPORTED_MODULE_10__["default"], sprotty__WEBPACK_IMPORTED_MODULE_1__.routingModule, sprotty__WEBPACK_IMPORTED_MODULE_1__.exportModule, sprotty__WEBPACK_IMPORTED_MODULE_1__.modelSourceModule, sprotty__WEBPACK_IMPORTED_MODULE_1__.edgeEditModule, sprotty__WEBPACK_IMPORTED_MODULE_1__.labelEditModule, _tools_feedback__WEBPACK_IMPORTED_MODULE_11__["default"], sprotty__WEBPACK_IMPORTED_MODULE_1__.edgeLayoutModule, elkGraphModule);
    return container;
});


/***/ }),

/***/ "./lib/sprotty/diagram-server.js":
/*!***************************************!*\
  !*** ./lib/sprotty/diagram-server.js ***!
  \***************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   JLModelSource: () => (/* binding */ JLModelSource)
/* harmony export */ });
/* harmony import */ var inversify__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! inversify */ "webpack/sharing/consume/default/inversify/inversify");
/* harmony import */ var inversify__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(inversify__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var sprotty_protocol__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! sprotty-protocol */ "webpack/sharing/consume/default/sprotty-protocol/sprotty-protocol");
/* harmony import */ var sprotty_protocol__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(sprotty_protocol__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var sprotty__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! sprotty */ "webpack/sharing/consume/default/sprotty/sprotty");
/* harmony import */ var sprotty__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(sprotty__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _tokens__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../tokens */ "./lib/tokens.js");
/* harmony import */ var _json_elkgraph_to_sprotty__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./json/elkgraph-to-sprotty */ "./lib/sprotty/json/elkgraph-to-sprotty.js");
/**
 * # Copyright (c) 2024 ipyelk contributors.
 * Distributed under the terms of the Modified BSD License.
 */
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
/** @jsx svg */





let JLModelSource = class JLModelSource extends sprotty__WEBPACK_IMPORTED_MODULE_2__.LocalModelSource {
    async updateLayout(layout, symbols, idPrefix) {
        this.elkToSprotty = new _json_elkgraph_to_sprotty__WEBPACK_IMPORTED_MODULE_3__.ElkGraphJsonToSprotty();
        let sGraph = this.elkToSprotty.transform(layout, symbols, idPrefix);
        await this.updateModel(sGraph);
        // TODO this promise resolves before ModelViewer rendering is done. need to hook into postprocessing
    }
    get root() {
        return this.factory.root;
    }
    /*
     * Helper method to return the appropriate sprotty model element in the current
     * graph based on id
     */
    getById(id) {
        return this.factory.root.index.getById(id);
    }
    /**
     * Submit the given model with an `UpdateModelAction` or a `SetModelAction` depending on the
     * `update` argument. If available, the model layout engine is invoked first.
     */
    async doSubmitModel(newRoot, update, cause, index) {
        _tokens__WEBPACK_IMPORTED_MODULE_4__.ELK_DEBUG && console.log('doSubmitModel');
        super.doSubmitModel(newRoot, update, cause, index);
        if (!index) {
            index = new sprotty_protocol__WEBPACK_IMPORTED_MODULE_1__.SModelIndex();
            index.add(this.currentRoot);
        }
        this.index = index;
    }
    element() {
        return document.getElementById(this.viewerOptions.baseDiv);
    }
    center(elementIds = [], animate = true, retainZoom = false) {
        let action = sprotty_protocol__WEBPACK_IMPORTED_MODULE_1__.CenterAction.create(elementIds, {
            animate: animate,
            retainZoom: retainZoom,
        });
        this.actionDispatcher.dispatch(action);
    }
    fit(elementIds = [], padding, maxZoom, animate) {
        let action = sprotty_protocol__WEBPACK_IMPORTED_MODULE_1__.FitToScreenAction.create(elementIds, {
            padding: padding,
            maxZoom: maxZoom,
            animate: animate,
        });
        this.actionDispatcher.dispatch(action);
    }
    resize(bounds) {
        let action = sprotty__WEBPACK_IMPORTED_MODULE_2__.InitializeCanvasBoundsAction.create(bounds);
        this.actionDispatcher.dispatch(action);
    }
    /**
     * Get the current viewport from the model.
     */
    async getViewport() {
        const res = await this.actionDispatcher.request(sprotty_protocol__WEBPACK_IMPORTED_MODULE_1__.GetViewportAction.create());
        return {
            scroll: res.viewport.scroll,
            zoom: res.viewport.zoom,
            canvasBounds: res.canvasBounds,
        };
    }
};
JLModelSource = __decorate([
    (0,inversify__WEBPACK_IMPORTED_MODULE_0__.injectable)()
], JLModelSource);



/***/ }),

/***/ "./lib/sprotty/json/elkgraph-json.js":
/*!*******************************************!*\
  !*** ./lib/sprotty/json/elkgraph-json.js ***!
  \*******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   isExtended: () => (/* binding */ isExtended),
/* harmony export */   isPrimitive: () => (/* binding */ isPrimitive)
/* harmony export */ });
/**
 * # Copyright (c) 2024 ipyelk contributors.
 * Distributed under the terms of the Modified BSD License.
 */
function isPrimitive(edge) {
    return (edge.source != null &&
        edge.target != null);
}
function isExtended(edge) {
    return (edge.sources != null &&
        edge.targets != null);
}


/***/ }),

/***/ "./lib/sprotty/json/elkgraph-to-sprotty.js":
/*!*************************************************!*\
  !*** ./lib/sprotty/json/elkgraph-to-sprotty.js ***!
  \*************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   ElkGraphJsonToSprotty: () => (/* binding */ ElkGraphJsonToSprotty),
/* harmony export */   getType: () => (/* binding */ getType)
/* harmony export */ });
/* harmony import */ var _elkgraph_json__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./elkgraph-json */ "./lib/sprotty/json/elkgraph-json.js");
/**
 * # Copyright (c) 2024 ipyelk contributors.
 * Distributed under the terms of the Modified BSD License.
 */

/**
 * Checks the given type string and potentially returns the default type
 */
function getType(type, defaultType = '') {
    if (type == null || type.length == 0) {
        return defaultType;
    }
    return type;
}
function getClasses(element) {
    var _a;
    let classes = (((_a = element.properties) === null || _a === void 0 ? void 0 : _a.cssClasses) || '').trim();
    return classes ? classes.split(' ') : [];
}
class ElkGraphJsonToSprotty {
    constructor() {
        this.nodeIds = new Set();
        this.edgeIds = new Set();
        this.portIds = new Set();
        this.labelIds = new Set();
        this.sectionIds = new Set();
        this.symbolsIds = new Map();
        this.connectors = new Map();
    }
    transform(elkGraph, symbols, idPrefix) {
        let children = [];
        let edges = [];
        if (elkGraph.children) {
            children = elkGraph.children.map(this.transformElkNode, this);
        }
        if (elkGraph.edges) {
            edges = elkGraph.edges.map(this.transformElkEdge, this);
        }
        const sGraph = {
            type: 'graph',
            id: elkGraph.id || 'root',
            children: [...children, ...edges],
            cssClasses: getClasses(elkGraph),
            symbols: this.transformSymbols(symbols, idPrefix),
        };
        return sGraph;
    }
    /**
     * Build up the Sprotty model objects for the SVG Symbols
     * @param symbols
     */
    transformSymbols(symbols, idPrefix) {
        let children = [];
        for (const key in symbols.library) {
            children.push(this.transformSymbol(key, symbols.library[key], idPrefix));
        }
        const sSymbols = {
            children: children,
        };
        return sSymbols;
    }
    transformSymbol(id, symbol, idPrefix) {
        let element = symbol === null || symbol === void 0 ? void 0 : symbol.element;
        let children = [];
        if (element) {
            children = [this.transformSymbolElement(element)];
        }
        this.symbolsIds[id] = `${idPrefix}_${id}`;
        if (symbol.hasOwnProperty('symbol_offset') ||
            symbol.hasOwnProperty('path_offset')) {
            this.connectors[id] = symbol;
        }
        return {
            type: 'symbol',
            id: id,
            children: children,
            position: this.pos(symbol),
            size: this.size(symbol),
            properties: symbol.properties,
        };
    }
    transformSymbolElement(elkNode) {
        var _a, _b;
        elkNode.properties.isSymbol = true;
        let sNode = {
            id: elkNode.id,
            position: this.pos(elkNode),
            size: this.size(elkNode),
            cssClasses: getClasses(elkNode),
            children: [],
            properties: elkNode.properties,
            type: getType((_b = (_a = elkNode === null || elkNode === void 0 ? void 0 : elkNode.properties) === null || _a === void 0 ? void 0 : _a.shape) === null || _b === void 0 ? void 0 : _b.type, 'node'),
        };
        const sNodes = elkNode.children.map(this.transformSymbolElement, this);
        sNode.children.push(...sNodes);
        return sNode;
    }
    transformElkNode(elkNode) {
        var _a, _b;
        this.checkAndRememberId(elkNode, this.nodeIds);
        const sNode = {
            type: getType((_b = (_a = elkNode === null || elkNode === void 0 ? void 0 : elkNode.properties) === null || _a === void 0 ? void 0 : _a.shape) === null || _b === void 0 ? void 0 : _b.type, 'node'),
            id: elkNode.id,
            position: this.pos(elkNode),
            size: this.size(elkNode),
            children: [],
            cssClasses: getClasses(elkNode),
            properties: elkNode === null || elkNode === void 0 ? void 0 : elkNode.properties,
            layoutOptions: elkNode === null || elkNode === void 0 ? void 0 : elkNode.layoutOptions,
        };
        // children
        if (elkNode.children) {
            const sNodes = elkNode.children.map(this.transformElkNode, this);
            sNode.children.push(...sNodes);
        }
        // ports
        if (elkNode.ports) {
            const sPorts = elkNode.ports.map(this.transformElkPort, this);
            sNode.children.push(...sPorts);
        }
        // labels
        if (elkNode.labels) {
            const sLabels = elkNode.labels.map(this.transformElkLabel, this);
            sNode.children.push(...sLabels);
        }
        // edges
        if (elkNode.edges) {
            const sEdges = elkNode.edges.map(this.transformElkEdge, this);
            sNode.children.push(...sEdges);
        }
        return sNode;
    }
    transformElkPort(elkPort) {
        var _a, _b;
        this.checkAndRememberId(elkPort, this.portIds);
        const sPort = {
            type: getType((_b = (_a = elkPort.properties) === null || _a === void 0 ? void 0 : _a.shape) === null || _b === void 0 ? void 0 : _b.type, 'port'),
            id: elkPort.id,
            position: this.pos(elkPort),
            size: this.size(elkPort),
            children: [],
            cssClasses: getClasses(elkPort),
            properties: elkPort === null || elkPort === void 0 ? void 0 : elkPort.properties,
            layoutOptions: elkPort === null || elkPort === void 0 ? void 0 : elkPort.layoutOptions,
        };
        // labels
        if (elkPort.labels) {
            const sLabels = elkPort.labels.map(this.transformElkLabel, this);
            sPort.children.push(...sLabels);
        }
        return sPort;
    }
    transformElkLabel(elkLabel) {
        var _a, _b;
        this.checkAndRememberId(elkLabel, this.labelIds);
        let sLabel = {
            type: getType((_b = (_a = elkLabel.properties) === null || _a === void 0 ? void 0 : _a.shape) === null || _b === void 0 ? void 0 : _b.type, 'label'),
            id: elkLabel.id,
            text: elkLabel.text,
            position: this.pos(elkLabel),
            size: this.size(elkLabel),
            cssClasses: getClasses(elkLabel),
            labels: [],
            properties: elkLabel === null || elkLabel === void 0 ? void 0 : elkLabel.properties,
            layoutOptions: elkLabel === null || elkLabel === void 0 ? void 0 : elkLabel.layoutOptions,
        };
        if (elkLabel.labels) {
            const sLabels = elkLabel.labels.map(this.transformElkLabel, this);
            sLabel.labels.push(...sLabels);
        }
        return sLabel;
    }
    transformElkEdge(elkEdge) {
        var _a, _b;
        this.checkAndRememberId(elkEdge, this.edgeIds);
        const sEdge = {
            type: getType((_b = (_a = elkEdge.properties) === null || _a === void 0 ? void 0 : _a.shape) === null || _b === void 0 ? void 0 : _b.type, 'edge'),
            id: elkEdge.id,
            sourceId: '',
            targetId: '',
            routingPoints: [],
            children: [],
            cssClasses: getClasses(elkEdge),
            properties: elkEdge === null || elkEdge === void 0 ? void 0 : elkEdge.properties,
            layoutOptions: elkEdge === null || elkEdge === void 0 ? void 0 : elkEdge.layoutOptions,
        };
        if ((0,_elkgraph_json__WEBPACK_IMPORTED_MODULE_0__.isPrimitive)(elkEdge)) {
            sEdge.sourceId = elkEdge.source;
            sEdge.targetId = elkEdge.target;
            if (elkEdge.sourcePoint)
                sEdge.routingPoints.push(elkEdge.sourcePoint);
            if (elkEdge.bendPoints)
                sEdge.routingPoints.push(...elkEdge.bendPoints);
            if (elkEdge.targetPoint)
                sEdge.routingPoints.push(elkEdge.targetPoint);
        }
        else if ((0,_elkgraph_json__WEBPACK_IMPORTED_MODULE_0__.isExtended)(elkEdge)) {
            sEdge.sourceId = elkEdge.sources[0];
            sEdge.targetId = elkEdge.targets[0];
            if (elkEdge.sections) {
                elkEdge.sections.forEach((section) => {
                    this.checkAndRememberId(section, this.sectionIds);
                    sEdge.routingPoints.push(section.startPoint);
                    if (section.bendPoints) {
                        sEdge.routingPoints.push(...section.bendPoints);
                    }
                    sEdge.routingPoints.push(section.endPoint);
                });
            }
        }
        if (elkEdge.junctionPoints) {
            elkEdge.junctionPoints.forEach((jp, i) => {
                const sJunction = {
                    type: 'junction',
                    id: elkEdge.id + '_j' + i,
                    position: jp,
                };
                sEdge.children.push(sJunction);
            });
        }
        // labels
        if (elkEdge.labels) {
            const sLabels = elkEdge.labels.map(this.transformElkLabel, this);
            sEdge.children.push(...sLabels);
        }
        return sEdge;
    }
    pos(elkShape) {
        return { x: elkShape.x || 0, y: elkShape.y || 0 };
    }
    size(elkShape) {
        return {
            width: elkShape.width || 0,
            height: elkShape.height || 0,
        };
    }
    checkAndRememberId(e, set) {
        if (e.id == null) {
            throw Error('An element is missing an id.');
        }
        else if (set.has(e.id)) {
            throw Error('Duplicate id: ' + e.id + '.');
        }
        else {
            set.add(e.id);
        }
    }
}


/***/ }),

/***/ "./lib/sprotty/renderer.js":
/*!*********************************!*\
  !*** ./lib/sprotty/renderer.js ***!
  \*********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   ElkModelRenderer: () => (/* binding */ ElkModelRenderer),
/* harmony export */   SSymbolModelFactory: () => (/* binding */ SSymbolModelFactory),
/* harmony export */   mergeBounds: () => (/* binding */ mergeBounds)
/* harmony export */ });
/* harmony import */ var sprotty_protocol__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! sprotty-protocol */ "webpack/sharing/consume/default/sprotty-protocol/sprotty-protocol");
/* harmony import */ var sprotty_protocol__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(sprotty_protocol__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var sprotty__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! sprotty */ "webpack/sharing/consume/default/sprotty/sprotty");
/* harmony import */ var sprotty__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(sprotty__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _tokens__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../tokens */ "./lib/tokens.js");
/* harmony import */ var _sprotty_model__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./sprotty-model */ "./lib/sprotty/sprotty-model.js");






/**
 * Custom Renderer allowing the layering of jupyterlab widgets on top of the
 * sprotty elements.
 */
class ElkModelRenderer extends sprotty__WEBPACK_IMPORTED_MODULE_1__.ModelRenderer {
    constructor(viewRegistry, targetKind, postprocessors, source, args = {}) {
        super(viewRegistry, targetKind, postprocessors, args);
        this.viewRegistry = viewRegistry;
        this.targetKind = targetKind;
        this.args = args;
        this.source = source;
        this.widgets = new Map();
    }
    getSelected() {
        var _a;
        let elements = [];
        if ((_a = this.source.selectedNodes) === null || _a === void 0 ? void 0 : _a.length) {
            for (let selected of this.source.selectedNodes) {
                let element = this.source.getById(selected.id); // as ElkNode
                elements.push(element);
                // if (element instanceof ElkNode){
                //   elements.push(element);
                // }
            }
        }
        return elements;
    }
    /**
     * Method to render potential overlay controls based on the selected diagram node
     */
    renderJLOverlayControl(args) {
        _tokens__WEBPACK_IMPORTED_MODULE_3__.ELK_DEBUG && console.log('render control overlay');
        let vnodes = [];
        if (this.source.control_overlay) {
            let selected = this.getSelected();
            // filter selectedNodes...
            if (selected.length == 0 || !selected[0]) {
                // exit is nothing is selected or no control_overlay
                return vnodes;
            }
            let overlay_widget = this.source.control_overlay;
            // let activeNode = selected[0];
            let elkNode = new _sprotty_model__WEBPACK_IMPORTED_MODULE_4__.ElkNode();
            // let size = activeNode.size
            let bounds = mergeBounds(selected);
            let size = {
                width: 0,
                height: 0,
            };
            elkNode.id = selected[0].id + '_entropy';
            elkNode.type = 'node:widget';
            elkNode.position = sprotty_protocol__WEBPACK_IMPORTED_MODULE_0__.Bounds.combine(bounds, { x: bounds.width, y: 0 });
            elkNode.size = size;
            elkNode.properties = {
                shape: {
                    use: overlay_widget.model_id,
                },
            };
            let jlsw = {
                vnode: undefined,
                node: elkNode,
                widget: overlay_widget.model_id,
                visible: true,
                html: undefined,
            };
            let vnode = this.widgetContainer(jlsw, args, false);
            if (vnode != null) {
                vnodes.push(vnode);
            }
        }
        return vnodes;
    }
    /**
     * Method iterate over the JupyterLab widgets and render the VNodes
     */
    renderJLNodeWidgets(args) {
        let vnodes = [];
        for (let key in this.widgets) {
            let jlsw = this.widgets[key];
            let vnode = this.widgetContainer(jlsw, args);
            if (vnode != null) {
                this.decorate(vnode, jlsw.node);
                vnodes.push(vnode);
            }
        }
        return vnodes;
    }
    /**
     * Sprotty Container for a JupyterLab widget
     */
    widgetContainer(jlsw, args, setBounds = true) {
        if (!jlsw.visible) {
            return;
        }
        let position = getPosition(jlsw.node);
        let style = {
            transform: `translate(${position.x}px, ${position.y}px)`,
            // background: '#9dd8d857'
        };
        // Specify Node Bounds
        if (setBounds) {
            let bounds = jlsw.node.bounds;
            if (!bounds) {
                bounds = (0,sprotty__WEBPACK_IMPORTED_MODULE_1__.getAbsoluteBounds)(jlsw.node);
            }
            style['width'] = `${bounds.width}px`;
            style['height'] = `${bounds.height}px`;
        }
        let props = {};
        if (jlsw.html) {
            props = { innerHTML: jlsw.html };
        }
        return (0,sprotty__WEBPACK_IMPORTED_MODULE_1__.html)('div', {
            key: jlsw.node.id,
            class: {
                elkcontainer: true,
            },
            style: style,
            props: props,
            hook: {
                insert: (vnode) => this.renderContent(vnode, jlsw),
            },
        });
    }
    /**
     * Attaching JupyterLab widget to sprotty container
     */
    async renderContent(vnode, jlsw, args) {
        var _a;
        if ((0,sprotty_protocol__WEBPACK_IMPORTED_MODULE_0__.getSubType)(jlsw.node) == 'widget') {
            let widget = jlsw.widget;
            let widget_model;
            if (typeof widget === 'string' || widget instanceof String) {
                widget_model = await this.source.widget_manager.get_model(widget);
            }
            else {
                widget_model = widget;
            }
            let view = await this.source.widget_manager.create_view(widget_model, {});
            let delay = ((_a = jlsw.node.properties.shape) === null || _a === void 0 ? void 0 : _a.delay) || 0;
            if (delay) {
                // initially render jl widget at "full" size. Then after questionable
                // timeout... scale widget to fit inside the elk node.
                let zoom = this.source.root['zoom'] || 1;
                let el = view.luminoWidget.node;
                el.style.transform = `scale(${1 / zoom})`;
                el.style.transformOrigin = `top left`;
                setTimeout(() => {
                    el.style.transform = '';
                }, delay);
            }
            _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__.Widget.attach(view.luminoWidget, vnode.elm);
        }
    }
    /**
     * Registration function for a particular sprotty element id as being needing
     * to be added to the overlay
     */
    async registerJLWidgetNode(vnode, node, visible) {
        this.widgets[node.id] = await this.wrapJLWidget(vnode, node, visible);
    }
    async wrapJLWidget(vnode, node, visible) {
        var _a, _b;
        let widget, html;
        let id = (_b = (_a = node.properties) === null || _a === void 0 ? void 0 : _a.shape) === null || _b === void 0 ? void 0 : _b.use;
        if ((0,sprotty_protocol__WEBPACK_IMPORTED_MODULE_0__.getSubType)(node) == 'widget') {
            if (id) {
                widget = await this.source.widget_manager.get_model(id);
                html = undefined;
            }
        }
        else {
            widget = undefined;
            html = id;
        }
        return {
            vnode: vnode,
            node: node,
            widget: widget,
            visible: visible,
            html: html,
        };
    }
    getConnector(id) {
        var _a;
        let connector = (_a = this.source.elkToSprotty) === null || _a === void 0 ? void 0 : _a.connectors[id];
        return connector;
    }
    hrefID(id) {
        if (id) {
            return this.source.elkToSprotty.symbolsIds[id];
        }
    }
    renderChildren(element, args) {
        const context = args
            ? new ElkModelRenderer(this.viewRegistry, this.targetKind, this['postprocessors'], // postprocessors is private to the parent class
            this.source, Object.assign(Object.assign({}, args), { parentArgs: this.args }))
            : this;
        return element.children
            .map((child) => context.renderElement(child))
            .filter((vnode) => vnode != null);
    }
}
function getPosition(element) {
    var _a, _b;
    let x = 0;
    let y = 0;
    while (element != null) {
        x = x + (((_a = element.bounds) === null || _a === void 0 ? void 0 : _a.x) || 0);
        y = y + (((_b = element.bounds) === null || _b === void 0 ? void 0 : _b.y) || 0);
        element = element === null || element === void 0 ? void 0 : element.parent;
    }
    return {
        x: x,
        y: y,
    };
}
class SSymbolModelFactory extends sprotty__WEBPACK_IMPORTED_MODULE_1__.SModelFactory {
    initializeRoot(root, schema) {
        root = super.initializeRoot(root, schema);
        if (root === null || root === void 0 ? void 0 : root.symbols) {
            root.symbols.children = schema.symbols.children.map((childSchema) => this.createElement(childSchema, root));
        }
        // TODO is there a better way to get a handle to the active `SModelRoot`?
        this.root = root;
        return root;
    }
}
/*
 * Merge Bounds of SModelElements
 */
function mergeBounds(elements) {
    let [minLeft, minBottom, maxRight, maxTop] = extents(elements[0]);
    elements.splice(1, elements.length).forEach((element) => {
        let [left, bottom, right, top] = extents(element);
        if (left < minLeft)
            minLeft = left;
        if (bottom > minBottom)
            minBottom = bottom;
        if (right > maxRight)
            maxRight = right;
        if (top < maxTop)
            maxTop = top;
    });
    let bounds = {
        x: minLeft,
        y: maxTop,
        height: minBottom - maxTop,
        width: maxRight - minLeft,
    };
    return bounds;
}
/*
 * Get SModelElement absolute bounds
 */
function extents(element) {
    let bounds = (0,sprotty__WEBPACK_IMPORTED_MODULE_1__.getAbsoluteBounds)(element);
    let left = bounds.x;
    let top = bounds.y;
    let right = bounds.x + bounds.width;
    let bottom = bounds.y + bounds.height;
    return [left, bottom, right, top];
}


/***/ }),

/***/ "./lib/sprotty/sprotty-model.js":
/*!**************************************!*\
  !*** ./lib/sprotty/sprotty-model.js ***!
  \**************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   ElkEdge: () => (/* binding */ ElkEdge),
/* harmony export */   ElkJunction: () => (/* binding */ ElkJunction),
/* harmony export */   ElkLabel: () => (/* binding */ ElkLabel),
/* harmony export */   ElkNode: () => (/* binding */ ElkNode),
/* harmony export */   ElkPort: () => (/* binding */ ElkPort),
/* harmony export */   SymbolNode: () => (/* binding */ SymbolNode)
/* harmony export */ });
/* harmony import */ var sprotty__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! sprotty */ "webpack/sharing/consume/default/sprotty/sprotty");
/* harmony import */ var sprotty__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(sprotty__WEBPACK_IMPORTED_MODULE_0__);
/**
 * # Copyright (c) 2024 ipyelk contributors.
 * Distributed under the terms of the Modified BSD License.
 */
// From https://github.com/OpenKieler/elkgraph-web

class ElkNode extends sprotty__WEBPACK_IMPORTED_MODULE_0__.RectangularNode {
    hasFeature(feature) {
        if (feature === sprotty__WEBPACK_IMPORTED_MODULE_0__.moveFeature)
            return false;
        else
            return super.hasFeature(feature);
    }
}
class ElkPort extends sprotty__WEBPACK_IMPORTED_MODULE_0__.RectangularPort {
    hasFeature(feature) {
        if (feature === sprotty__WEBPACK_IMPORTED_MODULE_0__.moveFeature)
            return false;
        else
            return super.hasFeature(feature);
    }
}
class ElkEdge extends sprotty__WEBPACK_IMPORTED_MODULE_0__.SEdgeImpl {
    hasFeature(feature) {
        if (feature === sprotty__WEBPACK_IMPORTED_MODULE_0__.editFeature)
            return false;
        else
            return super.hasFeature(feature);
    }
}
class ElkJunction extends sprotty__WEBPACK_IMPORTED_MODULE_0__.SNodeImpl {
    hasFeature(feature) {
        if (feature === sprotty__WEBPACK_IMPORTED_MODULE_0__.moveFeature ||
            feature === sprotty__WEBPACK_IMPORTED_MODULE_0__.selectFeature ||
            feature === sprotty__WEBPACK_IMPORTED_MODULE_0__.hoverFeedbackFeature)
            return false;
        else
            return super.hasFeature(feature);
    }
}
class ElkLabel extends sprotty__WEBPACK_IMPORTED_MODULE_0__.SLabelImpl {
    constructor() {
        super(...arguments);
        this.selected = false;
        this.hoverFeedback = false;
    }
    hasFeature(feature) {
        var _a;
        if (feature === sprotty__WEBPACK_IMPORTED_MODULE_0__.selectFeature || feature === sprotty__WEBPACK_IMPORTED_MODULE_0__.hoverFeedbackFeature) {
            if (((_a = this.properties) === null || _a === void 0 ? void 0 : _a.selectable) === true) {
                return true;
            }
        }
        else
            return super.hasFeature(feature);
    }
}
ElkLabel.DEFAULT_FEATURES = [
    sprotty__WEBPACK_IMPORTED_MODULE_0__.selectFeature,
    sprotty__WEBPACK_IMPORTED_MODULE_0__.hoverFeedbackFeature,
    sprotty__WEBPACK_IMPORTED_MODULE_0__.boundsFeature,
    sprotty__WEBPACK_IMPORTED_MODULE_0__.alignFeature,
    sprotty__WEBPACK_IMPORTED_MODULE_0__.layoutableChildFeature,
    sprotty__WEBPACK_IMPORTED_MODULE_0__.edgeLayoutFeature,
    sprotty__WEBPACK_IMPORTED_MODULE_0__.fadeFeature,
];
class SymbolNode extends sprotty__WEBPACK_IMPORTED_MODULE_0__.SNodeImpl {
    hasFeature(feature) {
        if (feature === sprotty__WEBPACK_IMPORTED_MODULE_0__.moveFeature)
            return false;
        else
            return super.hasFeature(feature);
    }
}


/***/ }),

/***/ "./lib/sprotty/update/index.js":
/*!*************************************!*\
  !*** ./lib/sprotty/update/index.js ***!
  \*************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var inversify__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! inversify */ "webpack/sharing/consume/default/inversify/inversify");
/* harmony import */ var inversify__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(inversify__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var sprotty__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! sprotty */ "webpack/sharing/consume/default/sprotty/sprotty");
/* harmony import */ var sprotty__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(sprotty__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _update_model__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./update-model */ "./lib/sprotty/update/update-model.js");
/**
 * # Copyright (c) 2024 ipyelk contributors.
 * Distributed under the terms of the Modified BSD License.
 * FIX BELOW FROM:
 * back porting to fix duplicate ids
 * https://github.com/eclipse/sprotty/pull/209/files
 * remove after next sprotty release > 0.9
 */



const updateModule = new inversify__WEBPACK_IMPORTED_MODULE_0__.ContainerModule((bind, _unbind, isBound) => {
    (0,sprotty__WEBPACK_IMPORTED_MODULE_1__.configureCommand)({ bind, isBound }, _update_model__WEBPACK_IMPORTED_MODULE_2__.UpdateModelCommand2);
});
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (updateModule);


/***/ }),

/***/ "./lib/sprotty/update/smodel-utils.js":
/*!********************************************!*\
  !*** ./lib/sprotty/update/smodel-utils.js ***!
  \********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   containsSome: () => (/* binding */ containsSome)
/* harmony export */ });
/**
 * Tests if the given model contains an id of then given element or one of its descendants.
 */
function containsSome(root, element) {
    const test = (element) => root.index.getById(element.id) != null;
    const find = (elements) => elements.some((element) => test(element) || find(element.children));
    return find([element]);
}


/***/ }),

/***/ "./lib/sprotty/update/update-model.js":
/*!********************************************!*\
  !*** ./lib/sprotty/update/update-model.js ***!
  \********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   UpdateModelCommand2: () => (/* binding */ UpdateModelCommand2)
/* harmony export */ });
/* harmony import */ var inversify__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! inversify */ "webpack/sharing/consume/default/inversify/inversify");
/* harmony import */ var inversify__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(inversify__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var sprotty__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! sprotty */ "webpack/sharing/consume/default/sprotty/sprotty");
/* harmony import */ var sprotty__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(sprotty__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _smodel_utils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./smodel-utils */ "./lib/sprotty/update/smodel-utils.js");
/**
 * # Copyright (c) 2024 ipyelk contributors.
 * Distributed under the terms of the Modified BSD License.
 * FIX BELOW FROM:
 */
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
/********************************************************************************
 * Copyright (c) 2017-2020 TypeFox and others.
 *
 * This program and the accompanying materials are made available under the
 * terms of the Eclipse Public License v. 2.0 which is available at
 * http://www.eclipse.org/legal/epl-2.0.
 *
 * This Source Code may also be made available under the following Secondary
 * Licenses when the conditions for such availability set forth in the Eclipse
 * Public License v. 2.0 are satisfied: GNU General Public License, version 2
 * with the GNU Classpath Exception which is available at
 * https://www.gnu.org/software/classpath/license.html.
 *
 * SPDX-License-Identifier: EPL-2.0 OR GPL-2.0 WITH Classpath-exception-2.0
 ********************************************************************************/




let UpdateModelCommand2 = class UpdateModelCommand2 extends sprotty__WEBPACK_IMPORTED_MODULE_1__.UpdateModelCommand {
    computeAnimation(newRoot, matchResult, context) {
        const animationData = {
            fades: [],
        };
        (0,sprotty__WEBPACK_IMPORTED_MODULE_1__.forEachMatch)(matchResult, (id, match) => {
            if (match.left != null && match.right != null) {
                // The element is still there, but may have been moved
                this.updateElement(match.left, match.right, animationData);
            }
            else if (match.right != null) {
                // An element has been added
                const right = match.right;
                if ((0,sprotty__WEBPACK_IMPORTED_MODULE_1__.isFadeable)(right)) {
                    right.opacity = 0;
                    animationData.fades.push({
                        element: right,
                        type: 'in',
                    });
                }
            }
            else if (match.left instanceof sprotty__WEBPACK_IMPORTED_MODULE_1__.SChildElementImpl) {
                // An element has been removed
                const left = match.left;
                if ((0,sprotty__WEBPACK_IMPORTED_MODULE_1__.isFadeable)(left) && match.leftParentId != null) {
                    if (!(0,_smodel_utils__WEBPACK_IMPORTED_MODULE_2__.containsSome)(newRoot, left)) {
                        const parent = newRoot.index.getById(match.leftParentId);
                        if (parent instanceof sprotty__WEBPACK_IMPORTED_MODULE_1__.SParentElementImpl) {
                            const leftCopy = context.modelFactory.createElement(left);
                            parent.add(leftCopy);
                            animationData.fades.push({
                                element: leftCopy,
                                type: 'out',
                            });
                        }
                    }
                }
            }
        });
        const animations = this.createAnimations(animationData, newRoot, context);
        if (animations.length >= 2) {
            return new sprotty__WEBPACK_IMPORTED_MODULE_1__.CompoundAnimation(newRoot, context, animations);
        }
        else if (animations.length === 1) {
            return animations[0];
        }
        else {
            return newRoot;
        }
    }
};
UpdateModelCommand2 = __decorate([
    (0,inversify__WEBPACK_IMPORTED_MODULE_0__.injectable)()
], UpdateModelCommand2);



/***/ }),

/***/ "./lib/sprotty/viewportModule.js":
/*!***************************************!*\
  !*** ./lib/sprotty/viewportModule.js ***!
  \***************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   CenterCommand: () => (/* binding */ CenterCommand),
/* harmony export */   FitToScreenCommand: () => (/* binding */ FitToScreenCommand),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var inversify__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! inversify */ "webpack/sharing/consume/default/inversify/inversify");
/* harmony import */ var inversify__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(inversify__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var sprotty_protocol__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! sprotty-protocol */ "webpack/sharing/consume/default/sprotty-protocol/sprotty-protocol");
/* harmony import */ var sprotty_protocol__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(sprotty_protocol__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var sprotty__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! sprotty */ "webpack/sharing/consume/default/sprotty/sprotty");
/* harmony import */ var sprotty__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(sprotty__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _diagram_server__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./diagram-server */ "./lib/sprotty/diagram-server.js");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (undefined && undefined.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
var __param = (undefined && undefined.__param) || function (paramIndex, decorator) {
    return function (target, key) { decorator(target, key, paramIndex); }
};
/**
 * # Copyright (c) 2024 ipyelk contributors.
 * Distributed under the terms of the Modified BSD License.
 */





let ModScrollMouseListener = class ModScrollMouseListener extends sprotty__WEBPACK_IMPORTED_MODULE_2__.ScrollMouseListener {
    /*
      Made this modified class for the scoll mouse listener to help with the inital skip on a scroll event but unable to pin down the error
      */
    constructor(model_source) {
        super();
        this.model_source = model_source;
    }
    mouseDown(target, event) {
        const moveable = (0,sprotty__WEBPACK_IMPORTED_MODULE_2__.findParentByFeature)(target, sprotty__WEBPACK_IMPORTED_MODULE_2__.isMoveable);
        if (moveable == null && !(target instanceof sprotty__WEBPACK_IMPORTED_MODULE_2__.SRoutingHandleImpl)) {
            if (target.type == 'node:widget') {
                // disable scrolling if mouse down on a widget node.
                this.lastScrollPosition = undefined;
            }
            else {
                const viewport = (0,sprotty__WEBPACK_IMPORTED_MODULE_2__.findParentByFeature)(target, sprotty__WEBPACK_IMPORTED_MODULE_2__.isViewport);
                if (viewport) {
                    this.lastScrollPosition = {
                        x: event.pageX,
                        y: event.pageY,
                    };
                }
                else {
                    this.lastScrollPosition = undefined;
                }
            }
        }
        return [];
    }
    mouseMove(target, event) {
        if (event.buttons === 0)
            this.mouseUp(target, event);
        else if (this.lastScrollPosition) {
            const viewport = (0,sprotty__WEBPACK_IMPORTED_MODULE_2__.findParentByFeature)(target, sprotty__WEBPACK_IMPORTED_MODULE_2__.isViewport);
            if (viewport) {
                const dx = (event.pageX - this.lastScrollPosition.x) / viewport.zoom;
                const dy = (event.pageY - this.lastScrollPosition.y) / viewport.zoom;
                // const windowScroll = this.model_source.element().getBoundingClientRect()
                const newViewport = {
                    scroll: {
                        x: viewport.scroll.x - dx,
                        y: viewport.scroll.y - dy,
                    },
                    zoom: viewport.zoom,
                };
                this.lastScrollPosition = { x: event.pageX, y: event.pageY };
                return [sprotty_protocol__WEBPACK_IMPORTED_MODULE_1__.SetViewportAction.create(viewport.id, newViewport, { animate: false })];
            }
        }
        return [];
    }
};
ModScrollMouseListener = __decorate([
    __param(0, (0,inversify__WEBPACK_IMPORTED_MODULE_0__.inject)(sprotty__WEBPACK_IMPORTED_MODULE_2__.TYPES.ModelSource)),
    __metadata("design:paramtypes", [_diagram_server__WEBPACK_IMPORTED_MODULE_3__.JLModelSource])
], ModScrollMouseListener);
let ModZoomMouseListener = class ModZoomMouseListener extends sprotty__WEBPACK_IMPORTED_MODULE_2__.ZoomMouseListener {
    /* Modified Zoom Muse Listener to use the base element bounding rectangle for referencing zoom events
     */
    constructor(model_source) {
        super();
        this.model_source = model_source;
    }
    getViewportOffset(root, event) {
        const windowScroll = this.model_source.element().getBoundingClientRect();
        const offset = {
            x: event.clientX - windowScroll.left,
            y: event.clientY - windowScroll.top,
        };
        return offset;
    }
};
ModZoomMouseListener = __decorate([
    __param(0, (0,inversify__WEBPACK_IMPORTED_MODULE_0__.inject)(sprotty__WEBPACK_IMPORTED_MODULE_2__.TYPES.ModelSource)),
    __metadata("design:paramtypes", [_diagram_server__WEBPACK_IMPORTED_MODULE_3__.JLModelSource])
], ModZoomMouseListener);
let CenterCommand = class CenterCommand extends sprotty__WEBPACK_IMPORTED_MODULE_2__.BoundsAwareViewportCommand {
    constructor(action) {
        super(action.animate);
        this.action = action;
    }
    getElementIds() {
        return this.action.elementIds;
    }
    getNewViewport(bounds, model) {
        if (!sprotty_protocol__WEBPACK_IMPORTED_MODULE_1__.Dimension.isValid(model.canvasBounds)) {
            return void 0;
        }
        let zoom = 1;
        if (this.action.retainZoom && (0,sprotty__WEBPACK_IMPORTED_MODULE_2__.isViewport)(model)) {
            zoom = model.zoom;
        }
        else if (this.action.zoomScale) {
            zoom = this.action.zoomScale;
        }
        const c = sprotty_protocol__WEBPACK_IMPORTED_MODULE_1__.Bounds.center(bounds);
        const x = c.x - (0.5 * model.canvasBounds.width) / zoom;
        const y = c.y - (0.5 * model.canvasBounds.height) / zoom;
        return {
            scroll: {
                x: x ? x : 0,
                y: y ? y : 0,
            },
            zoom: zoom,
        };
    }
};
CenterCommand.KIND = sprotty_protocol__WEBPACK_IMPORTED_MODULE_1__.CenterAction.KIND;
CenterCommand = __decorate([
    __param(0, (0,inversify__WEBPACK_IMPORTED_MODULE_0__.inject)(sprotty__WEBPACK_IMPORTED_MODULE_2__.TYPES.Action)),
    __metadata("design:paramtypes", [Object])
], CenterCommand);

let FitToScreenCommand = class FitToScreenCommand extends sprotty__WEBPACK_IMPORTED_MODULE_2__.BoundsAwareViewportCommand {
    constructor(action) {
        super(action.animate);
        this.action = action;
    }
    getElementIds() {
        return this.action.elementIds;
    }
    getNewViewport(bounds, model) {
        if (!sprotty_protocol__WEBPACK_IMPORTED_MODULE_1__.Dimension.isValid(model.canvasBounds)) {
            return void 0;
        }
        const c = sprotty_protocol__WEBPACK_IMPORTED_MODULE_1__.Bounds.center(bounds);
        const delta = this.action.padding == null ? 0 : 2 * this.action.padding;
        let zoom = Math.min(model.canvasBounds.width / (bounds.width + delta), model.canvasBounds.height / (bounds.height + delta));
        if (this.action.maxZoom != null)
            zoom = Math.min(zoom, this.action.maxZoom);
        if (zoom === Infinity) {
            zoom = 1;
        }
        const x = c.x - (0.5 * model.canvasBounds.width) / zoom;
        const y = c.y - (0.5 * model.canvasBounds.height) / zoom;
        return {
            scroll: {
                x: x ? x : 0,
                y: y ? y : 0,
            },
            zoom: zoom,
        };
    }
};
FitToScreenCommand.KIND = sprotty_protocol__WEBPACK_IMPORTED_MODULE_1__.FitToScreenAction.KIND;
FitToScreenCommand = __decorate([
    __param(0, (0,inversify__WEBPACK_IMPORTED_MODULE_0__.inject)(sprotty__WEBPACK_IMPORTED_MODULE_2__.TYPES.Action)),
    __metadata("design:paramtypes", [Object])
], FitToScreenCommand);

const viewportModule = new inversify__WEBPACK_IMPORTED_MODULE_0__.ContainerModule((bind, _unbind, isBound) => {
    (0,sprotty__WEBPACK_IMPORTED_MODULE_2__.configureCommand)({ bind, isBound }, CenterCommand);
    (0,sprotty__WEBPACK_IMPORTED_MODULE_2__.configureCommand)({ bind, isBound }, FitToScreenCommand);
    (0,sprotty__WEBPACK_IMPORTED_MODULE_2__.configureCommand)({ bind, isBound }, sprotty__WEBPACK_IMPORTED_MODULE_2__.SetViewportCommand);
    (0,sprotty__WEBPACK_IMPORTED_MODULE_2__.configureCommand)({ bind, isBound }, sprotty__WEBPACK_IMPORTED_MODULE_2__.GetViewportCommand);
    bind(sprotty__WEBPACK_IMPORTED_MODULE_2__.TYPES.KeyListener).to(sprotty__WEBPACK_IMPORTED_MODULE_2__.CenterKeyboardListener);
    bind(sprotty__WEBPACK_IMPORTED_MODULE_2__.TYPES.MouseListener).to(ModScrollMouseListener);
    bind(sprotty__WEBPACK_IMPORTED_MODULE_2__.TYPES.MouseListener).to(ModZoomMouseListener);
});
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (viewportModule);


/***/ }),

/***/ "./lib/sprotty/views/base.js":
/*!***********************************!*\
  !*** ./lib/sprotty/views/base.js ***!
  \***********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   CircularNodeView: () => (/* binding */ CircularNodeView),
/* harmony export */   RectangularNodeView: () => (/* binding */ RectangularNodeView),
/* harmony export */   ShapeView: () => (/* binding */ ShapeView),
/* harmony export */   validCanvasBounds: () => (/* binding */ validCanvasBounds)
/* harmony export */ });
/* harmony import */ var inversify__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! inversify */ "webpack/sharing/consume/default/inversify/inversify");
/* harmony import */ var inversify__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(inversify__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var sprotty_protocol__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! sprotty-protocol */ "webpack/sharing/consume/default/sprotty-protocol/sprotty-protocol");
/* harmony import */ var sprotty_protocol__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(sprotty_protocol__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var sprotty__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! sprotty */ "webpack/sharing/consume/default/sprotty/sprotty");
/* harmony import */ var sprotty__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(sprotty__WEBPACK_IMPORTED_MODULE_2__);
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};



function validCanvasBounds(bounds) {
    return bounds.width == 0 && bounds.height == 0;
}
let ShapeView = class ShapeView {
    /**
     * Check whether the given model element is in the current viewport. Use this method
     * in your `render` implementation to skip rendering in case the element is not visible.
     * This can greatly enhance performance for large models.
     */
    isVisible(model, context) {
        if (context.targetKind === 'hidden') {
            // Don't hide any element for hidden rendering
            return true;
        }
        if (!sprotty_protocol__WEBPACK_IMPORTED_MODULE_1__.Dimension.isValid(model.bounds)) {
            // We should hide only if we know the element's bounds
            return true;
        }
        const canvasBounds = model.root.canvasBounds;
        if (!validCanvasBounds(canvasBounds)) {
            // only hide if the canvas's size is set
            return true;
        }
        const ab = (0,sprotty__WEBPACK_IMPORTED_MODULE_2__.getAbsoluteBounds)(model);
        return (ab.x <= canvasBounds.width &&
            ab.x + ab.width >= 0 &&
            ab.y <= canvasBounds.height &&
            ab.y + ab.height >= 0);
    }
};
ShapeView = __decorate([
    (0,inversify__WEBPACK_IMPORTED_MODULE_0__.injectable)()
], ShapeView);

let CircularNodeView = class CircularNodeView extends ShapeView {
    render(node, context, args) {
        if (!this.isVisible(node, context)) {
            return undefined;
        }
        const radius = this.getRadius(node);
        return ((0,sprotty__WEBPACK_IMPORTED_MODULE_2__.svg)("g", null,
            (0,sprotty__WEBPACK_IMPORTED_MODULE_2__.svg)("circle", { "class-sprotty-node": node instanceof sprotty__WEBPACK_IMPORTED_MODULE_2__.SNodeImpl, "class-sprotty-port": node instanceof sprotty__WEBPACK_IMPORTED_MODULE_2__.SPortImpl, "class-mouseover": node.hoverFeedback, "class-selected": node.selected, r: radius, cx: radius, cy: radius }),
            context.renderChildren(node)));
    }
    getRadius(node) {
        const d = Math.min(node.size.width, node.size.height);
        return d > 0 ? d / 2 : 0;
    }
};
CircularNodeView = __decorate([
    (0,inversify__WEBPACK_IMPORTED_MODULE_0__.injectable)()
], CircularNodeView);

let RectangularNodeView = class RectangularNodeView extends ShapeView {
    render(node, context, args) {
        if (!this.isVisible(node, context)) {
            return undefined;
        }
        return ((0,sprotty__WEBPACK_IMPORTED_MODULE_2__.svg)("g", null,
            (0,sprotty__WEBPACK_IMPORTED_MODULE_2__.svg)("rect", { "class-sprotty-node": node instanceof sprotty__WEBPACK_IMPORTED_MODULE_2__.SNodeImpl, "class-sprotty-port": node instanceof sprotty__WEBPACK_IMPORTED_MODULE_2__.SPortImpl, "class-mouseover": node.hoverFeedback, "class-selected": node.selected, x: "0", y: "0", width: Math.max(node.size.width, 0), height: Math.max(node.size.height, 0) }),
            context.renderChildren(node)));
    }
};
RectangularNodeView = __decorate([
    (0,inversify__WEBPACK_IMPORTED_MODULE_0__.injectable)()
], RectangularNodeView);



/***/ }),

/***/ "./lib/sprotty/views/edge_views.js":
/*!*****************************************!*\
  !*** ./lib/sprotty/views/edge_views.js ***!
  \*****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   ElkEdgeView: () => (/* binding */ ElkEdgeView),
/* harmony export */   JunctionView: () => (/* binding */ JunctionView),
/* harmony export */   angle: () => (/* binding */ angle)
/* harmony export */ });
/* harmony import */ var inversify__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! inversify */ "webpack/sharing/consume/default/inversify/inversify");
/* harmony import */ var inversify__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(inversify__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var sprotty_protocol__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! sprotty-protocol */ "webpack/sharing/consume/default/sprotty-protocol/sprotty-protocol");
/* harmony import */ var sprotty_protocol__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(sprotty_protocol__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var sprotty__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! sprotty */ "webpack/sharing/consume/default/sprotty/sprotty");
/* harmony import */ var sprotty__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(sprotty__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _base__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./base */ "./lib/sprotty/views/base.js");
/**
 * Copyright (c) 2021 Dane Freeman.
 * Distributed under the terms of the Modified BSD License.
 */
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};




let JunctionView = class JunctionView extends _base__WEBPACK_IMPORTED_MODULE_3__.CircularNodeView {
    render(node, context) {
        const radius = this.getRadius(node);
        return ((0,sprotty__WEBPACK_IMPORTED_MODULE_2__.svg)("g", null,
            (0,sprotty__WEBPACK_IMPORTED_MODULE_2__.svg)("circle", { "class-elkjunction": true, r: radius })));
    }
    getRadius(node) {
        return 2;
    }
};
JunctionView = __decorate([
    (0,inversify__WEBPACK_IMPORTED_MODULE_0__.injectable)()
], JunctionView);

let ElkEdgeView = class ElkEdgeView extends sprotty__WEBPACK_IMPORTED_MODULE_2__.PolylineEdgeView {
    isVisible(model, route, context) {
        if (context.targetKind === 'hidden') {
            // Don't hide any element for hidden rendering
            return true;
        }
        if (route.length === 0) {
            // We should hide only if we know the element's route
            return true;
        }
        const canvasBounds = model.root.canvasBounds;
        if (!(0,_base__WEBPACK_IMPORTED_MODULE_3__.validCanvasBounds)(canvasBounds)) {
            // only hide if the canvas's size is set
            return true;
        }
        const ab = (0,sprotty__WEBPACK_IMPORTED_MODULE_2__.getAbsoluteRouteBounds)(model, route);
        return (ab.x <= canvasBounds.width &&
            ab.x + ab.width >= 0 &&
            ab.y <= canvasBounds.height &&
            ab.y + ab.height >= 0);
    }
    render(edge, context) {
        const router = this.edgeRouterRegistry.get(edge.routerKind);
        const route = router.route(edge);
        if (route.length === 0) {
            return this.renderDanglingEdge('Cannot compute route', edge, context);
        }
        if (!this.isVisible(edge, route, context)) {
            if (edge.children.length === 0) {
                return undefined;
            }
            // The children of an edge are not necessarily inside the bounding box of the route,
            // so we need to render a group to ensure the children have a chance to be rendered.
            return (0,sprotty__WEBPACK_IMPORTED_MODULE_2__.svg)("g", null, context.renderChildren(edge, { route }));
        }
        return ((0,sprotty__WEBPACK_IMPORTED_MODULE_2__.svg)("g", { "class-elkedge": true, "class-mouseover": edge.hoverFeedback },
            this.renderLine(edge, route, context),
            this.renderAdditionals(edge, route, context),
            context.renderChildren(edge, { route })));
    }
    renderLine(edge, segments, context) {
        var _a, _b, _c, _d;
        const p1_s = segments[1];
        const p2_s = segments[0];
        let r = (0,sprotty_protocol__WEBPACK_IMPORTED_MODULE_1__.angleOfPoint)({ x: p1_s.x - p2_s.x, y: p1_s.y - p2_s.y });
        const p1_e = segments[segments.length - 2];
        const p2_e = segments[segments.length - 1];
        let r2 = (0,sprotty_protocol__WEBPACK_IMPORTED_MODULE_1__.angleOfPoint)({ x: p1_e.x - p2_e.x, y: p1_e.y - p2_e.y });
        let start = this.getPathOffset((_b = (_a = edge === null || edge === void 0 ? void 0 : edge.properties) === null || _a === void 0 ? void 0 : _a.shape) === null || _b === void 0 ? void 0 : _b.start, context, r);
        let end = this.getPathOffset((_d = (_c = edge === null || edge === void 0 ? void 0 : edge.properties) === null || _c === void 0 ? void 0 : _c.shape) === null || _d === void 0 ? void 0 : _d.end, context, r2);
        const firstPoint = segments[0];
        let path = `M ${firstPoint.x - start.x},${firstPoint.y - start.y}`;
        for (let i = 1; i < segments.length - 1; i++) {
            const p = segments[i];
            path += ` L ${p.x},${p.y}`;
        }
        const lastPoint = segments[segments.length - 1];
        path += ` L ${lastPoint.x - end.x}, ${lastPoint.y - end.y}`;
        return (0,sprotty__WEBPACK_IMPORTED_MODULE_2__.svg)("path", { d: path });
    }
    getAnchorOffset(id, context, r) {
        let connection = context.getConnector(id);
        if (connection === null || connection === void 0 ? void 0 : connection.symbol_offset) {
            const p = connection.symbol_offset;
            return {
                x: p.x * Math.cos(r) - p.y * Math.sin(r),
                y: p.x * Math.sin(r) + p.y * Math.cos(r),
            };
        }
        return { x: 0, y: 0 };
    }
    getPathOffset(id, context, r) {
        let connection = context.getConnector(id);
        if (connection === null || connection === void 0 ? void 0 : connection.path_offset) {
            const p = connection.path_offset;
            return {
                x: p.x * Math.cos(r) - p.y * Math.sin(r),
                y: p.x * Math.sin(r) + p.y * Math.cos(r),
            };
        }
        return { x: 0, y: 0 };
    }
    renderAdditionals(edge, segments, context) {
        var _a, _b, _c, _d;
        let connectors = [];
        let href;
        let correction;
        let vnode;
        let start = (_b = (_a = edge === null || edge === void 0 ? void 0 : edge.properties) === null || _a === void 0 ? void 0 : _a.shape) === null || _b === void 0 ? void 0 : _b.start;
        let end = (_d = (_c = edge === null || edge === void 0 ? void 0 : edge.properties) === null || _c === void 0 ? void 0 : _c.shape) === null || _d === void 0 ? void 0 : _d.end;
        if (start) {
            const p1 = segments[1];
            const p2 = segments[0];
            let r = (0,sprotty_protocol__WEBPACK_IMPORTED_MODULE_1__.angleOfPoint)({ x: p1.x - p2.x, y: p1.y - p2.y });
            correction = this.getAnchorOffset(start, context, r);
            let x = p2.x - correction.x;
            let y = p2.y - correction.y;
            href = context.hrefID(start);
            vnode = ((0,sprotty__WEBPACK_IMPORTED_MODULE_2__.svg)("use", { href: '#' + href, "class-elkedge-start": true, "class-elkarrow": true, transform: `rotate(${(0,sprotty_protocol__WEBPACK_IMPORTED_MODULE_1__.toDegrees)(r)} ${x} ${y}) translate(${x} ${y})` }));
            (0,sprotty__WEBPACK_IMPORTED_MODULE_2__.setClass)(vnode, start, true);
            connectors.push(vnode);
        }
        if (end) {
            const p1 = segments[segments.length - 2];
            const p2 = segments[segments.length - 1];
            let r = (0,sprotty_protocol__WEBPACK_IMPORTED_MODULE_1__.angleOfPoint)({ x: p1.x - p2.x, y: p1.y - p2.y });
            correction = this.getAnchorOffset(end, context, r);
            let x = p2.x - correction.x;
            let y = p2.y - correction.y;
            href = context.hrefID(end);
            vnode = ((0,sprotty__WEBPACK_IMPORTED_MODULE_2__.svg)("use", { href: '#' + href, "class-elkedge-end": true, "class-elkarrow": true, transform: `rotate(${(0,sprotty_protocol__WEBPACK_IMPORTED_MODULE_1__.toDegrees)(r)} ${x} ${y}) translate(${x} ${y})` }));
            (0,sprotty__WEBPACK_IMPORTED_MODULE_2__.setClass)(vnode, end, true);
            connectors.push(vnode);
        }
        return connectors;
    }
};
ElkEdgeView = __decorate([
    (0,inversify__WEBPACK_IMPORTED_MODULE_0__.injectable)()
], ElkEdgeView);

function angle(x0, x1) {
    return (0,sprotty_protocol__WEBPACK_IMPORTED_MODULE_1__.toDegrees)(Math.atan2(x1.y - x0.y, x1.x - x0.x));
}


/***/ }),

/***/ "./lib/sprotty/views/graph_views.js":
/*!******************************************!*\
  !*** ./lib/sprotty/views/graph_views.js ***!
  \******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   SGraphView: () => (/* binding */ SGraphView)
/* harmony export */ });
/* harmony import */ var inversify__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! inversify */ "webpack/sharing/consume/default/inversify/inversify");
/* harmony import */ var inversify__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(inversify__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var sprotty__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! sprotty */ "webpack/sharing/consume/default/sprotty/sprotty");
/* harmony import */ var sprotty__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(sprotty__WEBPACK_IMPORTED_MODULE_1__);
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};


class SSymbolGraph extends sprotty__WEBPACK_IMPORTED_MODULE_1__.SGraphImpl {
}
/**
 * IView component that turns an SGraph element and its children into a tree of virtual DOM elements.
 */
let SGraphView = class SGraphView {
    render(model, context) {
        const x = model.scroll.x ? model.scroll.x : 0;
        const y = model.scroll.y ? model.scroll.y : 0;
        const transform = `scale(${model.zoom}) translate(${-x},${-y})`;
        let graph = (0,sprotty__WEBPACK_IMPORTED_MODULE_1__.svg)('svg', { class: { 'sprotty-graph': true } }, (0,sprotty__WEBPACK_IMPORTED_MODULE_1__.svg)('g', { transform: transform }, ...context.renderChildren(model)), (0,sprotty__WEBPACK_IMPORTED_MODULE_1__.svg)('g', { class: { elksymbols: true } }, ...context.renderChildren(model.symbols)));
        const css_transform = {
            transform: `scale(${model.zoom}) translateZ(0) translate(${-model.scroll
                .x}px,${-model.scroll.y}px)`,
        };
        let overlay = ((0,sprotty__WEBPACK_IMPORTED_MODULE_1__.html)("div", { "class-sprotty-overlay": true, style: css_transform }, context.renderJLNodeWidgets()));
        let element = ((0,sprotty__WEBPACK_IMPORTED_MODULE_1__.html)("div", { "class-sprotty-root": true },
            (0,sprotty__WEBPACK_IMPORTED_MODULE_1__.html)("div", { "class-sprotty-overlay": true }, context.renderJLOverlayControl()),
            graph,
            overlay));
        return element;
    }
};
SGraphView = __decorate([
    (0,inversify__WEBPACK_IMPORTED_MODULE_0__.injectable)()
], SGraphView);



/***/ }),

/***/ "./lib/sprotty/views/node_views.js":
/*!*****************************************!*\
  !*** ./lib/sprotty/views/node_views.js ***!
  \*****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   ElkCommentNodeView: () => (/* binding */ ElkCommentNodeView),
/* harmony export */   ElkCompartmentNodeView: () => (/* binding */ ElkCompartmentNodeView),
/* harmony export */   ElkDiamondNodeView: () => (/* binding */ ElkDiamondNodeView),
/* harmony export */   ElkForeignObjectNodeView: () => (/* binding */ ElkForeignObjectNodeView),
/* harmony export */   ElkImageNodeView: () => (/* binding */ ElkImageNodeView),
/* harmony export */   ElkJLNodeView: () => (/* binding */ ElkJLNodeView),
/* harmony export */   ElkLabelView: () => (/* binding */ ElkLabelView),
/* harmony export */   ElkNodeView: () => (/* binding */ ElkNodeView),
/* harmony export */   ElkPathNodeView: () => (/* binding */ ElkPathNodeView),
/* harmony export */   ElkPortView: () => (/* binding */ ElkPortView),
/* harmony export */   ElkRoundNodeView: () => (/* binding */ ElkRoundNodeView),
/* harmony export */   ElkSVGNodeView: () => (/* binding */ ElkSVGNodeView),
/* harmony export */   ElkUseNodeView: () => (/* binding */ ElkUseNodeView)
/* harmony export */ });
/* harmony import */ var inversify__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! inversify */ "webpack/sharing/consume/default/inversify/inversify");
/* harmony import */ var inversify__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(inversify__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var sprotty__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! sprotty */ "webpack/sharing/consume/default/sprotty/sprotty");
/* harmony import */ var sprotty__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(sprotty__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./base */ "./lib/sprotty/views/base.js");
/**
 * Copyright (c) 2021 Dane Freeman.
 * Distributed under the terms of the Modified BSD License.
 */
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};



function svgStr(point) {
    return `${point.x},${point.y}`;
}
let ElkNodeView = class ElkNodeView extends _base__WEBPACK_IMPORTED_MODULE_2__.RectangularNodeView {
    render(node, context) {
        if (!this.isSymbol(node) && !this.isVisible(node, context)) {
            return;
        }
        let mark = this.renderMark(node, context);
        if (!this.isSymbol(node)) {
            // skip marking extra classes on symbol nodes
            (0,sprotty__WEBPACK_IMPORTED_MODULE_1__.setClass)(mark, 'elknode', true);
            (0,sprotty__WEBPACK_IMPORTED_MODULE_1__.setClass)(mark, 'mouseover', node.hoverFeedback);
            (0,sprotty__WEBPACK_IMPORTED_MODULE_1__.setClass)(mark, 'selected', node.selected);
        }
        (0,sprotty__WEBPACK_IMPORTED_MODULE_1__.setClass)(mark, node.type.replace(':', '-'), true);
        return ((0,sprotty__WEBPACK_IMPORTED_MODULE_1__.svg)("g", null,
            mark,
            (0,sprotty__WEBPACK_IMPORTED_MODULE_1__.svg)("g", { "class-elkchildren": true }, this.renderChildren(node, context))));
    }
    renderMark(node, context) {
        let mark = ((0,sprotty__WEBPACK_IMPORTED_MODULE_1__.svg)("rect", { x: "0", y: "0", width: node.size.width, height: node.size.height }));
        return mark;
    }
    renderChildren(node, context) {
        return context.renderChildren(node);
    }
    /**
     *
     * @param node
     */
    isSymbol(node) {
        var _a;
        return ((_a = node === null || node === void 0 ? void 0 : node.properties) === null || _a === void 0 ? void 0 : _a.isSymbol) == true;
    }
};
ElkNodeView = __decorate([
    (0,inversify__WEBPACK_IMPORTED_MODULE_0__.injectable)()
], ElkNodeView);

let ElkDiamondNodeView = class ElkDiamondNodeView extends ElkNodeView {
    renderMark(node, context) {
        let width = node.size.width;
        let height = node.size.height;
        const top = {
            x: width / 2,
            y: 0,
        };
        const right = {
            x: width,
            y: height / 2,
        };
        const left = {
            x: 0,
            y: height / 2,
        };
        const bottom = {
            x: width / 2,
            y: height,
        };
        const points = `${svgStr(top)} ${svgStr(right)} ${svgStr(bottom)} ${svgStr(left)}`;
        return (0,sprotty__WEBPACK_IMPORTED_MODULE_1__.svg)("polygon", { points: points });
    }
};
ElkDiamondNodeView = __decorate([
    (0,inversify__WEBPACK_IMPORTED_MODULE_0__.injectable)()
], ElkDiamondNodeView);

let ElkRoundNodeView = class ElkRoundNodeView extends ElkNodeView {
    renderMark(node, context) {
        var _a, _b, _c, _d;
        let rx = node.size.width / 2;
        let ry = node.size.height / 2;
        let x = (_b = (_a = node.properties) === null || _a === void 0 ? void 0 : _a.shape) === null || _b === void 0 ? void 0 : _b.x;
        if (x == null)
            x = rx;
        let y = (_d = (_c = node.properties) === null || _c === void 0 ? void 0 : _c.shape) === null || _d === void 0 ? void 0 : _d.y;
        if (y == null)
            y = ry;
        return (0,sprotty__WEBPACK_IMPORTED_MODULE_1__.svg)("ellipse", { rx: rx, ry: ry, cx: x, cy: y });
    }
};
ElkRoundNodeView = __decorate([
    (0,inversify__WEBPACK_IMPORTED_MODULE_0__.injectable)()
], ElkRoundNodeView);

let ElkImageNodeView = class ElkImageNodeView extends ElkNodeView {
    renderMark(node, context) {
        var _a, _b;
        let width = node.size.width;
        let height = node.size.height;
        return (0,sprotty__WEBPACK_IMPORTED_MODULE_1__.svg)("image", { width: width, height: height, href: (_b = (_a = node.properties) === null || _a === void 0 ? void 0 : _a.shape) === null || _b === void 0 ? void 0 : _b.use });
    }
};
ElkImageNodeView = __decorate([
    (0,inversify__WEBPACK_IMPORTED_MODULE_0__.injectable)()
], ElkImageNodeView);

let ElkCommentNodeView = class ElkCommentNodeView extends ElkNodeView {
    renderMark(node, context) {
        var _a, _b;
        let tabSize = Number((_b = (_a = node === null || node === void 0 ? void 0 : node.properties) === null || _a === void 0 ? void 0 : _a.shape) === null || _b === void 0 ? void 0 : _b.use) || 15;
        let width = node.size.width;
        let height = node.size.height;
        const points = [
            { x: 0, y: 0 },
            { x: width - tabSize, y: 0 },
            { x: width, y: tabSize },
            { x: width, y: height },
            { x: 0, y: height },
        ]
            .map(svgStr)
            .join(' ');
        return (0,sprotty__WEBPACK_IMPORTED_MODULE_1__.svg)("polygon", { points: points });
    }
};
ElkCommentNodeView = __decorate([
    (0,inversify__WEBPACK_IMPORTED_MODULE_0__.injectable)()
], ElkCommentNodeView);

let ElkPathNodeView = class ElkPathNodeView extends ElkNodeView {
    renderMark(node, context) {
        var _a, _b;
        let segments = (_b = (_a = node === null || node === void 0 ? void 0 : node.properties) === null || _a === void 0 ? void 0 : _a.shape) === null || _b === void 0 ? void 0 : _b.use;
        return (0,sprotty__WEBPACK_IMPORTED_MODULE_1__.svg)("path", { d: segments });
    }
};
ElkPathNodeView = __decorate([
    (0,inversify__WEBPACK_IMPORTED_MODULE_0__.injectable)()
], ElkPathNodeView);

let ElkUseNodeView = class ElkUseNodeView extends ElkNodeView {
    renderMark(node, context) {
        var _a, _b;
        let use = (_b = (_a = node === null || node === void 0 ? void 0 : node.properties) === null || _a === void 0 ? void 0 : _a.shape) === null || _b === void 0 ? void 0 : _b.use;
        let href = context.hrefID(use);
        let mark = ((0,sprotty__WEBPACK_IMPORTED_MODULE_1__.svg)("use", { href: '#' + href, width: node.size.width, height: node.size.height }));
        (0,sprotty__WEBPACK_IMPORTED_MODULE_1__.setClass)(mark, use, true);
        return mark;
    }
};
ElkUseNodeView = __decorate([
    (0,inversify__WEBPACK_IMPORTED_MODULE_0__.injectable)()
], ElkUseNodeView);

let ElkSVGNodeView = class ElkSVGNodeView extends ElkNodeView {
    renderMark(node, context) {
        var _a, _b, _c, _d, _e, _f;
        let x = ((_b = (_a = node.properties) === null || _a === void 0 ? void 0 : _a.shape) === null || _b === void 0 ? void 0 : _b.x) || 0;
        let y = ((_d = (_c = node.properties) === null || _c === void 0 ? void 0 : _c.shape) === null || _d === void 0 ? void 0 : _d.y) || 0;
        return (0,sprotty__WEBPACK_IMPORTED_MODULE_1__.svg)('g', {
            props: { innerHTML: (_f = (_e = node === null || node === void 0 ? void 0 : node.properties) === null || _e === void 0 ? void 0 : _e.shape) === null || _f === void 0 ? void 0 : _f.use },
            transform: `translate(${x} ${y})`,
        });
    }
};
ElkSVGNodeView = __decorate([
    (0,inversify__WEBPACK_IMPORTED_MODULE_0__.injectable)()
], ElkSVGNodeView);

let ElkCompartmentNodeView = class ElkCompartmentNodeView extends ElkNodeView {
    renderMark(node, context) {
        if (node.parent.type == node.type) {
            const parentSize = node.parent.size;
            return ((0,sprotty__WEBPACK_IMPORTED_MODULE_1__.svg)("rect", { x: "0", y: "0", width: parentSize.width, height: node.size.height }));
        }
        return super.renderMark(node, context);
    }
};
ElkCompartmentNodeView = __decorate([
    (0,inversify__WEBPACK_IMPORTED_MODULE_0__.injectable)()
], ElkCompartmentNodeView);

let ElkForeignObjectNodeView = class ElkForeignObjectNodeView extends ElkNodeView {
    renderMark(node, context) {
        var _a, _b;
        let contents = (0,sprotty__WEBPACK_IMPORTED_MODULE_1__.html)('div', { props: { innerHTML: (_b = (_a = node === null || node === void 0 ? void 0 : node.properties) === null || _a === void 0 ? void 0 : _a.shape) === null || _b === void 0 ? void 0 : _b.use } });
        return ((0,sprotty__WEBPACK_IMPORTED_MODULE_1__.svg)("foreignObject", { requiredFeatures: "http://www.w3.org/TR/SVG11/feature#Extensibility", height: node.size.height, width: node.size.width, x: 0, y: 0 }, contents));
    }
};
ElkForeignObjectNodeView = __decorate([
    (0,inversify__WEBPACK_IMPORTED_MODULE_0__.injectable)()
], ElkForeignObjectNodeView);

/**
 * View for bridging the JupyterLab Widgets with Sprotty Elements
 */
let ElkJLNodeView = class ElkJLNodeView extends ElkNodeView {
    render(node, context) {
        if (!this.isSymbol(node) && !this.isVisible(node, context)) {
            return;
        }
        let mark = this.renderMark(node, context);
        if (!this.isSymbol(node)) {
            // skip marking extra classes on symbol nodes
            (0,sprotty__WEBPACK_IMPORTED_MODULE_1__.setClass)(mark, 'elknode', true);
            (0,sprotty__WEBPACK_IMPORTED_MODULE_1__.setClass)(mark, 'mouseover', node.hoverFeedback);
            (0,sprotty__WEBPACK_IMPORTED_MODULE_1__.setClass)(mark, 'selected', node.selected);
        }
        (0,sprotty__WEBPACK_IMPORTED_MODULE_1__.setClass)(mark, node.type, true);
        return (0,sprotty__WEBPACK_IMPORTED_MODULE_1__.svg)('g', {
            hook: {
                insert: (vnode) => context.registerJLWidgetNode(vnode, node, true),
                destroy: (vnode) => context.registerJLWidgetNode(vnode, node, false),
                update: (oldnode, vnode) => context.registerJLWidgetNode(vnode, node, this.isVisible(node, context)),
            },
        }, mark, (0,sprotty__WEBPACK_IMPORTED_MODULE_1__.svg)("g", { "class-elkchildren": true }, this.renderChildren(node, context)));
    }
};
ElkJLNodeView = __decorate([
    (0,inversify__WEBPACK_IMPORTED_MODULE_0__.injectable)()
], ElkJLNodeView);

let ElkPortView = class ElkPortView extends _base__WEBPACK_IMPORTED_MODULE_2__.RectangularNodeView {
    render(port, context) {
        var _a, _b;
        let mark;
        let use = (_b = (_a = port === null || port === void 0 ? void 0 : port.properties) === null || _a === void 0 ? void 0 : _a.shape) === null || _b === void 0 ? void 0 : _b.use;
        let href = context.hrefID(use);
        if (href) {
            mark = ((0,sprotty__WEBPACK_IMPORTED_MODULE_1__.svg)("use", { "class-elkport": true, width: port.size.width, height: port.size.height, "class-mouseover": port.hoverFeedback, "class-selected": port.selected, href: '#' + href }));
            (0,sprotty__WEBPACK_IMPORTED_MODULE_1__.setClass)(mark, use, true);
        }
        else {
            mark = ((0,sprotty__WEBPACK_IMPORTED_MODULE_1__.svg)("rect", { "class-elkport": true, "class-mouseover": port.hoverFeedback, "class-selected": port.selected, 
                // className={port.properties.classes}
                x: "0", y: "0", width: port.size.width, height: port.size.height }));
        }
        return ((0,sprotty__WEBPACK_IMPORTED_MODULE_1__.svg)("g", null,
            mark,
            context.renderChildren(port)));
    }
};
ElkPortView = __decorate([
    (0,inversify__WEBPACK_IMPORTED_MODULE_0__.injectable)()
], ElkPortView);

let ElkLabelView = class ElkLabelView extends _base__WEBPACK_IMPORTED_MODULE_2__.ShapeView {
    render(label, context) {
        var _a, _b, _c, _d, _e;
        // label.root.zoom
        if (!this.isVisible(label, context)) {
            return undefined;
        }
        let mark;
        let use = (_b = (_a = label === null || label === void 0 ? void 0 : label.properties) === null || _a === void 0 ? void 0 : _a.shape) === null || _b === void 0 ? void 0 : _b.use;
        let href = context.hrefID(use);
        if (href) {
            mark = ((0,sprotty__WEBPACK_IMPORTED_MODULE_1__.svg)("use", { "class-elklabel": true, "class-mouseover": label.hoverFeedback, "class-selected": label.selected, href: '#' + href, width: label.size.width, height: label.size.height }));
            (0,sprotty__WEBPACK_IMPORTED_MODULE_1__.setClass)(mark, use, true);
        }
        else {
            mark = ((0,sprotty__WEBPACK_IMPORTED_MODULE_1__.svg)("text", { "class-elklabel": true, "class-selected": label.selected, "class-mouseover": label.hoverFeedback }, label.text));
        }
        if ((_c = label.labels) === null || _c === void 0 ? void 0 : _c.length) {
            let icon = label.labels[0];
            let use = (_e = (_d = icon === null || icon === void 0 ? void 0 : icon.properties) === null || _d === void 0 ? void 0 : _d.shape) === null || _e === void 0 ? void 0 : _e.use;
            let href = context.hrefID(use);
            let height = label.size.height;
            let iconDims = this.dimension(icon);
            let labelDims = this.dimension(label);
            let iconPos = {
                x: 0 + icon.position.x,
                y: (height - iconDims.height) / 2 + icon.position.x,
            };
            let opts = (icon === null || icon === void 0 ? void 0 : icon.layoutOptions) || {};
            let spacing = Number(opts['org.eclipse.elk.spacing.labelLabel']) || 0;
            let labelPos = {
                x: iconDims.width + spacing,
                y: (height - labelDims.height) / 2,
            };
            mark = ((0,sprotty__WEBPACK_IMPORTED_MODULE_1__.svg)("g", null,
                (0,sprotty__WEBPACK_IMPORTED_MODULE_1__.svg)("use", { transform: `translate(${iconPos.x} ${iconPos.y})`, "class-elklabel": true, "class-mouseover": label.hoverFeedback, "class-selected": label.selected, href: '#' + href, width: icon.size.width, height: icon.size.height }),
                (0,sprotty__WEBPACK_IMPORTED_MODULE_1__.svg)("g", { transform: `translate(${labelPos.x} ${labelPos.y})` }, mark)));
        }
        return mark;
    }
    dimension(label) {
        var _a, _b, _c, _d;
        return {
            width: ((_b = (_a = label === null || label === void 0 ? void 0 : label.properties) === null || _a === void 0 ? void 0 : _a.shape) === null || _b === void 0 ? void 0 : _b.width) || label.size.width,
            height: ((_d = (_c = label === null || label === void 0 ? void 0 : label.properties) === null || _c === void 0 ? void 0 : _c.shape) === null || _d === void 0 ? void 0 : _d.height) || label.size.height,
        };
    }
    isVisible(label, context) {
        // check first if label is within bounding box of view
        let inView = super.isVisible(label, context);
        if (!inView) {
            return false;
        }
        // check if label should be rendered due to zoom level and min size
        const root = label.root;
        let zoom = root['zoom']; // should there be a method on the context to get the zoom level?
        let heightLOD;
        if (label.size.height) {
            heightLOD = zoom * label.size.height > 3;
        }
        else {
            heightLOD = true;
        }
        return heightLOD;
    }
};
ElkLabelView = __decorate([
    (0,inversify__WEBPACK_IMPORTED_MODULE_0__.injectable)()
], ElkLabelView);



/***/ }),

/***/ "./lib/sprotty/views/symbol_views.js":
/*!*******************************************!*\
  !*** ./lib/sprotty/views/symbol_views.js ***!
  \*******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   SymbolNodeView: () => (/* binding */ SymbolNodeView)
/* harmony export */ });
/* harmony import */ var inversify__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! inversify */ "webpack/sharing/consume/default/inversify/inversify");
/* harmony import */ var inversify__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(inversify__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var sprotty__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! sprotty */ "webpack/sharing/consume/default/sprotty/sprotty");
/* harmony import */ var sprotty__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(sprotty__WEBPACK_IMPORTED_MODULE_1__);
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};


let SymbolNodeView = class SymbolNodeView {
    render(symbol, context) {
        var _a, _b;
        let x = ((_a = symbol.position) === null || _a === void 0 ? void 0 : _a.x) || 0;
        let y = ((_b = symbol.position) === null || _b === void 0 ? void 0 : _b.y) || 0;
        let width = symbol.size.width || 0;
        let height = symbol.size.height || 0;
        let attrs = {
            class: {
                [symbol.id]: true,
                elksymbol: true,
            },
        };
        if (width && height) {
            attrs['viewBox'] = `${x} ${y} ${width} ${height}`;
        }
        return (0,sprotty__WEBPACK_IMPORTED_MODULE_1__.svg)('symbol', attrs, ...context.renderChildren(symbol));
    }
};
SymbolNodeView = __decorate([
    (0,inversify__WEBPACK_IMPORTED_MODULE_0__.injectable)()
], SymbolNodeView);



/***/ }),

/***/ "./lib/tools/draw-aware-mouse-listener.js":
/*!************************************************!*\
  !*** ./lib/tools/draw-aware-mouse-listener.js ***!
  \************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   DragAwareHoverMouseListener: () => (/* binding */ DragAwareHoverMouseListener),
/* harmony export */   DragAwareMouseListener: () => (/* binding */ DragAwareMouseListener)
/* harmony export */ });
/* harmony import */ var sprotty_protocol__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! sprotty-protocol */ "webpack/sharing/consume/default/sprotty-protocol/sprotty-protocol");
/* harmony import */ var sprotty_protocol__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(sprotty_protocol__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var sprotty__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! sprotty */ "webpack/sharing/consume/default/sprotty/sprotty");
/* harmony import */ var sprotty__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(sprotty__WEBPACK_IMPORTED_MODULE_1__);
/**
 * # Copyright (c) 2024 ipyelk contributors.
 * Distributed under the terms of the Modified BSD License.
 */


/**
 * A mouse listener that is aware of prior mouse dragging.
 *
 * Therefore, this listener distinguishes between mouse up events after dragging and
 * mouse up events without prior dragging. Subclasses may override the methods
 * `draggingMouseUp` and/or `nonDraggingMouseUp` to react to only these specific kinds
 * of mouse up events.
 */
class DragAwareMouseListener extends sprotty__WEBPACK_IMPORTED_MODULE_1__.MouseListener {
    constructor() {
        super(...arguments);
        this.isMouseDown = false;
        this.isMouseDrag = false;
    }
    mouseDown(target, event) {
        this.isMouseDown = true;
        return [];
    }
    mouseMove(target, event) {
        if (this.isMouseDown) {
            this.isMouseDrag = true;
        }
        return [];
    }
    mouseUp(element, event) {
        this.isMouseDown = false;
        if (this.isMouseDrag) {
            this.isMouseDrag = false;
            return this.draggingMouseUp(element, event);
        }
        return this.nonDraggingMouseUp(element, event);
    }
    nonDraggingMouseUp(element, event) {
        return [];
    }
    draggingMouseUp(element, event) {
        return [];
    }
}
class DragAwareHoverMouseListener extends DragAwareMouseListener {
    constructor(elementTypeId, tool) {
        super();
        this.elementTypeId = elementTypeId;
        this.tool = tool;
    }
    mouseOver(target, event) {
        return [
            sprotty_protocol__WEBPACK_IMPORTED_MODULE_0__.HoverFeedbackAction.create({ mouseoverElement: target.id, mouseIsOver: true }),
        ];
    }
    mouseOut(target, event) {
        return [
            sprotty_protocol__WEBPACK_IMPORTED_MODULE_0__.HoverFeedbackAction.create({ mouseoverElement: target.id, mouseIsOver: false }),
        ];
    }
}


/***/ }),

/***/ "./lib/tools/expand.js":
/*!*****************************!*\
  !*** ./lib/tools/expand.js ***!
  \*****************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   ExpandAction: () => (/* binding */ ExpandAction),
/* harmony export */   NodeExpandTool: () => (/* binding */ NodeExpandTool),
/* harmony export */   NodeExpandToolMouseListener: () => (/* binding */ NodeExpandToolMouseListener)
/* harmony export */ });
/* harmony import */ var inversify__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! inversify */ "webpack/sharing/consume/default/inversify/inversify");
/* harmony import */ var inversify__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(inversify__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var sprotty_protocol__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! sprotty-protocol */ "webpack/sharing/consume/default/sprotty-protocol/sprotty-protocol");
/* harmony import */ var sprotty_protocol__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(sprotty_protocol__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var sprotty__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! sprotty */ "webpack/sharing/consume/default/sprotty/sprotty");
/* harmony import */ var sprotty__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(sprotty__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var sprotty_lib_utils_iterable__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! sprotty/lib/utils/iterable */ "./node_modules/sprotty/lib/utils/iterable.js");
/* harmony import */ var _draw_aware_mouse_listener__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./draw-aware-mouse-listener */ "./lib/tools/draw-aware-mouse-listener.js");
/* harmony import */ var _tool__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./tool */ "./lib/tools/tool.js");
/* harmony import */ var _types__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./types */ "./lib/tools/types.js");
/* harmony import */ var _util__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./util */ "./lib/tools/util.js");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (undefined && undefined.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
var __param = (undefined && undefined.__param) || function (paramIndex, decorator) {
    return function (target, key) { decorator(target, key, paramIndex); }
};








class ExpandAction {
    constructor(expandElementsIDs = [], contractElementsIDs = []) {
        this.expandElementsIDs = expandElementsIDs;
        this.contractElementsIDs = contractElementsIDs;
        this.kind = sprotty_protocol__WEBPACK_IMPORTED_MODULE_1__.SelectAction.KIND;
    }
}
ExpandAction.KIND = 'elementExpand';
let NodeExpandTool = class NodeExpandTool extends _tool__WEBPACK_IMPORTED_MODULE_4__.DiagramTool {
    constructor(mouseTool, feedbackDispatcher) {
        super();
        this.mouseTool = mouseTool;
        this.feedbackDispatcher = feedbackDispatcher;
        this.elementTypeId = 'unknown';
        this.operationKind = ExpandAction.KIND;
    }
    enable() {
        this.expansionToolMouseListener = new NodeExpandToolMouseListener(this.elementTypeId, this);
        this.mouseTool.register(this.expansionToolMouseListener);
    }
    disable() {
        this.mouseTool.deregister(this.expansionToolMouseListener);
    }
    dispatchFeedback(actions) {
        this.feedbackDispatcher.registerFeedback(this, actions);
    }
};
NodeExpandTool = __decorate([
    (0,inversify__WEBPACK_IMPORTED_MODULE_0__.injectable)(),
    __param(0, (0,inversify__WEBPACK_IMPORTED_MODULE_0__.inject)(sprotty__WEBPACK_IMPORTED_MODULE_2__.MouseTool)),
    __param(1, (0,inversify__WEBPACK_IMPORTED_MODULE_0__.inject)(_types__WEBPACK_IMPORTED_MODULE_5__.ToolTYPES.IFeedbackActionDispatcher)),
    __metadata("design:paramtypes", [Object, Object])
], NodeExpandTool);

let NodeExpandToolMouseListener = class NodeExpandToolMouseListener extends _draw_aware_mouse_listener__WEBPACK_IMPORTED_MODULE_6__.DragAwareMouseListener {
    constructor(elementTypeId, tool) {
        super();
        this.elementTypeId = elementTypeId;
        this.tool = tool;
    }
    wheel(target, event) {
        return [];
        let entering = []; // elements entering selection
        let exiting = []; // element exiting selection
        if (event.button === 0) {
            const selectableTarget = (0,sprotty__WEBPACK_IMPORTED_MODULE_2__.findParentByFeature)(target, sprotty__WEBPACK_IMPORTED_MODULE_2__.isSelectable);
            if (selectableTarget != null) {
                // multi-selection?
                if (!(0,sprotty__WEBPACK_IMPORTED_MODULE_2__.isCtrlOrCmd)(event)) {
                    exiting = (0,sprotty_lib_utils_iterable__WEBPACK_IMPORTED_MODULE_3__.toArray)(target.root.index
                        .all()
                        .filter((element) => (0,sprotty__WEBPACK_IMPORTED_MODULE_2__.isSelectable)(element) &&
                        element.selected &&
                        !(selectableTarget instanceof sprotty__WEBPACK_IMPORTED_MODULE_2__.SRoutingHandleImpl &&
                            element === selectableTarget.parent)));
                }
                if (selectableTarget != null) {
                    if (!selectableTarget.selected) {
                        entering = [selectableTarget];
                    }
                    else if ((0,sprotty__WEBPACK_IMPORTED_MODULE_2__.isCtrlOrCmd)(event)) {
                        exiting = [selectableTarget];
                    }
                }
            }
        }
        return [
            sprotty_protocol__WEBPACK_IMPORTED_MODULE_1__.SelectAction.create({
                selectedElementsIDs: entering.map(_util__WEBPACK_IMPORTED_MODULE_7__.idGetter),
                deselectedElementsIDs: exiting.map(_util__WEBPACK_IMPORTED_MODULE_7__.idGetter),
            }),
        ];
    }
    /**
     * Apply CSS `selected` class for selected elements
     *  TODO replace with `this.tool.dispatchFeedback`?
     * @param vnode
     * @param element
     */
    decorate(vnode, element) {
        const selectableTarget = (0,sprotty__WEBPACK_IMPORTED_MODULE_2__.findParentByFeature)(element, sprotty__WEBPACK_IMPORTED_MODULE_2__.isSelectable);
        if (selectableTarget != null)
            (0,sprotty__WEBPACK_IMPORTED_MODULE_2__.setClass)(vnode, 'selected', selectableTarget.selected);
        return vnode;
    }
};
NodeExpandToolMouseListener = __decorate([
    (0,inversify__WEBPACK_IMPORTED_MODULE_0__.injectable)(),
    __metadata("design:paramtypes", [String, NodeExpandTool])
], NodeExpandToolMouseListener);



/***/ }),

/***/ "./lib/tools/feedback/cursor-feedback.js":
/*!***********************************************!*\
  !*** ./lib/tools/feedback/cursor-feedback.js ***!
  \***********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   ApplyCSSFeedbackAction: () => (/* binding */ ApplyCSSFeedbackAction),
/* harmony export */   ApplyCursorCSSFeedbackActionCommand: () => (/* binding */ ApplyCursorCSSFeedbackActionCommand),
/* harmony export */   CursorCSS: () => (/* binding */ CursorCSS)
/* harmony export */ });
/* harmony import */ var inversify__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! inversify */ "webpack/sharing/consume/default/inversify/inversify");
/* harmony import */ var inversify__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(inversify__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var sprotty_lib__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! sprotty/lib */ "./node_modules/sprotty/lib/index.js");
/* harmony import */ var sprotty_lib__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(sprotty_lib__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _model__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./model */ "./lib/tools/feedback/model.js");
/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./utils */ "./lib/tools/feedback/utils.js");
/**
 * # Copyright (c) 2024 ipyelk contributors.
 * Distributed under the terms of the Modified BSD License.
 */
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (undefined && undefined.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
var __param = (undefined && undefined.__param) || function (paramIndex, decorator) {
    return function (target, key) { decorator(target, key, paramIndex); }
};
/********************************************************************************
 * Copyright (c) 2019 EclipseSource and others.
 *
 * This program and the accompanying materials are made available under the
 * terms of the Eclipse Public License v. 2.0 which is available at
 * http://www.eclipse.org/legal/epl-2.0.
 *
 * This Source Code may also be made available under the following Secondary
 * Licenses when the conditions for such availability set forth in the Eclipse
 * Public License v. 2.0 are satisfied: GNU General Public License, version 2
 * with the GNU Classpath Exception which is available at
 * https://www.gnu.org/software/classpath/license.html.
 *
 * SPDX-License-Identifier: EPL-2.0 OR GPL-2.0 WITH Classpath-exception-2.0
 ********************************************************************************/




var CursorCSS;
(function (CursorCSS) {
    CursorCSS["DEFAULT"] = "default-mode";
    CursorCSS["OVERLAP_FORBIDDEN"] = "overlap-forbidden-mode";
    CursorCSS["NODE_CREATION"] = "node-creation-mode";
    CursorCSS["EDGE_CREATION_SOURCE"] = "edge-creation-select-source-mode";
    CursorCSS["EDGE_CREATION_TARGET"] = "edge-creation-select-target-mode";
    CursorCSS["EDGE_RECONNECT"] = "edge-reconnect-select-target-mode";
    CursorCSS["OPERATION_NOT_ALLOWED"] = "edge-modification-not-allowed-mode";
    CursorCSS["ELEMENT_DELETION"] = "element-deletion-mode";
    CursorCSS["MOUSEOVER"] = "mouseover";
    CursorCSS["SELECTED"] = "selected";
})(CursorCSS || (CursorCSS = {}));
class ApplyCSSFeedbackAction {
    constructor(target, cssClass) {
        this.target = target;
        this.cssClass = cssClass;
        this.kind = ApplyCursorCSSFeedbackActionCommand.KIND;
    }
}
let ApplyCursorCSSFeedbackActionCommand = class ApplyCursorCSSFeedbackActionCommand extends _model__WEBPACK_IMPORTED_MODULE_2__.FeedbackCommand {
    constructor(action) {
        super();
        this.action = action;
    }
    execute(context) {
        (0,_utils__WEBPACK_IMPORTED_MODULE_3__.removeCssClasses)(this.action.target, Object.values(CursorCSS));
        if (this.action.cssClass) {
            (0,_utils__WEBPACK_IMPORTED_MODULE_3__.addCssClasses)(this.action.target, [this.action.cssClass]);
        }
        return context.root;
    }
};
ApplyCursorCSSFeedbackActionCommand.KIND = 'applyCursorCssFeedback';
ApplyCursorCSSFeedbackActionCommand = __decorate([
    (0,inversify__WEBPACK_IMPORTED_MODULE_0__.injectable)(),
    __param(0, (0,inversify__WEBPACK_IMPORTED_MODULE_0__.inject)(sprotty_lib__WEBPACK_IMPORTED_MODULE_1__.TYPES.Action)),
    __metadata("design:paramtypes", [ApplyCSSFeedbackAction])
], ApplyCursorCSSFeedbackActionCommand);



/***/ }),

/***/ "./lib/tools/feedback/di.config.js":
/*!*****************************************!*\
  !*** ./lib/tools/feedback/di.config.js ***!
  \*****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var inversify__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! inversify */ "webpack/sharing/consume/default/inversify/inversify");
/* harmony import */ var inversify__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(inversify__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var sprotty_lib__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! sprotty/lib */ "./node_modules/sprotty/lib/index.js");
/* harmony import */ var sprotty_lib__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(sprotty_lib__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _types__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../types */ "./lib/tools/types.js");
/* harmony import */ var _cursor_feedback__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./cursor-feedback */ "./lib/tools/feedback/cursor-feedback.js");
/* harmony import */ var _feedback_action_dispatcher__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./feedback-action-dispatcher */ "./lib/tools/feedback/feedback-action-dispatcher.js");
/**
 * # Copyright (c) 2024 ipyelk contributors.
 * Distributed under the terms of the Modified BSD License.
 */





const toolFeedbackModule = new inversify__WEBPACK_IMPORTED_MODULE_0__.ContainerModule((bind, _unbind, isBound) => {
    bind(_types__WEBPACK_IMPORTED_MODULE_2__.ToolTYPES.IFeedbackActionDispatcher)
        .to(_feedback_action_dispatcher__WEBPACK_IMPORTED_MODULE_3__.FeedbackActionDispatcher)
        .inSingletonScope();
    // create node and edge tool feedback
    (0,sprotty_lib__WEBPACK_IMPORTED_MODULE_1__.configureCommand)({ bind, isBound }, _cursor_feedback__WEBPACK_IMPORTED_MODULE_4__.ApplyCursorCSSFeedbackActionCommand);
    (0,sprotty_lib__WEBPACK_IMPORTED_MODULE_1__.configureCommand)({ bind, isBound }, sprotty_lib__WEBPACK_IMPORTED_MODULE_1__.MoveCommand);
    //Select commands
    (0,sprotty_lib__WEBPACK_IMPORTED_MODULE_1__.configureCommand)({ bind, isBound }, sprotty_lib__WEBPACK_IMPORTED_MODULE_1__.SelectCommand);
    (0,sprotty_lib__WEBPACK_IMPORTED_MODULE_1__.configureCommand)({ bind, isBound }, sprotty_lib__WEBPACK_IMPORTED_MODULE_1__.SelectAllCommand);
    (0,sprotty_lib__WEBPACK_IMPORTED_MODULE_1__.configureCommand)({ bind, isBound }, sprotty_lib__WEBPACK_IMPORTED_MODULE_1__.GetSelectionCommand);
    bind(sprotty_lib__WEBPACK_IMPORTED_MODULE_1__.TYPES.IVNodePostprocessor).to(sprotty_lib__WEBPACK_IMPORTED_MODULE_1__.LocationPostprocessor);
    bind(sprotty_lib__WEBPACK_IMPORTED_MODULE_1__.TYPES.HiddenVNodePostprocessor).to(sprotty_lib__WEBPACK_IMPORTED_MODULE_1__.LocationPostprocessor);
});
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (toolFeedbackModule);


/***/ }),

/***/ "./lib/tools/feedback/feedback-action-dispatcher.js":
/*!**********************************************************!*\
  !*** ./lib/tools/feedback/feedback-action-dispatcher.js ***!
  \**********************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   FeedbackActionDispatcher: () => (/* binding */ FeedbackActionDispatcher)
/* harmony export */ });
/* harmony import */ var inversify__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! inversify */ "webpack/sharing/consume/default/inversify/inversify");
/* harmony import */ var inversify__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(inversify__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var sprotty_lib__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! sprotty/lib */ "./node_modules/sprotty/lib/index.js");
/* harmony import */ var sprotty_lib__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(sprotty_lib__WEBPACK_IMPORTED_MODULE_1__);
/**
 * # Copyright (c) 2024 ipyelk contributors.
 * Distributed under the terms of the Modified BSD License.
 */
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (undefined && undefined.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
var __param = (undefined && undefined.__param) || function (paramIndex, decorator) {
    return function (target, key) { decorator(target, key, paramIndex); }
};
/********************************************************************************
 * Copyright (c) 2019 EclipseSource and others.
 *
 * This program and the accompanying materials are made available under the
 * terms of the Eclipse Public License v. 2.0 which is available at
 * http://www.eclipse.org/legal/epl-2.0.
 *
 * This Source Code may also be made available under the following Secondary
 * Licenses when the conditions for such availability set forth in the Eclipse
 * Public License v. 2.0 are satisfied: GNU General Public License, version 2
 * with the GNU Classpath Exception which is available at
 * https://www.gnu.org/software/classpath/license.html.
 *
 * SPDX-License-Identifier: EPL-2.0 OR GPL-2.0 WITH Classpath-exception-2.0
 ********************************************************************************/



let FeedbackActionDispatcher = class FeedbackActionDispatcher {
    constructor(actionDispatcher, logger) {
        this.actionDispatcher = actionDispatcher;
        this.logger = logger;
        this.feedbackEmitters = new Map();
    }
    registerFeedback(feedbackEmitter, actions) {
        this.feedbackEmitters.set(feedbackEmitter, actions);
        this.dispatch(actions, feedbackEmitter);
    }
    deregisterFeedback(feedbackEmitter, actions) {
        this.feedbackEmitters.delete(feedbackEmitter);
        this.dispatch(actions, feedbackEmitter);
    }
    dispatch(actions, feedbackEmitter) {
        this.actionDispatcher()
            .then((dispatcher) => dispatcher.dispatchAll(actions))
            .then(() => this.logger.info(this, `Dispatched feedback actions for ${feedbackEmitter}`))
            .catch((reason) => this.logger.error(this, 'Failed to dispatch feedback actions', reason));
    }
    getRegisteredFeedback() {
        const result = [];
        this.feedbackEmitters.forEach((value, key) => result.push(...value));
        return result;
    }
    getRegisteredFeedbackEmitters(action) {
        const result = [];
        this.feedbackEmitters.forEach((value, key) => {
            if (value.find((a) => a === action)) {
                result.push(key);
            }
        });
        return result;
    }
};
FeedbackActionDispatcher = __decorate([
    (0,inversify__WEBPACK_IMPORTED_MODULE_0__.injectable)(),
    __param(0, (0,inversify__WEBPACK_IMPORTED_MODULE_0__.inject)(sprotty_lib__WEBPACK_IMPORTED_MODULE_1__.TYPES.IActionDispatcherProvider)),
    __param(1, (0,inversify__WEBPACK_IMPORTED_MODULE_0__.inject)(sprotty_lib__WEBPACK_IMPORTED_MODULE_1__.TYPES.ILogger)),
    __metadata("design:paramtypes", [Function, Object])
], FeedbackActionDispatcher);



/***/ }),

/***/ "./lib/tools/feedback/model.js":
/*!*************************************!*\
  !*** ./lib/tools/feedback/model.js ***!
  \*************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   FeedbackCommand: () => (/* binding */ FeedbackCommand)
/* harmony export */ });
/* harmony import */ var sprotty_lib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! sprotty/lib */ "./node_modules/sprotty/lib/index.js");
/* harmony import */ var sprotty_lib__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(sprotty_lib__WEBPACK_IMPORTED_MODULE_0__);
/**
 * # Copyright (c) 2024 ipyelk contributors.
 * Distributed under the terms of the Modified BSD License.
 */
/********************************************************************************
 * Copyright (c) 2019 EclipseSource and others.
 *
 * This program and the accompanying materials are made available under the
 * terms of the Eclipse Public License v. 2.0 which is available at
 * http://www.eclipse.org/legal/epl-2.0.
 *
 * This Source Code may also be made available under the following Secondary
 * Licenses when the conditions for such availability set forth in the Eclipse
 * Public License v. 2.0 are satisfied: GNU General Public License, version 2
 * with the GNU Classpath Exception which is available at
 * https://www.gnu.org/software/classpath/license.html.
 *
 * SPDX-License-Identifier: EPL-2.0 OR GPL-2.0 WITH Classpath-exception-2.0
 ********************************************************************************/

class FeedbackCommand extends sprotty_lib__WEBPACK_IMPORTED_MODULE_0__.Command {
    constructor() {
        super(...arguments);
        // used by the `FeedbackAwareUpdateModelCommand`
        this.priority = 0;
    }
    undo(context) {
        return context.root;
    }
    redo(context) {
        return context.root;
    }
}


/***/ }),

/***/ "./lib/tools/feedback/utils.js":
/*!*************************************!*\
  !*** ./lib/tools/feedback/utils.js ***!
  \*************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   addCssClasses: () => (/* binding */ addCssClasses),
/* harmony export */   removeCssClasses: () => (/* binding */ removeCssClasses)
/* harmony export */ });
function addCssClasses(root, cssClasses) {
    if (root.cssClasses == null) {
        root.cssClasses = [];
    }
    for (const cssClass of cssClasses) {
        if (root.cssClasses.indexOf(cssClass) < 0) {
            root.cssClasses.push(cssClass);
        }
    }
}
function removeCssClasses(root, cssClasses) {
    if (root.cssClasses == null || root.cssClasses.length === 0) {
        return;
    }
    for (const cssClass of cssClasses) {
        const index = root.cssClasses.indexOf(cssClass);
        if (index !== -1) {
            root.cssClasses.splice(root.cssClasses.indexOf(cssClass), 1);
        }
    }
}


/***/ }),

/***/ "./lib/tools/select.js":
/*!*****************************!*\
  !*** ./lib/tools/select.js ***!
  \*****************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   NodeSelectTool: () => (/* binding */ NodeSelectTool),
/* harmony export */   NodeSelectToolMouseListener: () => (/* binding */ NodeSelectToolMouseListener)
/* harmony export */ });
/* harmony import */ var inversify__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! inversify */ "webpack/sharing/consume/default/inversify/inversify");
/* harmony import */ var inversify__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(inversify__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var sprotty_protocol__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! sprotty-protocol */ "webpack/sharing/consume/default/sprotty-protocol/sprotty-protocol");
/* harmony import */ var sprotty_protocol__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(sprotty_protocol__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var sprotty__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! sprotty */ "webpack/sharing/consume/default/sprotty/sprotty");
/* harmony import */ var sprotty__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(sprotty__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var sprotty_lib_utils_iterable__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! sprotty/lib/utils/iterable */ "./node_modules/sprotty/lib/utils/iterable.js");
/* harmony import */ var _draw_aware_mouse_listener__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./draw-aware-mouse-listener */ "./lib/tools/draw-aware-mouse-listener.js");
/* harmony import */ var _tool__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./tool */ "./lib/tools/tool.js");
/* harmony import */ var _types__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./types */ "./lib/tools/types.js");
/* harmony import */ var _util__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./util */ "./lib/tools/util.js");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (undefined && undefined.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
var __param = (undefined && undefined.__param) || function (paramIndex, decorator) {
    return function (target, key) { decorator(target, key, paramIndex); }
};








let NodeSelectTool = class NodeSelectTool extends _tool__WEBPACK_IMPORTED_MODULE_4__.DiagramTool {
    constructor(mouseTool, feedbackDispatcher) {
        super();
        this.mouseTool = mouseTool;
        this.feedbackDispatcher = feedbackDispatcher;
        this.elementTypeId = 'unknown';
        this.operationKind = sprotty_protocol__WEBPACK_IMPORTED_MODULE_1__.SelectAction.KIND;
    }
    enable() {
        this.selectionToolMouseListener = new NodeSelectToolMouseListener(this.elementTypeId, this);
        this.mouseTool.register(this.selectionToolMouseListener);
    }
    disable() {
        this.mouseTool.deregister(this.selectionToolMouseListener);
    }
};
NodeSelectTool = __decorate([
    (0,inversify__WEBPACK_IMPORTED_MODULE_0__.injectable)(),
    __param(0, (0,inversify__WEBPACK_IMPORTED_MODULE_0__.inject)(sprotty__WEBPACK_IMPORTED_MODULE_2__.MouseTool)),
    __param(1, (0,inversify__WEBPACK_IMPORTED_MODULE_0__.inject)(_types__WEBPACK_IMPORTED_MODULE_5__.ToolTYPES.IFeedbackActionDispatcher)),
    __metadata("design:paramtypes", [Object, Object])
], NodeSelectTool);

let NodeSelectToolMouseListener = class NodeSelectToolMouseListener extends _draw_aware_mouse_listener__WEBPACK_IMPORTED_MODULE_6__.DragAwareHoverMouseListener {
    constructor(elementTypeId, tool) {
        super(elementTypeId, tool);
        this.elementTypeId = elementTypeId;
        this.tool = tool;
    }
    nonDraggingMouseUp(target, event) {
        let entering = []; // elements entering selection
        let exiting = []; // element exiting selection
        if (event.button === 0 && !isJLWidget(event.target)) {
            const selectableTarget = (0,sprotty__WEBPACK_IMPORTED_MODULE_2__.findParentByFeature)(target, sprotty__WEBPACK_IMPORTED_MODULE_2__.isSelectable);
            if (selectableTarget != null) {
                // multi-selection?
                if (!(0,sprotty__WEBPACK_IMPORTED_MODULE_2__.isCtrlOrCmd)(event)) {
                    exiting = (0,sprotty_lib_utils_iterable__WEBPACK_IMPORTED_MODULE_3__.toArray)(target.root.index
                        .all()
                        .filter((element) => (0,sprotty__WEBPACK_IMPORTED_MODULE_2__.isSelectable)(element) &&
                        element.selected &&
                        !(selectableTarget instanceof sprotty__WEBPACK_IMPORTED_MODULE_2__.SRoutingHandleImpl &&
                            element === selectableTarget.parent)));
                }
                if (selectableTarget != null) {
                    if (!selectableTarget.selected) {
                        entering = [selectableTarget];
                    }
                    else if ((0,sprotty__WEBPACK_IMPORTED_MODULE_2__.isCtrlOrCmd)(event)) {
                        exiting = [selectableTarget];
                    }
                }
            }
        }
        return [
            sprotty_protocol__WEBPACK_IMPORTED_MODULE_1__.SelectAction.create({
                selectedElementsIDs: entering.map(_util__WEBPACK_IMPORTED_MODULE_7__.idGetter),
                deselectedElementsIDs: exiting.map(_util__WEBPACK_IMPORTED_MODULE_7__.idGetter),
            }),
        ];
    }
    /**
     * Apply CSS `selected` class for selected elements
     * @param vnode
     * @param element
     */
    decorate(vnode, element) {
        const selectableTarget = (0,sprotty__WEBPACK_IMPORTED_MODULE_2__.findParentByFeature)(element, sprotty__WEBPACK_IMPORTED_MODULE_2__.isSelectable);
        if (selectableTarget != null)
            (0,sprotty__WEBPACK_IMPORTED_MODULE_2__.setClass)(vnode, 'selected', selectableTarget.selected);
        return vnode;
    }
};
NodeSelectToolMouseListener = __decorate([
    (0,inversify__WEBPACK_IMPORTED_MODULE_0__.injectable)(),
    __metadata("design:paramtypes", [String, NodeSelectTool])
], NodeSelectToolMouseListener);

/*
 * Test is given dom element is a jupyter lab widget
 */
function isJLWidget(target) {
    var _a;
    // TODO is this sufficiently robust?
    return (_a = target === null || target === void 0 ? void 0 : target.classList) === null || _a === void 0 ? void 0 : _a.contains('jupyter-widgets');
}


/***/ }),

/***/ "./lib/tools/tool.js":
/*!***************************!*\
  !*** ./lib/tools/tool.js ***!
  \***************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   DiagramTool: () => (/* binding */ DiagramTool),
/* harmony export */   TOOL_ID_PREFIX: () => (/* binding */ TOOL_ID_PREFIX),
/* harmony export */   deriveToolId: () => (/* binding */ deriveToolId)
/* harmony export */ });
/* harmony import */ var inversify__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! inversify */ "webpack/sharing/consume/default/inversify/inversify");
/* harmony import */ var inversify__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(inversify__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var sprotty__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! sprotty */ "webpack/sharing/consume/default/sprotty/sprotty");
/* harmony import */ var sprotty__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(sprotty__WEBPACK_IMPORTED_MODULE_1__);
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
/**
 * # Copyright (c) 2024 ipyelk contributors.
 * Distributed under the terms of the Modified BSD License.
 */


const TOOL_ID_PREFIX = 'tool';
function deriveToolId(operationKind, elementTypeId) {
    return `${TOOL_ID_PREFIX}_${operationKind}_${elementTypeId}`;
}
// TODO make this an interface?
let DiagramTool = class DiagramTool extends sprotty__WEBPACK_IMPORTED_MODULE_1__.MouseTool {
    constructor() {
        super(...arguments);
        this.elementTypeId = 'unknown';
        this.operationKind = 'generic';
    }
    get id() {
        return deriveToolId(this.operationKind, this.elementTypeId);
    }
    enable() { }
    disable() { }
    dispatchFeedback(actions) { }
};
DiagramTool = __decorate([
    (0,inversify__WEBPACK_IMPORTED_MODULE_0__.injectable)()
], DiagramTool);



/***/ }),

/***/ "./lib/tools/types.js":
/*!****************************!*\
  !*** ./lib/tools/types.js ***!
  \****************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   ToolTYPES: () => (/* binding */ ToolTYPES)
/* harmony export */ });
/**
 * # Copyright (c) 2024 ipyelk contributors.
 * Distributed under the terms of the Modified BSD License.
 */
const ToolTYPES = {
    IFeedbackActionDispatcher: Symbol.for('IFeedbackActionDispatcher'),
    IToolFactory: Symbol.for('Factory<Tool>'),
    IEditConfigProvider: Symbol.for('IEditConfigProvider'),
    RequestResponseSupport: Symbol.for('RequestResponseSupport'),
    SelectionService: Symbol.for('SelectionService'),
    SelectionListener: Symbol.for('SelectionListener'),
    SModelRootListener: Symbol.for('SModelRootListener'),
    MouseTool: Symbol.for('MouseTool'),
    ViewerOptions: Symbol.for('ViewerOptions'),
};


/***/ }),

/***/ "./lib/tools/util.js":
/*!***************************!*\
  !*** ./lib/tools/util.js ***!
  \***************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   idGetter: () => (/* binding */ idGetter)
/* harmony export */ });
function idGetter(e) {
    return e.id;
}


/***/ })

}]);
//# sourceMappingURL=elkdisplay.08d92926f5b2f061e67d.js.map?v=08d92926f5b2f061e67d