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
		client: {"start":"_app/immutable/entry/start.JcPQkdmu.js","app":"_app/immutable/entry/app.Er3JC-rf.js","imports":["_app/immutable/entry/start.JcPQkdmu.js","_app/immutable/chunks/entry.C-y9X2td.js","_app/immutable/chunks/scheduler.xQsDa6L3.js","_app/immutable/entry/app.Er3JC-rf.js","_app/immutable/chunks/preload-helper.D6kgxu3v.js","_app/immutable/chunks/scheduler.xQsDa6L3.js","_app/immutable/chunks/index.lnKugwF0.js"],"stylesheets":[],"fonts":[],"uses_env_dynamic_public":false},
		nodes: [
			__memo(() => import('./chunks/0-CMXy4SJy.js')),
			__memo(() => import('./chunks/1-hsKzFefQ.js')),
			__memo(() => import('./chunks/2-Ax4bcEC3.js').then(function (n) { return n._; }))
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
