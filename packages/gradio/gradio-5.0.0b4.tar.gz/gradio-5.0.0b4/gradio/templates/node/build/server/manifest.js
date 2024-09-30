const manifest = (() => {
function __memo(fn) {
	let value;
	return () => value ??= (value = fn());
}

return {
	appDir: "_app",
	appPath: "_app",
	assets: new Set(["favicon.png"]),
	mimeTypes: {".png":"image/png"},
	_: {
		client: {"start":"_app/immutable/entry/start.DWfhZiPL.js","app":"_app/immutable/entry/app.D0fdl4zd.js","imports":["_app/immutable/entry/start.DWfhZiPL.js","_app/immutable/chunks/entry.CrGqrYiV.js","_app/immutable/chunks/scheduler.xQsDa6L3.js","_app/immutable/entry/app.D0fdl4zd.js","_app/immutable/chunks/preload-helper.D6kgxu3v.js","_app/immutable/chunks/scheduler.xQsDa6L3.js","_app/immutable/chunks/index.lnKugwF0.js"],"stylesheets":[],"fonts":[],"uses_env_dynamic_public":false},
		nodes: [
			__memo(() => import('./chunks/0-BM_k8tv8.js')),
			__memo(() => import('./chunks/1-CsXz-_4E.js')),
			__memo(() => import('./chunks/2-DpTvHskm.js').then(function (n) { return n._; }))
		],
		routes: [
			{
				id: "/[...catchall]",
				pattern: /^(?:\/(.*))?\/?$/,
				params: [{"name":"catchall","optional":false,"rest":true,"chained":true}],
				page: { layouts: [0,], errors: [1,], leaf: 2 },
				endpoint: null
			}
		],
		matchers: async () => {
			
			return {  };
		},
		server_assets: {}
	}
}
})();

const prerendered = new Set([]);

const base = "";

export { base, manifest, prerendered };
//# sourceMappingURL=manifest.js.map
