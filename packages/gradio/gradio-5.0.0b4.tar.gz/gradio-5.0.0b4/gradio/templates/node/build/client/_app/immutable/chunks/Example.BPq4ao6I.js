import{s as I,z as m,i as b,f as _,e as k,t as q,c as V,b as E,d as w,h as D,j as S,n as v,r as j,a0 as y,p as z,q as c,L as A}from"./scheduler.xQsDa6L3.js";import{S as C,i as L,t as d,g as N,b as p,e as B,f as F,c as G,a as H,m as J,d as K}from"./index.lnKugwF0.js";import{V as M}from"./Video.BpynpsrS.js";import"./2.Bbgn9Xo5.js";function g(o){let e,l,t,n;const f=[P,O],u=[];function s(a,i){return 0}return e=s(),l=u[e]=f[e](o),{c(){l.c(),t=m()},l(a){l.l(a),t=m()},m(a,i){u[e].m(a,i),b(a,t,i),n=!0},p(a,i){l.p(a,i)},i(a){n||(d(l),n=!0)},o(a){p(l),n=!1},d(a){a&&_(t),u[e].d(a)}}}function O(o){let e,l;return{c(){e=k("div"),l=q(o[2])},l(t){e=V(t,"DIV",{});var n=E(e);l=w(n,o[2]),n.forEach(_)},m(t,n){b(t,e,n),D(e,l)},p(t,n){n&4&&S(l,t[2])},i:v,o:v,d(t){t&&_(e)}}}function P(o){var s;let e,l,t,n;function f(a){o[6](a)}let u={muted:!0,playsinline:!0,src:(s=o[2])==null?void 0:s.video.url,is_stream:!1,loop:o[3]};return o[4]!==void 0&&(u.node=o[4]),l=new M({props:u}),j.push(()=>F(l,"node",f)),l.$on("loadeddata",o[5]),l.$on("mouseover",function(){y(o[4].play.bind(o[4]))&&o[4].play.bind(o[4]).apply(this,arguments)}),l.$on("mouseout",function(){y(o[4].pause.bind(o[4]))&&o[4].pause.bind(o[4]).apply(this,arguments)}),{c(){e=k("div"),G(l.$$.fragment),this.h()},l(a){e=V(a,"DIV",{class:!0});var i=E(e);H(l.$$.fragment,i),i.forEach(_),this.h()},h(){z(e,"class","container svelte-13u05e4"),c(e,"table",o[0]==="table"),c(e,"gallery",o[0]==="gallery"),c(e,"selected",o[1])},m(a,i){b(a,e,i),J(l,e,null),n=!0},p(a,i){var h;o=a;const r={};i&4&&(r.src=(h=o[2])==null?void 0:h.video.url),i&8&&(r.loop=o[3]),!t&&i&16&&(t=!0,r.node=o[4],A(()=>t=!1)),l.$set(r),(!n||i&1)&&c(e,"table",o[0]==="table"),(!n||i&1)&&c(e,"gallery",o[0]==="gallery"),(!n||i&2)&&c(e,"selected",o[1])},i(a){n||(d(l.$$.fragment,a),n=!0)},o(a){p(l.$$.fragment,a),n=!1},d(a){a&&_(e),K(l)}}}function Q(o){let e,l,t=o[2]&&g(o);return{c(){t&&t.c(),e=m()},l(n){t&&t.l(n),e=m()},m(n,f){t&&t.m(n,f),b(n,e,f),l=!0},p(n,[f]){n[2]?t?(t.p(n,f),f&4&&d(t,1)):(t=g(n),t.c(),d(t,1),t.m(e.parentNode,e)):t&&(N(),p(t,1,1,()=>{t=null}),B())},i(n){l||(d(t),l=!0)},o(n){p(t),l=!1},d(n){n&&_(e),t&&t.d(n)}}}function R(o,e,l){let{type:t}=e,{selected:n=!1}=e,{value:f}=e,{loop:u}=e,s;async function a(){l(4,s.muted=!0,s),l(4,s.playsInline=!0,s),l(4,s.controls=!1,s),s.setAttribute("muted",""),await s.play(),s.pause()}function i(r){s=r,l(4,s)}return o.$$set=r=>{"type"in r&&l(0,t=r.type),"selected"in r&&l(1,n=r.selected),"value"in r&&l(2,f=r.value),"loop"in r&&l(3,u=r.loop)},[t,n,f,u,s,a,i]}class Y extends C{constructor(e){super(),L(this,e,R,Q,I,{type:0,selected:1,value:2,loop:3})}}export{Y as default};
