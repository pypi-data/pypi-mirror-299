const __vite__fileDeps=["./vega-embed.module-sBY_gVL0.js","./index-rhD_mH1q.js","./index-CXT-o_Mx.css","./dsv-DB8NKgIY.js"],__vite__mapDeps=i=>i.map(i=>__vite__fileDeps[i]);
import{_ as Le}from"./index-rhD_mH1q.js";import{B as Te}from"./Block--xuAGeyl.js";import{B as Ve}from"./BlockTitle-BFisnzlz.js";import"./IconButtonWrapper.svelte_svelte_type_style_lang-Cdolb8gF.js";import{E as je}from"./Empty-D-VJ_RsP.js";import{L as Ie}from"./LineChart-CKh1Fdep.js";import{S as Be}from"./index-BjSxOpmL.js";import"./StreamingBar.svelte_svelte_type_style_lang-hwxd5zZk.js";import"./svelte/svelte.js";import"./Info-CU8DPF6R.js";import"./IconButton-DBg6YGHG.js";import"./Clear-By3xiIwg.js";const{SvelteComponent:De,append:Ne,assign:qe,attr:we,binding_callbacks:Me,check_outros:he,create_component:B,destroy_component:D,detach:E,element:ve,empty:Fe,flush:u,get_spread_object:Re,get_spread_update:He,group_outros:be,init:Ue,insert:O,mount_component:N,noop:ye,safe_not_equal:Xe,set_data:Pe,space:le,text:ze,transition_in:k,transition_out:F}=window.__gradio__svelte__internal,{onMount:Ye}=window.__gradio__svelte__internal;function xe(r){let e,t;const i=[{autoscroll:r[2].autoscroll},{i18n:r[2].i18n},r[10]];let n={};for(let s=0;s<i.length;s+=1)n=qe(n,i[s]);return e=new Be({props:n}),e.$on("clear_status",r[38]),{c(){B(e.$$.fragment)},m(s,_){N(e,s,_),t=!0},p(s,_){const m=_[0]&1028?He(i,[_[0]&4&&{autoscroll:s[2].autoscroll},_[0]&4&&{i18n:s[2].i18n},_[0]&1024&&Re(s[10])]):{};e.$set(m)},i(s){t||(k(e.$$.fragment,s),t=!0)},o(s){F(e.$$.fragment,s),t=!1},d(s){D(e,s)}}}function Ge(r){let e;return{c(){e=ze(r[3])},m(t,i){O(t,e,i)},p(t,i){i[0]&8&&Pe(e,t[3])},d(t){t&&E(e)}}}function Je(r){let e,t;return e=new je({props:{unpadded_box:!0,$$slots:{default:[Qe]},$$scope:{ctx:r}}}),{c(){B(e.$$.fragment)},m(i,n){N(e,i,n),t=!0},p(i,n){const s={};n[1]&8388608&&(s.$$scope={dirty:n,ctx:i}),e.$set(s)},i(i){t||(k(e.$$.fragment,i),t=!0)},o(i){F(e.$$.fragment,i),t=!1},d(i){D(e,i)}}}function Ke(r){let e,t,i,n=r[1]&&ke(r);return{c(){e=ve("div"),t=le(),n&&n.c(),i=Fe(),we(e,"class","svelte-10k9m4v")},m(s,_){O(s,e,_),r[39](e),O(s,t,_),n&&n.m(s,_),O(s,i,_)},p(s,_){s[1]?n?n.p(s,_):(n=ke(s),n.c(),n.m(i.parentNode,i)):n&&(n.d(1),n=null)},i:ye,o:ye,d(s){s&&(E(e),E(t),E(i)),r[39](null),n&&n.d(s)}}}function Qe(r){let e,t;return e=new Ie({}),{c(){B(e.$$.fragment)},m(i,n){N(e,i,n),t=!0},i(i){t||(k(e.$$.fragment,i),t=!0)},o(i){F(e.$$.fragment,i),t=!1},d(i){D(e,i)}}}function ke(r){let e,t;return{c(){e=ve("p"),t=ze(r[1]),we(e,"class","caption svelte-10k9m4v")},m(i,n){O(i,e,n),Ne(e,t)},p(i,n){n[0]&2&&Pe(t,i[1])},d(i){i&&E(e)}}}function Ze(r){let e,t,i,n,s,_,m,a=r[10]&&xe(r);t=new Ve({props:{show_label:r[7],info:void 0,$$slots:{default:[Ge]},$$scope:{ctx:r}}});const g=[Ke,Je],c=[];function f(o,d){return o[0]&&o[13]?0:1}return n=f(r),s=c[n]=g[n](r),{c(){a&&a.c(),e=le(),B(t.$$.fragment),i=le(),s.c(),_=Fe()},m(o,d){a&&a.m(o,d),O(o,e,d),N(t,o,d),O(o,i,d),c[n].m(o,d),O(o,_,d),m=!0},p(o,d){o[10]?a?(a.p(o,d),d[0]&1024&&k(a,1)):(a=xe(o),a.c(),k(a,1),a.m(e.parentNode,e)):a&&(be(),F(a,1,1,()=>{a=null}),he());const P={};d[0]&128&&(P.show_label=o[7]),d[0]&8|d[1]&8388608&&(P.$$scope={dirty:d,ctx:o}),t.$set(P);let W=n;n=f(o),n===W?c[n].p(o,d):(be(),F(c[W],1,1,()=>{c[W]=null}),he(),s=c[n],s?s.p(o,d):(s=c[n]=g[n](o),s.c()),k(s,1),s.m(_.parentNode,_))},i(o){m||(k(a),k(t.$$.fragment,o),k(s),m=!0)},o(o){F(a),F(t.$$.fragment,o),F(s),m=!1},d(o){o&&(E(e),E(i),E(_)),a&&a.d(o),D(t,o),c[n].d(o)}}}function pe(r){let e,t;return e=new Te({props:{visible:r[6],elem_id:r[4],elem_classes:r[5],scale:r[8],min_width:r[9],allow_overflow:!1,padding:!0,height:r[11],$$slots:{default:[Ze]},$$scope:{ctx:r}}}),{c(){B(e.$$.fragment)},m(i,n){N(e,i,n),t=!0},p(i,n){const s={};n[0]&64&&(s.visible=i[6]),n[0]&16&&(s.elem_id=i[4]),n[0]&32&&(s.elem_classes=i[5]),n[0]&256&&(s.scale=i[8]),n[0]&512&&(s.min_width=i[9]),n[0]&2048&&(s.height=i[11]),n[0]&5263|n[1]&8388608&&(s.$$scope={dirty:n,ctx:i}),e.$set(s)},i(i){t||(k(e.$$.fragment,i),t=!0)},o(i){F(e.$$.fragment,i),t=!1},d(i){D(e,i)}}}function $e(r,e,t){let i,n,s,_,m,{value:a}=e,{x:g}=e,{y:c}=e,{color:f=null}=e,{title:o=null}=e,{x_title:d=null}=e,{y_title:P=null}=e,{color_title:W=null}=e,{x_bin:w=null}=e,{y_aggregate:j=void 0}=e,{color_map:q=null}=e,{x_lim:L=null}=e,{y_lim:M=null}=e,{x_label_angle:R=null}=e,{y_label_angle:H=null}=e,{caption:ie=null}=e,{sort:K=null}=e;function Se(l){if(l==="x")return"ascending";if(l==="-x")return"descending";if(l==="y")return{field:c,order:"ascending"};if(l==="-y")return{field:c,order:"descending"};if(l===null)return;if(Array.isArray(l))return l}let{_selectable:U=!1}=e,{target:X}=e,Y,{gradio:T}=e,z,Q=!1;const Ce={s:1,m:60,h:60*60,d:24*60*60};let I,V;function Ee(l){let h=l.columns.indexOf(g),C=l.columns.indexOf(c),x=f?l.columns.indexOf(f):null;return l.data.map(v=>{const b={[g]:v[h],[c]:v[C]};return f&&x!==null&&(b[f]=v[x]),b})}const ne=typeof window<"u";let y,S,Z=!1,se,G,p;async function re(){if(S&&S.finalize(),!a||!y)return;se=y.offsetWidth;const l=Oe();l&&(G=new ResizeObserver(h=>{!h[0].target||!(h[0].target instanceof HTMLElement)||(se===0&&y.offsetWidth!==0&&a.datatypes[g]==="nominal"?re():S.signal("width",h[0].target.offsetWidth).run())}),p||(p=(await Le(()=>import("./vega-embed.module-sBY_gVL0.js"),__vite__mapDeps([0,1,2,3]),import.meta.url)).default),p(y,l,{actions:!1}).then(function(h){S=h.view,G.observe(y);var C;S.addEventListener("dblclick",()=>{T.dispatch("double_click")}),y.addEventListener("mousedown",function(x){x.detail>1&&x.preventDefault()},!1),U&&S.addSignalListener("brush",function(x,v){if(Object.keys(v).length===0)return;clearTimeout(C);let b=v[Object.keys(v)[0]];s&&(b=[b[0]/1e3,b[1]/1e3]),Q?J=()=>{T.dispatch("select",{value:b,index:b,selected:!0})}:C=setTimeout(function(){T.dispatch("select",{value:b,index:b,selected:!0})},250)})}))}let J=null;Ye(()=>(t(35,Z=!0),y.addEventListener("mousedown",()=>{Q=!0}),y.addEventListener("mouseup",()=>{Q=!1,J&&(J(),J=null)}),()=>{t(35,Z=!1),S&&S.finalize(),G&&G.disconnect()}));function Oe(){if(!a||!m)return null;let l=m.getPropertyValue("--color-accent"),h=m.getPropertyValue("--body-text-color"),C=m.getPropertyValue("--border-color-primary"),x=m.fontFamily,v=m.getPropertyValue("--block-title-text-weight");const b=A=>A.endsWith("px")?parseFloat(A.slice(0,-2)):12;let ge=b(m.getPropertyValue("--text-md")),ee=b(m.getPropertyValue("--text-sm"));return{$schema:"https://vega.github.io/schema/vega-lite/v5.17.0.json",background:"transparent",config:{autosize:{type:"fit",contains:"padding"},axis:{labelFont:x,labelColor:h,titleFont:x,titleColor:h,titlePadding:8,tickColor:C,labelFontSize:ee,gridColor:C,titleFontWeight:"normal",titleFontSize:ee,labelFontWeight:"normal",domain:!1,labelAngle:0},legend:{labelColor:h,labelFont:x,titleColor:h,titleFont:x,titleFontWeight:"normal",titleFontSize:ee,labelFontWeight:"normal",offset:2},title:{color:h,font:x,fontSize:ge,fontWeight:v,anchor:"middle"},view:{stroke:C},mark:{stroke:a.mark!=="bar"?l:void 0,fill:a.mark==="bar"?l:void 0,cursor:"crosshair"}},data:{name:"data"},datasets:{data:Y},layer:["plot",...a.mark==="line"?["hover"]:[]].map(A=>({encoding:{size:a.mark==="line"?A=="plot"?{condition:{empty:!1,param:"hoverPlot",value:3},value:2}:{condition:{empty:!1,param:"hover",value:100},value:0}:void 0,opacity:A==="plot"?void 0:{condition:{empty:!1,param:"hover",value:1},value:0},x:{axis:R?{labelAngle:R}:{},field:g,title:d||g,type:a.datatypes[g],scale:_?{domain:_}:void 0,bin:z?{step:z}:void 0,sort:n},y:{axis:H?{labelAngle:H}:{},field:c,title:P||c,type:a.datatypes[c],scale:M?{domain:M}:void 0,aggregate:V?I:void 0},color:f?{field:f,legend:{orient:"bottom",title:W},scale:a.datatypes[f]==="nominal"?{domain:i,range:q?i.map(te=>q[te]):void 0}:{range:[100,200,300,400,500,600,700,800,900].map(te=>m.getPropertyValue("--primary-"+te)),interpolate:"hsl"},type:a.datatypes[f]}:void 0,tooltip:[{field:c,type:a.datatypes[c],aggregate:V?I:void 0,title:P||c},{field:g,type:a.datatypes[g],title:d||g,format:s?"%Y-%m-%d %H:%M:%S":void 0,bin:z?{step:z}:void 0},...f?[{field:f,type:a.datatypes[f]}]:[]]},strokeDash:{},mark:{clip:!0,type:A==="hover"?"point":a.mark},name:A})),params:[...a.mark==="line"?[{name:"hoverPlot",select:{clear:"mouseout",fields:f?[f]:[],nearest:!0,on:"mouseover",type:"point"},views:["hover"]},{name:"hover",select:{clear:"mouseout",nearest:!0,on:"mouseover",type:"point"},views:["hover"]}]:[],...U?[{name:"brush",select:{encodings:["x"],mark:{fill:"gray",fillOpacity:.3,stroke:"none"},type:"interval"},views:["plot"]}]:[]],width:y.offsetWidth,title:o||void 0}}let{label:ae="Textbox"}=e,{elem_id:oe=""}=e,{elem_classes:ue=[]}=e,{visible:_e=!0}=e,{show_label:ce}=e,{scale:fe=null}=e,{min_width:de=void 0}=e,{loading_status:$=void 0}=e,{height:me=void 0}=e;const We=()=>T.dispatch("clear_status",$);function Ae(l){Me[l?"unshift":"push"](()=>{y=l,t(12,y)})}return r.$$set=l=>{"value"in l&&t(0,a=l.value),"x"in l&&t(14,g=l.x),"y"in l&&t(15,c=l.y),"color"in l&&t(16,f=l.color),"title"in l&&t(17,o=l.title),"x_title"in l&&t(18,d=l.x_title),"y_title"in l&&t(19,P=l.y_title),"color_title"in l&&t(20,W=l.color_title),"x_bin"in l&&t(21,w=l.x_bin),"y_aggregate"in l&&t(22,j=l.y_aggregate),"color_map"in l&&t(23,q=l.color_map),"x_lim"in l&&t(24,L=l.x_lim),"y_lim"in l&&t(25,M=l.y_lim),"x_label_angle"in l&&t(26,R=l.x_label_angle),"y_label_angle"in l&&t(27,H=l.y_label_angle),"caption"in l&&t(1,ie=l.caption),"sort"in l&&t(28,K=l.sort),"_selectable"in l&&t(29,U=l._selectable),"target"in l&&t(30,X=l.target),"gradio"in l&&t(2,T=l.gradio),"label"in l&&t(3,ae=l.label),"elem_id"in l&&t(4,oe=l.elem_id),"elem_classes"in l&&t(5,ue=l.elem_classes),"visible"in l&&t(6,_e=l.visible),"show_label"in l&&t(7,ce=l.show_label),"scale"in l&&t(8,fe=l.scale),"min_width"in l&&t(9,de=l.min_width),"loading_status"in l&&t(10,$=l.loading_status),"height"in l&&t(11,me=l.height)},r.$$.update=()=>{r.$$.dirty[0]&1&&t(31,Y=a?Ee(a):[]),r.$$.dirty[0]&65537|r.$$.dirty[1]&1&&(i=f&&a&&a.datatypes[f]==="nominal"?Array.from(new Set(Y.map(l=>l[f]))):[]),r.$$.dirty[0]&268435456&&(n=Se(K)),r.$$.dirty[0]&16385&&t(36,s=a&&a.datatypes[g]==="temporal"),r.$$.dirty[0]&16777216|r.$$.dirty[1]&32&&(_=L&&s?[L[0]*1e3,L[1]*1e3]:L),r.$$.dirty[0]&2097152&&t(32,z=w?typeof w=="string"?1e3*parseInt(w.substring(0,w.length-1))*Ce[w[w.length-1]]:w:void 0),r.$$.dirty[0]&4210689|r.$$.dirty[1]&10&&a&&(a.mark==="point"?(t(34,V=z!==void 0),t(33,I=j||V?"sum":void 0)):(t(34,V=z!==void 0||a.datatypes[g]==="nominal"),t(33,I=j||"sum"))),r.$$.dirty[0]&1073741824&&t(37,m=X&&ne?window.getComputedStyle(X):null),r.$$.dirty[0]&331337731|r.$$.dirty[1]&84&&m&&requestAnimationFrame(re)},[a,ie,T,ae,oe,ue,_e,ce,fe,de,$,me,y,ne,g,c,f,o,d,P,W,w,j,q,L,M,R,H,K,U,X,Y,z,I,V,Z,s,m,We,Ae]}class ft extends De{constructor(e){super(),Ue(this,e,$e,pe,Xe,{value:0,x:14,y:15,color:16,title:17,x_title:18,y_title:19,color_title:20,x_bin:21,y_aggregate:22,color_map:23,x_lim:24,y_lim:25,x_label_angle:26,y_label_angle:27,caption:1,sort:28,_selectable:29,target:30,gradio:2,label:3,elem_id:4,elem_classes:5,visible:6,show_label:7,scale:8,min_width:9,loading_status:10,height:11},null,[-1,-1])}get value(){return this.$$.ctx[0]}set value(e){this.$$set({value:e}),u()}get x(){return this.$$.ctx[14]}set x(e){this.$$set({x:e}),u()}get y(){return this.$$.ctx[15]}set y(e){this.$$set({y:e}),u()}get color(){return this.$$.ctx[16]}set color(e){this.$$set({color:e}),u()}get title(){return this.$$.ctx[17]}set title(e){this.$$set({title:e}),u()}get x_title(){return this.$$.ctx[18]}set x_title(e){this.$$set({x_title:e}),u()}get y_title(){return this.$$.ctx[19]}set y_title(e){this.$$set({y_title:e}),u()}get color_title(){return this.$$.ctx[20]}set color_title(e){this.$$set({color_title:e}),u()}get x_bin(){return this.$$.ctx[21]}set x_bin(e){this.$$set({x_bin:e}),u()}get y_aggregate(){return this.$$.ctx[22]}set y_aggregate(e){this.$$set({y_aggregate:e}),u()}get color_map(){return this.$$.ctx[23]}set color_map(e){this.$$set({color_map:e}),u()}get x_lim(){return this.$$.ctx[24]}set x_lim(e){this.$$set({x_lim:e}),u()}get y_lim(){return this.$$.ctx[25]}set y_lim(e){this.$$set({y_lim:e}),u()}get x_label_angle(){return this.$$.ctx[26]}set x_label_angle(e){this.$$set({x_label_angle:e}),u()}get y_label_angle(){return this.$$.ctx[27]}set y_label_angle(e){this.$$set({y_label_angle:e}),u()}get caption(){return this.$$.ctx[1]}set caption(e){this.$$set({caption:e}),u()}get sort(){return this.$$.ctx[28]}set sort(e){this.$$set({sort:e}),u()}get _selectable(){return this.$$.ctx[29]}set _selectable(e){this.$$set({_selectable:e}),u()}get target(){return this.$$.ctx[30]}set target(e){this.$$set({target:e}),u()}get gradio(){return this.$$.ctx[2]}set gradio(e){this.$$set({gradio:e}),u()}get label(){return this.$$.ctx[3]}set label(e){this.$$set({label:e}),u()}get elem_id(){return this.$$.ctx[4]}set elem_id(e){this.$$set({elem_id:e}),u()}get elem_classes(){return this.$$.ctx[5]}set elem_classes(e){this.$$set({elem_classes:e}),u()}get visible(){return this.$$.ctx[6]}set visible(e){this.$$set({visible:e}),u()}get show_label(){return this.$$.ctx[7]}set show_label(e){this.$$set({show_label:e}),u()}get scale(){return this.$$.ctx[8]}set scale(e){this.$$set({scale:e}),u()}get min_width(){return this.$$.ctx[9]}set min_width(e){this.$$set({min_width:e}),u()}get loading_status(){return this.$$.ctx[10]}set loading_status(e){this.$$set({loading_status:e}),u()}get height(){return this.$$.ctx[11]}set height(e){this.$$set({height:e}),u()}}export{ft as default};
//# sourceMappingURL=Index-DRLEO22V.js.map
