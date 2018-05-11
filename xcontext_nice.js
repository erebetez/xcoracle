if (!console) var console = {
    log: function() {},
    dir: function() {},
    time: function() {},
    trace: function() {}
};
ZenController = function() {
    function ZenController() {
        if (ZenController.SELF instanceof ZenController) throw "ZenController MUST NOT be instantiate more than once";
        ZenController.SELF = this;
        this.setApiKey();
    };
    ZenController.API_ROOT = null;
    ZenController.VERSIONS = {};
    ZenController.LOAD_PLAN = {};
    ZenController.STATE_COOKIES = null;
    ZenController._AUTH_DATA_ = null;
    ZenController.prototype = {
        API_KEY: null,
        _googleMapsApiKey: null,
        authSeed: null,
        authData: null,
        authTime: null,
        _isAuthCheckRunning: false,
        setApiKey: function() {
            var scripts = document.getElementsByTagName('script');
            var src = scripts[scripts.length - 1].src;
            var key = src.substr(src.indexOf("key=") + 4, 50);
            this.API_KEY = key;
        },
        googleMapsApiKey: function() {
            if (!this._googleMapsApiKey) {
                for (var i = 0; i < this.Loader.runQueue.length; i++) {
                    var q = this.Loader.runQueue[i];
                    if (q.options && q.options.global && q.options.global.googleMapsApiKey) {
                        this._googleMapsApiKey = q.options.global.googleMapsApiKey;
                        break;
                    };
                };
            };
            return this._googleMapsApiKey;
        },
        run: function(typeIdent, options, node, actionGadgets) {
            this.Loader.run(typeIdent, options, node, actionGadgets);
        },
        triggerRun: function(typeIdent, options, node) {
            throw "ZenController.triggerRun() MUST be overwritten";
        },
        Loader: {
            loadedMods: {},
            runQueue: [],
            modQueue: {},
            run: function(typeIdent, options, node, actionGadgets) {
                var needQueue = this._isAuthCheckRunning ? true : false;
                var loadPlan = ZenController.LOAD_PLAN.basic.concat(ZenController.LOAD_PLAN.extra[typeIdent] || []);
                for (var i = 0; i < loadPlan.length; i++) {
                    var module = loadPlan[i];
                    var modLS = this.loadedMods[module];
                    if (modLS) continue;
                    if (typeof(modLS) == "undefined") {
                        this.loadModule(module);
                        this.loadedMods[module] = false;
                    };
                    needQueue = true;
                };
                if (needQueue) {
                    this.runQueue.push({
                        loadPlan: loadPlan,
                        typeIdent: typeIdent,
                        options: options,
                        node: node,
                        actionGadgets: actionGadgets
                    });
                } else {
                    ZenController.SELF.triggerRun(typeIdent, options, node, actionGadgets);
                };
            },
            loadScript: function(props, onloadHandler, doc) {
                if (typeof props != "object") throw "Unable to create script";
                doc = doc ? doc : document;
                var script = doc.createElement('script');
                if (props.src) script.src = props.src;
                if (props.text) script.text = props.text;
                if (script.readyState) {
                    script.onreadystatechange = function() {
                        if (script.readyState != "loaded" && script.readyState != "complete") return;
                        script.onreadystatechange = null;
                        if (typeof onloadHandler == "function") onloadHandler(this);
                    };
                } else {
                    script.onload = function() {
                        if (typeof onloadHandler == "function") onloadHandler(this);
                    };
                };
                script.type = "text/javascript";
                doc.getElementsByTagName('head')[0].appendChild(script);
            },
            loadModule: function(module) {
                if (!ZenController.VERSIONS.modules[module]) throw "Module '" + module + "' is not defined";
                var src = (ZenController.API_ROOT + 'js/?&mod={mod}&key={key}&v={version}').replace(/\{mod\}/, module).replace(/\{key\}/, ZenController.SELF.API_KEY).replace(/\{version\}/, ZenController.VERSIONS.modules[module]);
                this.loadScript({
                    src: src
                }, function() {
                    ZenController.SELF.Loader.onLoadModule(module);
                });
            },
            onLoadModule: function(module) {
                this.loadedMods[module] = true;
                this.checkRun();
            },
            checkRun: function() {
                if (this._isAuthCheckRunning) return;
                var needRemove = [];
                for (var i = 0; i < this.runQueue.length; i++) {
                    var rQ = this.runQueue[i];
                    var loadPlan = rQ.loadPlan;
                    var isLoaded = true;
                    for (var j = 0; j < loadPlan.length; j++) {
                        if (this.loadedMods[loadPlan[j]]) continue;
                        isLoaded = false;
                        break;
                    };
                    if (isLoaded) {
                        for (var j = 0; j < loadPlan.length; j++) {
                            module = loadPlan[j];
                            if (!this.modQueue[module]) continue;
                            for (var k = 0; k < this.modQueue[module].length; k++) {
                                this.modQueue[module][k]();
                            };
                            delete this.modQueue[module];
                        };
                        ZenController.SELF.triggerRun(rQ.typeIdent, rQ.options, rQ.node, rQ.actionGadgets);
                        needRemove.push(i);
                    };
                };
                var removed = 0;
                for (var i = 0; i < needRemove.length; i++) {
                    this.runQueue.splice((needRemove[i] - removed), 1);
                    removed++;
                };
            },
            queue: function(module, func) {
                if (!this.modQueue[module]) this.modQueue[module] = [];
                this.modQueue[module].push(func);
            }
        },
        checkAuthWndName: function() {
            try {
                eval("var wnData = " + window.name);
                ZenController.STATE_COOKIES = wnData.STATE_COOKIES;
                SELF.authSeed = wnData.authSeed;
                SELF.authData = wnData.authData;
                window.name = '';
                return true;
            } catch (e) {
                return false;
            };
        },
        checkAuth: function() {
            var SELF = this;
            if (ZenController.STATE_COOKIES == 'ok') {
                SELF.authData = ZenController._AUTH_DATA_;
                ZenController._AUTH_DATA_ = null;
                return;
            };
            if (ZenController.STATE_COOKIES === null && window.name) {
                if (this.checkAuthWndName()) return;
            }
            var url = (ZenController.API_ROOT + 'auth/check/?key={key}').replace(/\{key\}/, ZenController.SELF.API_KEY);
            this._isAuthCheckRunning = true;
            this.Loader.loadScript({
                src: url
            }, function() {
                if (ZenController.STATE_COOKIES === null && window.name) {
                    if (!this.checkAuthWndName()) throw "checkAuth invalid. Javascript code (other than XContest API) possibly use window.name property.";
                };
                this._isAuthCheckRunning = false;
                this.checkRun();
            });
        }
    };
    return ZenController;
}();
ZenController.VERSIONS = {
    "modules": {
        "contest": "2.5.20",
        "flight": "2.5.12",
        "map": "2.5.7"
    },
    "css": "2.5.10",
    "lng": "2.5.8"
};
ZenController.LOAD_PLAN = {
    "basic": ["contest"],
    "extra": {
        "flight": ["flight"],
        "flight_multi": ["flight"],
        "livetrack_multi": ["flight"],
        "map": ["map"]
    }
};
ZenController.API_ROOT = "https://www.xcontest.org/api/";
ZenController.STATE_COOKIES = "ok";
ZenController._AUTH_DATA_ = {
    "isLogged": false
};
var XContest = new ZenController;
XContest.checkAuth();
XContest.content = function(league) {
    XContest.Loader.queue("contest", function() {
        XContest.startLoadContent(league);
    });
};