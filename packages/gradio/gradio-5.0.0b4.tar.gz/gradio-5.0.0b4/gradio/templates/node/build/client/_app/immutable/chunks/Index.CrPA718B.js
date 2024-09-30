import{s as ne,v as de,w as me,b as L,f as d,p as _,i as y,h as H,n as le,e as C,c as A,y as el,a as D,g as R,Q as ee,T as ce,t as W,d as X,j as te,F as I,R as $,z,q as j,E as U,J as Dl,r as ge,L as be,B as ll}from"./scheduler.xQsDa6L3.js";import{S as oe,i as ie,g as Q,b as N,e as Y,t as w,f as ke,c as q,a as Z,m as J,d as K}from"./index.lnKugwF0.js";import{t as ve,f as F,B as tl,d as nl,b as ol,e as il}from"./2.Bbgn9Xo5.js";import{g as sl}from"./color.Dwea8QME.js";import{B as rl}from"./BlockLabel.EPnqKJ7A.js";import{E as al}from"./Empty.cyjo30Lv.js";function Rl(t){let e,n,l;return{c(){e=de("svg"),n=de("path"),l=de("path"),this.h()},l(o){e=me(o,"svg",{xmlns:!0,"xmlns:xlink":!0,"aria-hidden":!0,role:!0,class:!0,width:!0,height:!0,preserveAspectRatio:!0,viewBox:!0});var s=L(e);n=me(s,"path",{fill:!0,d:!0}),L(n).forEach(d),l=me(s,"path",{fill:!0,d:!0}),L(l).forEach(d),s.forEach(d),this.h()},h(){_(n,"fill","currentColor"),_(n,"d","M12 15H5a3 3 0 0 1-3-3v-2a3 3 0 0 1 3-3h5V5a1 1 0 0 0-1-1H3V2h6a3 3 0 0 1 3 3zM5 9a1 1 0 0 0-1 1v2a1 1 0 0 0 1 1h5V9zm15 14v2a1 1 0 0 0 1 1h5v-4h-5a1 1 0 0 0-1 1z"),_(l,"fill","currentColor"),_(l,"d","M2 30h28V2Zm26-2h-7a3 3 0 0 1-3-3v-2a3 3 0 0 1 3-3h5v-2a1 1 0 0 0-1-1h-6v-2h6a3 3 0 0 1 3 3Z"),_(e,"xmlns","http://www.w3.org/2000/svg"),_(e,"xmlns:xlink","http://www.w3.org/1999/xlink"),_(e,"aria-hidden","true"),_(e,"role","img"),_(e,"class","iconify iconify--carbon"),_(e,"width","100%"),_(e,"height","100%"),_(e,"preserveAspectRatio","xMidYMid meet"),_(e,"viewBox","0 0 32 32")},m(o,s){y(o,e,s),H(e,n),H(e,l)},p:le,i:le,o:le,d(o){o&&d(e)}}}class _e extends oe{constructor(e){super(),ie(this,e,null,Rl,ne,{})}}function pe(t,e,n){if(!n){var l=document.createElement("canvas");n=l.getContext("2d")}n.fillStyle=t,n.fillRect(0,0,1,1);const[o,s,i]=n.getImageData(0,0,1,1).data;return n.clearRect(0,0,1,1),`rgba(${o}, ${s}, ${i}, ${255/e})`}function fl(t,e,n,l){for(const o in t){const s=t[o].trim();s in ve?e[o]=ve[s]:e[o]={primary:n?pe(t[o],1,l):t[o],secondary:n?pe(t[o],.5,l):t[o]}}}function ul(t,e){let n=[],l=null,o=null;for(const s of t)o===s.class_or_confidence?l=l?l+s.token:s.token:(l!==null&&n.push({token:l,class_or_confidence:o}),l=s.token,o=s.class_or_confidence);return l!==null&&n.push({token:l,class_or_confidence:o}),n}function we(t,e,n){const l=t.slice();l[18]=e[n];const o=typeof l[18].class_or_confidence=="string"?parseInt(l[18].class_or_confidence):l[18].class_or_confidence;return l[27]=o,l}function ye(t,e,n){const l=t.slice();return l[18]=e[n],l[20]=n,l}function Ee(t,e,n){const l=t.slice();return l[21]=e[n],l[23]=n,l}function Se(t,e,n){const l=t.slice();return l[24]=e[n][0],l[25]=e[n][1],l[20]=n,l}function zl(t){let e,n,l=t[1]&&Ne(),o=F(t[0]),s=[];for(let i=0;i<o.length;i+=1)s[i]=Ie(we(t,o,i));return{c(){l&&l.c(),e=D(),n=C("div");for(let i=0;i<s.length;i+=1)s[i].c();this.h()},l(i){l&&l.l(i),e=R(i),n=A(i,"DIV",{class:!0,"data-testid":!0});var a=L(n);for(let r=0;r<s.length;r+=1)s[r].l(a);a.forEach(d),this.h()},h(){_(n,"class","textfield svelte-1woixh4"),_(n,"data-testid","highlighted-text:textfield")},m(i,a){l&&l.m(i,a),y(i,e,a),y(i,n,a);for(let r=0;r<s.length;r+=1)s[r]&&s[r].m(n,null)},p(i,a){if(i[1]?l||(l=Ne(),l.c(),l.m(e.parentNode,e)):l&&(l.d(1),l=null),a&1){o=F(i[0]);let r;for(r=0;r<o.length;r+=1){const u=we(i,o,r);s[r]?s[r].p(u,a):(s[r]=Ie(u),s[r].c(),s[r].m(n,null))}for(;r<s.length;r+=1)s[r].d(1);s.length=o.length}},d(i){i&&(d(e),d(n)),l&&l.d(i),ee(s,i)}}}function Fl(t){let e,n,l=t[1]&&Ve(t),o=F(t[0]),s=[];for(let i=0;i<o.length;i+=1)s[i]=Le(ye(t,o,i));return{c(){l&&l.c(),e=D(),n=C("div");for(let i=0;i<s.length;i+=1)s[i].c();this.h()},l(i){l&&l.l(i),e=R(i),n=A(i,"DIV",{class:!0});var a=L(n);for(let r=0;r<s.length;r+=1)s[r].l(a);a.forEach(d),this.h()},h(){_(n,"class","textfield svelte-1woixh4")},m(i,a){l&&l.m(i,a),y(i,e,a),y(i,n,a);for(let r=0;r<s.length;r+=1)s[r]&&s[r].m(n,null)},p(i,a){if(i[1]?l?l.p(i,a):(l=Ve(i),l.c(),l.m(e.parentNode,e)):l&&(l.d(1),l=null),a&223){o=F(i[0]);let r;for(r=0;r<o.length;r+=1){const u=ye(i,o,r);s[r]?s[r].p(u,a):(s[r]=Le(u),s[r].c(),s[r].m(n,null))}for(;r<s.length;r+=1)s[r].d(1);s.length=o.length}},d(i){i&&(d(e),d(n)),l&&l.d(i),ee(s,i)}}}function Ne(t){let e,n="<span>-1</span> <span>0</span> <span>+1</span>";return{c(){e=C("div"),e.innerHTML=n,this.h()},l(l){e=A(l,"DIV",{class:!0,"data-testid":!0,"data-svelte-h":!0}),ce(e)!=="svelte-mv3vmx"&&(e.innerHTML=n),this.h()},h(){_(e,"class","color-legend svelte-1woixh4"),_(e,"data-testid","highlighted-text:color-legend")},m(l,o){y(l,e,o)},d(l){l&&d(e)}}}function Ie(t){let e,n,l=t[18].token+"",o,s,i;return{c(){e=C("span"),n=C("span"),o=W(l),s=D(),this.h()},l(a){e=A(a,"SPAN",{class:!0,style:!0});var r=L(e);n=A(r,"SPAN",{class:!0});var u=L(n);o=X(u,l),u.forEach(d),s=R(r),r.forEach(d),this.h()},h(){_(n,"class","text svelte-1woixh4"),_(e,"class","textspan score-text svelte-1woixh4"),_(e,"style",i="background-color: rgba("+(t[27]&&t[27]<0?"128, 90, 213,"+-t[27]:"239, 68, 60,"+t[27])+")")},m(a,r){y(a,e,r),H(e,n),H(n,o),H(e,s)},p(a,r){r&1&&l!==(l=a[18].token+"")&&te(o,l),r&1&&i!==(i="background-color: rgba("+(a[27]&&a[27]<0?"128, 90, 213,"+-a[27]:"239, 68, 60,"+a[27])+")")&&_(e,"style",i)},d(a){a&&d(e)}}}function Ve(t){let e,n=F(Object.entries(t[6])),l=[];for(let o=0;o<n.length;o+=1)l[o]=Te(Se(t,n,o));return{c(){e=C("div");for(let o=0;o<l.length;o+=1)l[o].c();this.h()},l(o){e=A(o,"DIV",{class:!0,"data-testid":!0});var s=L(e);for(let i=0;i<l.length;i+=1)l[i].l(s);s.forEach(d),this.h()},h(){_(e,"class","category-legend svelte-1woixh4"),_(e,"data-testid","highlighted-text:category-legend")},m(o,s){y(o,e,s);for(let i=0;i<l.length;i+=1)l[i]&&l[i].m(e,null)},p(o,s){if(s&832){n=F(Object.entries(o[6]));let i;for(i=0;i<n.length;i+=1){const a=Se(o,n,i);l[i]?l[i].p(a,s):(l[i]=Te(a),l[i].c(),l[i].m(e,null))}for(;i<l.length;i+=1)l[i].d(1);l.length=n.length}},d(o){o&&d(e),ee(l,o)}}}function Te(t){let e,n=t[24]+"",l,o,s,i;function a(){return t[11](t[24])}function r(){return t[12](t[24])}return{c(){e=C("div"),l=W(n),o=D(),this.h()},l(u){e=A(u,"DIV",{class:!0,style:!0});var f=L(e);l=X(f,n),o=R(f),f.forEach(d),this.h()},h(){_(e,"class","category-label svelte-1woixh4"),_(e,"style","background-color:"+t[25].secondary)},m(u,f){y(u,e,f),H(e,l),H(e,o),s||(i=[I(e,"mouseover",a),I(e,"focus",r),I(e,"mouseout",t[13]),I(e,"blur",t[14])],s=!0)},p(u,f){t=u},d(u){u&&d(e),s=!1,$(i)}}}function Ce(t){let e,n,l=t[21]+"",o,s,i,a,r=!t[1]&&t[2]&&t[18].class_or_confidence!==null&&Ae(t);function u(){return t[15](t[20],t[18])}return{c(){e=C("span"),n=C("span"),o=W(l),s=D(),r&&r.c(),this.h()},l(f){e=A(f,"SPAN",{class:!0});var g=L(e);n=A(g,"SPAN",{class:!0});var p=L(n);o=X(p,l),p.forEach(d),s=R(g),r&&r.l(g),g.forEach(d),this.h()},h(){_(n,"class","text svelte-1woixh4"),j(n,"no-label",t[18].class_or_confidence===null||!t[6][t[18].class_or_confidence]),_(e,"class","textspan svelte-1woixh4"),j(e,"no-cat",t[18].class_or_confidence===null||t[4]&&t[4]!==t[18].class_or_confidence),j(e,"hl",t[18].class_or_confidence!==null),j(e,"selectable",t[3]),U(e,"background-color",t[18].class_or_confidence===null||t[4]&&t[4]!==t[18].class_or_confidence?"":t[6][t[18].class_or_confidence].secondary)},m(f,g){y(f,e,g),H(e,n),H(n,o),H(e,s),r&&r.m(e,null),i||(a=I(e,"click",u),i=!0)},p(f,g){t=f,g&1&&l!==(l=t[21]+"")&&te(o,l),g&65&&j(n,"no-label",t[18].class_or_confidence===null||!t[6][t[18].class_or_confidence]),!t[1]&&t[2]&&t[18].class_or_confidence!==null?r?r.p(t,g):(r=Ae(t),r.c(),r.m(e,null)):r&&(r.d(1),r=null),g&17&&j(e,"no-cat",t[18].class_or_confidence===null||t[4]&&t[4]!==t[18].class_or_confidence),g&1&&j(e,"hl",t[18].class_or_confidence!==null),g&8&&j(e,"selectable",t[3]),g&17&&U(e,"background-color",t[18].class_or_confidence===null||t[4]&&t[4]!==t[18].class_or_confidence?"":t[6][t[18].class_or_confidence].secondary)},d(f){f&&d(e),r&&r.d(),i=!1,a()}}}function Ae(t){let e,n,l=t[18].class_or_confidence+"",o;return{c(){e=W(` 
								`),n=C("span"),o=W(l),this.h()},l(s){e=X(s,` 
								`),n=A(s,"SPAN",{class:!0});var i=L(n);o=X(i,l),i.forEach(d),this.h()},h(){_(n,"class","label svelte-1woixh4"),U(n,"background-color",t[18].class_or_confidence===null||t[4]&&t[4]!==t[18].class_or_confidence?"":t[6][t[18].class_or_confidence].primary)},m(s,i){y(s,e,i),y(s,n,i),H(n,o)},p(s,i){i&1&&l!==(l=s[18].class_or_confidence+"")&&te(o,l),i&17&&U(n,"background-color",s[18].class_or_confidence===null||s[4]&&s[4]!==s[18].class_or_confidence?"":s[6][s[18].class_or_confidence].primary)},d(s){s&&(d(e),d(n))}}}function Be(t){let e;return{c(){e=C("br")},l(n){e=A(n,"BR",{})},m(n,l){y(n,e,l)},d(n){n&&d(e)}}}function He(t){let e=t[21].trim()!=="",n,l=t[23]<fe(t[18].token).length-1,o,s=e&&Ce(t),i=l&&Be();return{c(){s&&s.c(),n=D(),i&&i.c(),o=z()},l(a){s&&s.l(a),n=R(a),i&&i.l(a),o=z()},m(a,r){s&&s.m(a,r),y(a,n,r),i&&i.m(a,r),y(a,o,r)},p(a,r){r&1&&(e=a[21].trim()!==""),e?s?s.p(a,r):(s=Ce(a),s.c(),s.m(n.parentNode,n)):s&&(s.d(1),s=null),r&1&&(l=a[23]<fe(a[18].token).length-1),l?i||(i=Be(),i.c(),i.m(o.parentNode,o)):i&&(i.d(1),i=null)},d(a){a&&(d(n),d(o)),s&&s.d(a),i&&i.d(a)}}}function Le(t){let e,n=F(fe(t[18].token)),l=[];for(let o=0;o<n.length;o+=1)l[o]=He(Ee(t,n,o));return{c(){for(let o=0;o<l.length;o+=1)l[o].c();e=z()},l(o){for(let s=0;s<l.length;s+=1)l[s].l(o);e=z()},m(o,s){for(let i=0;i<l.length;i+=1)l[i]&&l[i].m(o,s);y(o,e,s)},p(o,s){if(s&223){n=F(fe(o[18].token));let i;for(i=0;i<n.length;i+=1){const a=Ee(o,n,i);l[i]?l[i].p(a,s):(l[i]=He(a),l[i].c(),l[i].m(e.parentNode,e))}for(;i<l.length;i+=1)l[i].d(1);l.length=n.length}},d(o){o&&d(e),ee(l,o)}}}function Ul(t){let e;function n(s,i){return s[5]==="categories"?Fl:zl}let l=n(t),o=l(t);return{c(){e=C("div"),o.c(),this.h()},l(s){e=A(s,"DIV",{class:!0});var i=L(e);o.l(i),i.forEach(d),this.h()},h(){_(e,"class","container svelte-1woixh4")},m(s,i){y(s,e,i),o.m(e,null)},p(s,[i]){l===(l=n(s))&&o?o.p(s,i):(o.d(1),o=l(s),o&&(o.c(),o.m(e,null)))},i:le,o:le,d(s){s&&d(e),o.d()}}}function fe(t){return t.split(`
`)}function ql(t,e,n){const l=typeof document<"u";let{value:o=[]}=e,{show_legend:s=!1}=e,{show_inline_category:i=!0}=e,{color_map:a={}}=e,{selectable:r=!1}=e,u,f={},g="";const p=el();let v;function c(k){n(4,g=k)}function m(){n(4,g="")}const S=k=>c(k),P=k=>c(k),T=()=>m(),b=()=>m(),V=(k,B)=>{p("select",{index:k,value:[B.token,B.class_or_confidence]})};return t.$$set=k=>{"value"in k&&n(0,o=k.value),"show_legend"in k&&n(1,s=k.show_legend),"show_inline_category"in k&&n(2,i=k.show_inline_category),"color_map"in k&&n(10,a=k.color_map),"selectable"in k&&n(3,r=k.selectable)},t.$$.update=()=>{if(t.$$.dirty&1025){if(a||n(10,a={}),o.length>0){for(let k of o)if(k.class_or_confidence!==null)if(typeof k.class_or_confidence=="string"){if(n(5,v="categories"),!(k.class_or_confidence in a)){let B=sl(Object.keys(a).length);n(10,a[k.class_or_confidence]=B,a)}}else n(5,v="scores")}fl(a,f,l,u)}},[o,s,i,r,g,v,f,p,c,m,a,S,P,T,b,V]}class Zl extends oe{constructor(e){super(),ie(this,e,ql,Ul,ne,{value:0,show_legend:1,show_inline_category:2,color_map:10,selectable:3})}}const Jl=Zl;function Kl(t){let e,n,l,o;return{c(){e=C("input"),this.h()},l(s){e=A(s,"INPUT",{class:!0,type:!0,step:!0,style:!0}),this.h()},h(){_(e,"class","label-input svelte-df6jzs"),e.autofocus=!0,_(e,"type","number"),_(e,"step","0.1"),_(e,"style",n="background-color: rgba("+(typeof t[1]=="number"&&t[1]<0?"128, 90, 213,"+-t[1]:"239, 68, 60,"+t[1])+")"),e.value=t[1],U(e,"width","7ch")},m(s,i){y(s,e,i),e.focus(),l||(o=[I(e,"input",t[8]),I(e,"blur",t[14]),I(e,"keydown",t[15])],l=!0)},p(s,i){i&2&&n!==(n="background-color: rgba("+(typeof s[1]=="number"&&s[1]<0?"128, 90, 213,"+-s[1]:"239, 68, 60,"+s[1])+")")&&_(e,"style",n),i&2&&e.value!==s[1]&&(e.value=s[1]);const a=i&2;(i&2||a)&&U(e,"width","7ch")},d(s){s&&d(e),l=!1,$(o)}}}function Ql(t){let e,n,l,o;return{c(){e=C("input"),this.h()},l(s){e=A(s,"INPUT",{class:!0,id:!0,type:!0,placeholder:!0}),this.h()},h(){var s;_(e,"class","label-input svelte-df6jzs"),e.autofocus=!0,_(e,"id",n=`label-input-${t[3]}`),_(e,"type","text"),_(e,"placeholder","label"),e.value=t[1],U(e,"background-color",t[1]===null||t[2]&&t[2]!==t[1]?"":t[6][t[1]].primary),U(e,"width",t[7]?((s=t[7].toString())==null?void 0:s.length)+4+"ch":"8ch")},m(s,i){y(s,e,i),e.focus(),l||(o=[I(e,"input",t[8]),I(e,"blur",t[12]),I(e,"keydown",t[13]),I(e,"focus",Gl)],l=!0)},p(s,i){var a;i&8&&n!==(n=`label-input-${s[3]}`)&&_(e,"id",n),i&2&&e.value!==s[1]&&(e.value=s[1]),i&70&&U(e,"background-color",s[1]===null||s[2]&&s[2]!==s[1]?"":s[6][s[1]].primary),i&128&&U(e,"width",s[7]?((a=s[7].toString())==null?void 0:a.length)+4+"ch":"8ch")},d(s){s&&d(e),l=!1,$(o)}}}function Yl(t){let e;function n(s,i){return s[5]?Kl:Ql}let l=n(t),o=l(t);return{c(){o.c(),e=z()},l(s){o.l(s),e=z()},m(s,i){o.m(s,i),y(s,e,i)},p(s,[i]){l===(l=n(s))&&o?o.p(s,i):(o.d(1),o=l(s),o&&(o.c(),o.m(e.parentNode,e)))},i:le,o:le,d(s){s&&d(e),o.d(s)}}}function Gl(t){let e=t.target;e&&e.placeholder&&(e.placeholder="")}function Wl(t,e,n){let{value:l}=e,{category:o}=e,{active:s}=e,{labelToEdit:i}=e,{indexOfLabel:a}=e,{text:r}=e,{handleValueChange:u}=e,{isScoresMode:f=!1}=e,{_color_map:g}=e,p=o;function v(b){let V=b.target;V&&n(7,p=V.value)}function c(b,V,k){let B=b.target;n(10,l=[...l.slice(0,V),{token:k,class_or_confidence:B.value===""?null:f?Number(B.value):B.value},...l.slice(V+1)]),u()}const m=b=>c(b,a,r),S=b=>{b.key==="Enter"&&(c(b,a,r),n(0,i=-1))},P=b=>c(b,a,r),T=b=>{b.key==="Enter"&&(c(b,a,r),n(0,i=-1))};return t.$$set=b=>{"value"in b&&n(10,l=b.value),"category"in b&&n(1,o=b.category),"active"in b&&n(2,s=b.active),"labelToEdit"in b&&n(0,i=b.labelToEdit),"indexOfLabel"in b&&n(3,a=b.indexOfLabel),"text"in b&&n(4,r=b.text),"handleValueChange"in b&&n(11,u=b.handleValueChange),"isScoresMode"in b&&n(5,f=b.isScoresMode),"_color_map"in b&&n(6,g=b._color_map)},[i,o,s,a,r,f,g,p,v,c,l,u,m,S,P,T]}class cl extends oe{constructor(e){super(),ie(this,e,Wl,Yl,ne,{value:10,category:1,active:2,labelToEdit:0,indexOfLabel:3,text:4,handleValueChange:11,isScoresMode:5,_color_map:6})}}function Pe(t,e,n){const l=t.slice();l[45]=e[n].token,l[46]=e[n].class_or_confidence,l[48]=n;const o=typeof l[46]=="string"?parseInt(l[46]):l[46];return l[54]=o,l}function Me(t,e,n){const l=t.slice();return l[45]=e[n].token,l[46]=e[n].class_or_confidence,l[48]=n,l}function Oe(t,e,n){const l=t.slice();return l[49]=e[n],l[51]=n,l}function je(t,e,n){const l=t.slice();return l[46]=e[n][0],l[52]=e[n][1],l[48]=n,l}function Xl(t){let e,n,l,o=t[1]&&De(),s=F(t[0]),i=[];for(let r=0;r<s.length;r+=1)i[r]=Fe(Pe(t,s,r));const a=r=>N(i[r],1,1,()=>{i[r]=null});return{c(){o&&o.c(),e=D(),n=C("div");for(let r=0;r<i.length;r+=1)i[r].c();this.h()},l(r){o&&o.l(r),e=R(r),n=A(r,"DIV",{class:!0,"data-testid":!0});var u=L(n);for(let f=0;f<i.length;f+=1)i[f].l(u);u.forEach(d),this.h()},h(){_(n,"class","textfield svelte-u7mykt"),_(n,"data-testid","highlighted-text:textfield")},m(r,u){o&&o.m(r,u),y(r,e,u),y(r,n,u);for(let f=0;f<i.length;f+=1)i[f]&&i[f].m(n,null);l=!0},p(r,u){if(r[1]?o||(o=De(),o.c(),o.m(e.parentNode,e)):o&&(o.d(1),o=null),u[0]&889){s=F(r[0]);let f;for(f=0;f<s.length;f+=1){const g=Pe(r,s,f);i[f]?(i[f].p(g,u),w(i[f],1)):(i[f]=Fe(g),i[f].c(),w(i[f],1),i[f].m(n,null))}for(Q(),f=s.length;f<i.length;f+=1)a(f);Y()}},i(r){if(!l){for(let u=0;u<s.length;u+=1)w(i[u]);l=!0}},o(r){i=i.filter(Boolean);for(let u=0;u<i.length;u+=1)N(i[u]);l=!1},d(r){r&&(d(e),d(n)),o&&o.d(r),ee(i,r)}}}function $l(t){let e,n,l,o=t[1]&&Ue(t),s=F(t[0]),i=[];for(let r=0;r<s.length;r+=1)i[r]=Xe(Me(t,s,r));const a=r=>N(i[r],1,1,()=>{i[r]=null});return{c(){o&&o.c(),e=D(),n=C("div");for(let r=0;r<i.length;r+=1)i[r].c();this.h()},l(r){o&&o.l(r),e=R(r),n=A(r,"DIV",{class:!0});var u=L(n);for(let f=0;f<i.length;f+=1)i[f].l(u);u.forEach(d),this.h()},h(){_(n,"class","textfield svelte-u7mykt")},m(r,u){o&&o.m(r,u),y(r,e,u),y(r,n,u);for(let f=0;f<i.length;f+=1)i[f]&&i[f].m(n,null);l=!0},p(r,u){if(r[1]?o?o.p(r,u):(o=Ue(r),o.c(),o.m(e.parentNode,e)):o&&(o.d(1),o=null),u[0]&13183){s=F(r[0]);let f;for(f=0;f<s.length;f+=1){const g=Me(r,s,f);i[f]?(i[f].p(g,u),w(i[f],1)):(i[f]=Xe(g),i[f].c(),w(i[f],1),i[f].m(n,null))}for(Q(),f=s.length;f<i.length;f+=1)a(f);Y()}},i(r){if(!l){for(let u=0;u<s.length;u+=1)w(i[u]);l=!0}},o(r){i=i.filter(Boolean);for(let u=0;u<i.length;u+=1)N(i[u]);l=!1},d(r){r&&(d(e),d(n)),o&&o.d(r),ee(i,r)}}}function De(t){let e,n="<span>-1</span> <span>0</span> <span>+1</span>";return{c(){e=C("div"),e.innerHTML=n,this.h()},l(l){e=A(l,"DIV",{class:!0,"data-testid":!0,"data-svelte-h":!0}),ce(e)!=="svelte-mv3vmx"&&(e.innerHTML=n),this.h()},h(){_(e,"class","color-legend svelte-u7mykt"),_(e,"data-testid","highlighted-text:color-legend")},m(l,o){y(l,e,o)},d(l){l&&d(e)}}}function Re(t){let e,n,l;function o(i){t[32](i)}let s={labelToEdit:t[6],_color_map:t[3],category:t[46],active:t[5],indexOfLabel:t[48],text:t[45],handleValueChange:t[9],isScoresMode:!0};return t[0]!==void 0&&(s.value=t[0]),e=new cl({props:s}),ge.push(()=>ke(e,"value",o)),{c(){q(e.$$.fragment)},l(i){Z(e.$$.fragment,i)},m(i,a){J(e,i,a),l=!0},p(i,a){const r={};a[0]&64&&(r.labelToEdit=i[6]),a[0]&8&&(r._color_map=i[3]),a[0]&1&&(r.category=i[46]),a[0]&32&&(r.active=i[5]),a[0]&1&&(r.text=i[45]),!n&&a[0]&1&&(n=!0,r.value=i[0],be(()=>n=!1)),e.$set(r)},i(i){l||(w(e.$$.fragment,i),l=!0)},o(i){N(e.$$.fragment,i),l=!1},d(i){K(e,i)}}}function ze(t){let e,n="×",l,o;function s(){return t[37](t[48])}function i(...a){return t[38](t[48],...a)}return{c(){e=C("span"),e.textContent=n,this.h()},l(a){e=A(a,"SPAN",{class:!0,role:!0,"aria-roledescription":!0,tabindex:!0,"data-svelte-h":!0}),ce(e)!=="svelte-hxhs1z"&&(e.textContent=n),this.h()},h(){_(e,"class","label-clear-button svelte-u7mykt"),_(e,"role","button"),_(e,"aria-roledescription","Remove label from text"),_(e,"tabindex","0")},m(a,r){y(a,e,r),l||(o=[I(e,"click",s),I(e,"keydown",i)],l=!0)},p(a,r){t=a},d(a){a&&d(e),l=!1,$(o)}}}function Fe(t){let e,n,l,o=t[45]+"",s,i,a,r,u,f,g,p,v=t[46]&&t[6]===t[48]&&Re(t);function c(){return t[33](t[48])}function m(){return t[34](t[48])}function S(){return t[35](t[48])}function P(...b){return t[36](t[48],...b)}let T=t[46]&&t[4]===t[48]&&ze(t);return{c(){e=C("span"),n=C("span"),l=C("span"),s=W(o),i=D(),v&&v.c(),r=D(),T&&T.c(),u=D(),this.h()},l(b){e=A(b,"SPAN",{class:!0});var V=L(e);n=A(V,"SPAN",{class:!0,role:!0,tabindex:!0,style:!0});var k=L(n);l=A(k,"SPAN",{class:!0});var B=L(l);s=X(B,o),B.forEach(d),i=R(k),v&&v.l(k),k.forEach(d),r=R(V),T&&T.l(V),u=R(V),V.forEach(d),this.h()},h(){_(l,"class","text svelte-u7mykt"),_(n,"class","textspan score-text svelte-u7mykt"),_(n,"role","button"),_(n,"tabindex","0"),_(n,"style",a="background-color: rgba("+(t[54]&&t[54]<0?"128, 90, 213,"+-t[54]:"239, 68, 60,"+t[54])+")"),j(n,"no-cat",t[46]===null||t[5]&&t[5]!==t[46]),j(n,"hl",t[46]!==null),_(e,"class","score-text-container svelte-u7mykt")},m(b,V){y(b,e,V),H(e,n),H(n,l),H(l,s),H(n,i),v&&v.m(n,null),H(e,r),T&&T.m(e,null),H(e,u),f=!0,g||(p=[I(n,"mouseover",c),I(n,"focus",m),I(n,"click",S),I(n,"keydown",P)],g=!0)},p(b,V){t=b,(!f||V[0]&1)&&o!==(o=t[45]+"")&&te(s,o),t[46]&&t[6]===t[48]?v?(v.p(t,V),V[0]&65&&w(v,1)):(v=Re(t),v.c(),w(v,1),v.m(n,null)):v&&(Q(),N(v,1,1,()=>{v=null}),Y()),(!f||V[0]&1&&a!==(a="background-color: rgba("+(t[54]&&t[54]<0?"128, 90, 213,"+-t[54]:"239, 68, 60,"+t[54])+")"))&&_(n,"style",a),(!f||V[0]&33)&&j(n,"no-cat",t[46]===null||t[5]&&t[5]!==t[46]),(!f||V[0]&1)&&j(n,"hl",t[46]!==null),t[46]&&t[4]===t[48]?T?T.p(t,V):(T=ze(t),T.c(),T.m(e,u)):T&&(T.d(1),T=null)},i(b){f||(w(v),f=!0)},o(b){N(v),f=!1},d(b){b&&d(e),v&&v.d(),T&&T.d(),g=!1,$(p)}}}function Ue(t){let e,n=t[3]&&qe(t);return{c(){e=C("div"),n&&n.c(),this.h()},l(l){e=A(l,"DIV",{class:!0,"data-testid":!0});var o=L(e);n&&n.l(o),o.forEach(d),this.h()},h(){_(e,"class","class_or_confidence-legend svelte-u7mykt"),_(e,"data-testid","highlighted-text:class_or_confidence-legend")},m(l,o){y(l,e,o),n&&n.m(e,null)},p(l,o){l[3]?n?n.p(l,o):(n=qe(l),n.c(),n.m(e,null)):n&&(n.d(1),n=null)},d(l){l&&d(e),n&&n.d()}}}function qe(t){let e,n=F(Object.entries(t[3])),l=[];for(let o=0;o<n.length;o+=1)l[o]=Ze(je(t,n,o));return{c(){for(let o=0;o<l.length;o+=1)l[o].c();e=z()},l(o){for(let s=0;s<l.length;s+=1)l[s].l(o);e=z()},m(o,s){for(let i=0;i<l.length;i+=1)l[i]&&l[i].m(o,s);y(o,e,s)},p(o,s){if(s[0]&3080){n=F(Object.entries(o[3]));let i;for(i=0;i<n.length;i+=1){const a=je(o,n,i);l[i]?l[i].p(a,s):(l[i]=Ze(a),l[i].c(),l[i].m(e.parentNode,e))}for(;i<l.length;i+=1)l[i].d(1);l.length=n.length}},d(o){o&&d(e),ee(l,o)}}}function Ze(t){let e,n=t[46]+"",l,o,s,i,a;function r(){return t[15](t[46])}function u(){return t[16](t[46])}return{c(){e=C("div"),l=W(n),o=D(),this.h()},l(f){e=A(f,"DIV",{role:!0,"aria-roledescription":!0,tabindex:!0,class:!0,style:!0});var g=L(e);l=X(g,n),o=R(g),g.forEach(d),this.h()},h(){_(e,"role","button"),_(e,"aria-roledescription","Categories of highlighted text. Hover to see text with this class_or_confidence highlighted."),_(e,"tabindex","0"),_(e,"class","class_or_confidence-label svelte-u7mykt"),_(e,"style",s="background-color:"+t[52].secondary)},m(f,g){y(f,e,g),H(e,l),H(e,o),i||(a=[I(e,"mouseover",r),I(e,"focus",u),I(e,"mouseout",t[17]),I(e,"blur",t[18])],i=!0)},p(f,g){t=f,g[0]&8&&n!==(n=t[46]+"")&&te(l,n),g[0]&8&&s!==(s="background-color:"+t[52].secondary)&&_(e,"style",s)},d(f){f&&d(e),i=!1,$(a)}}}function Je(t){let e,n,l,o=t[49]+"",s,i,a,r,u,f,g;function p(){return t[20](t[48])}function v(){return t[21](t[48])}function c(){return t[22](t[48])}let m=!t[1]&&t[46]!==null&&t[6]!==t[48]&&Ke(t),S=t[6]===t[48]&&t[46]!==null&&Qe(t);function P(){return t[26](t[46],t[48],t[45])}function T(...B){return t[27](t[46],t[48],t[45],...B)}function b(){return t[28](t[48])}function V(){return t[29](t[48])}let k=t[46]!==null&&Ye(t);return{c(){e=C("span"),n=C("span"),l=C("span"),s=W(o),i=D(),m&&m.c(),a=D(),S&&S.c(),r=D(),k&&k.c(),this.h()},l(B){e=A(B,"SPAN",{class:!0});var M=L(e);n=A(M,"SPAN",{role:!0,tabindex:!0,class:!0});var G=L(n);l=A(G,"SPAN",{class:!0,role:!0,tabindex:!0});var E=L(l);s=X(E,o),E.forEach(d),i=R(G),m&&m.l(G),a=R(G),S&&S.l(G),G.forEach(d),r=R(M),k&&k.l(M),M.forEach(d),this.h()},h(){_(l,"class","text svelte-u7mykt"),_(l,"role","button"),_(l,"tabindex","0"),j(l,"no-label",t[46]===null),_(n,"role","button"),_(n,"tabindex","0"),_(n,"class","textspan svelte-u7mykt"),j(n,"no-cat",t[46]===null||t[5]&&t[5]!==t[46]),j(n,"hl",t[46]!==null),j(n,"selectable",t[2]),U(n,"background-color",t[46]===null||t[5]&&t[5]!==t[46]?"":t[46]&&t[3][t[46]]?t[3][t[46]].secondary:""),_(e,"class","text-class_or_confidence-container svelte-u7mykt")},m(B,M){y(B,e,M),H(e,n),H(n,l),H(l,s),H(n,i),m&&m.m(n,null),H(n,a),S&&S.m(n,null),H(e,r),k&&k.m(e,null),u=!0,f||(g=[I(l,"keydown",t[19]),I(l,"focus",p),I(l,"mouseover",v),I(l,"click",c),I(n,"click",P),I(n,"keydown",T),I(n,"focus",b),I(n,"mouseover",V)],f=!0)},p(B,M){t=B,(!u||M[0]&1)&&o!==(o=t[49]+"")&&te(s,o),(!u||M[0]&1)&&j(l,"no-label",t[46]===null),!t[1]&&t[46]!==null&&t[6]!==t[48]?m?m.p(t,M):(m=Ke(t),m.c(),m.m(n,a)):m&&(m.d(1),m=null),t[6]===t[48]&&t[46]!==null?S?(S.p(t,M),M[0]&65&&w(S,1)):(S=Qe(t),S.c(),w(S,1),S.m(n,null)):S&&(Q(),N(S,1,1,()=>{S=null}),Y()),(!u||M[0]&33)&&j(n,"no-cat",t[46]===null||t[5]&&t[5]!==t[46]),(!u||M[0]&1)&&j(n,"hl",t[46]!==null),(!u||M[0]&4)&&j(n,"selectable",t[2]),M[0]&41&&U(n,"background-color",t[46]===null||t[5]&&t[5]!==t[46]?"":t[46]&&t[3][t[46]]?t[3][t[46]].secondary:""),t[46]!==null?k?k.p(t,M):(k=Ye(t),k.c(),k.m(e,null)):k&&(k.d(1),k=null)},i(B){u||(w(S),u=!0)},o(B){N(S),u=!1},d(B){B&&d(e),m&&m.d(),S&&S.d(),k&&k.d(),f=!1,$(g)}}}function Ke(t){let e,n=t[46]+"",l,o,s;function i(){return t[23](t[48])}function a(){return t[24](t[48])}return{c(){e=C("span"),l=W(n),this.h()},l(r){e=A(r,"SPAN",{id:!0,class:!0,role:!0,tabindex:!0});var u=L(e);l=X(u,n),u.forEach(d),this.h()},h(){_(e,"id",`label-tag-${t[48]}`),_(e,"class","label svelte-u7mykt"),_(e,"role","button"),_(e,"tabindex","0"),U(e,"background-color",t[46]===null||t[5]&&t[5]!==t[46]?"":t[3][t[46]].primary)},m(r,u){y(r,e,u),H(e,l),o||(s=[I(e,"click",i),I(e,"keydown",a)],o=!0)},p(r,u){t=r,u[0]&1&&n!==(n=t[46]+"")&&te(l,n),u[0]&41&&U(e,"background-color",t[46]===null||t[5]&&t[5]!==t[46]?"":t[3][t[46]].primary)},d(r){r&&d(e),o=!1,$(s)}}}function Qe(t){let e,n,l,o;function s(a){t[25](a)}let i={labelToEdit:t[6],category:t[46],active:t[5],_color_map:t[3],indexOfLabel:t[48],text:t[45],handleValueChange:t[9]};return t[0]!==void 0&&(i.value=t[0]),n=new cl({props:i}),ge.push(()=>ke(n,"value",s)),{c(){e=W(` 
									`),q(n.$$.fragment)},l(a){e=X(a,` 
									`),Z(n.$$.fragment,a)},m(a,r){y(a,e,r),J(n,a,r),o=!0},p(a,r){const u={};r[0]&64&&(u.labelToEdit=a[6]),r[0]&1&&(u.category=a[46]),r[0]&32&&(u.active=a[5]),r[0]&8&&(u._color_map=a[3]),r[0]&1&&(u.text=a[45]),!l&&r[0]&1&&(l=!0,u.value=a[0],be(()=>l=!1)),n.$set(u)},i(a){o||(w(n.$$.fragment,a),o=!0)},o(a){N(n.$$.fragment,a),o=!1},d(a){a&&d(e),K(n,a)}}}function Ye(t){let e,n="×",l,o;function s(){return t[30](t[48])}function i(...a){return t[31](t[48],...a)}return{c(){e=C("span"),e.textContent=n,this.h()},l(a){e=A(a,"SPAN",{class:!0,role:!0,"aria-roledescription":!0,tabindex:!0,"data-svelte-h":!0}),ce(e)!=="svelte-1fuy4vv"&&(e.textContent=n),this.h()},h(){_(e,"class","label-clear-button svelte-u7mykt"),_(e,"role","button"),_(e,"aria-roledescription","Remove label from text"),_(e,"tabindex","0")},m(a,r){y(a,e,r),l||(o=[I(e,"click",s),I(e,"keydown",i)],l=!0)},p(a,r){t=a},d(a){a&&d(e),l=!1,$(o)}}}function Ge(t){let e;return{c(){e=C("br")},l(n){e=A(n,"BR",{})},m(n,l){y(n,e,l)},d(n){n&&d(e)}}}function We(t){let e=t[49].trim()!=="",n,l=t[51]<ue(t[45]).length-1,o,s,i=e&&Je(t),a=l&&Ge();return{c(){i&&i.c(),n=D(),a&&a.c(),o=z()},l(r){i&&i.l(r),n=R(r),a&&a.l(r),o=z()},m(r,u){i&&i.m(r,u),y(r,n,u),a&&a.m(r,u),y(r,o,u),s=!0},p(r,u){u[0]&1&&(e=r[49].trim()!==""),e?i?(i.p(r,u),u[0]&1&&w(i,1)):(i=Je(r),i.c(),w(i,1),i.m(n.parentNode,n)):i&&(Q(),N(i,1,1,()=>{i=null}),Y()),u[0]&1&&(l=r[51]<ue(r[45]).length-1),l?a||(a=Ge(),a.c(),a.m(o.parentNode,o)):a&&(a.d(1),a=null)},i(r){s||(w(i),s=!0)},o(r){N(i),s=!1},d(r){r&&(d(n),d(o)),i&&i.d(r),a&&a.d(r)}}}function Xe(t){let e,n,l=F(ue(t[45])),o=[];for(let i=0;i<l.length;i+=1)o[i]=We(Oe(t,l,i));const s=i=>N(o[i],1,1,()=>{o[i]=null});return{c(){for(let i=0;i<o.length;i+=1)o[i].c();e=z()},l(i){for(let a=0;a<o.length;a+=1)o[a].l(i);e=z()},m(i,a){for(let r=0;r<o.length;r+=1)o[r]&&o[r].m(i,a);y(i,e,a),n=!0},p(i,a){if(a[0]&13183){l=F(ue(i[45]));let r;for(r=0;r<l.length;r+=1){const u=Oe(i,l,r);o[r]?(o[r].p(u,a),w(o[r],1)):(o[r]=We(u),o[r].c(),w(o[r],1),o[r].m(e.parentNode,e))}for(Q(),r=l.length;r<o.length;r+=1)s(r);Y()}},i(i){if(!n){for(let a=0;a<l.length;a+=1)w(o[a]);n=!0}},o(i){o=o.filter(Boolean);for(let a=0;a<o.length;a+=1)N(o[a]);n=!1},d(i){i&&d(e),ee(o,i)}}}function xl(t){let e,n,l,o;const s=[$l,Xl],i=[];function a(r,u){return r[7]==="categories"?0:1}return n=a(t),l=i[n]=s[n](t),{c(){e=C("div"),l.c(),this.h()},l(r){e=A(r,"DIV",{class:!0});var u=L(e);l.l(u),u.forEach(d),this.h()},h(){_(e,"class","container svelte-u7mykt")},m(r,u){y(r,e,u),i[n].m(e,null),o=!0},p(r,u){let f=n;n=a(r),n===f?i[n].p(r,u):(Q(),N(i[f],1,1,()=>{i[f]=null}),Y(),l=i[n],l?l.p(r,u):(l=i[n]=s[n](r),l.c()),w(l,1),l.m(e,null))},i(r){o||(w(l),o=!0)},o(r){N(l),o=!1},d(r){r&&d(e),i[n].d()}}}function ue(t){return t.split(`
`)}function et(t,e,n){const l=typeof document<"u";let{value:o=[]}=e,{show_legend:s=!1}=e,{color_map:i={}}=e,{selectable:a=!1}=e,r=-1,u,f={},g="",p,v=-1;Dl(()=>{const h=()=>{p=window.getSelection(),B(),window.removeEventListener("mouseup",h)};window.addEventListener("mousedown",()=>{window.addEventListener("mouseup",h)})});async function c(h,O){var x;if(p!=null&&p.toString()&&r!==-1&&o[r].token.toString().includes(p.toString())){const se=Symbol(),he=o[r].token,[Pl,Ml,Ol]=[he.substring(0,h),he.substring(h,O),he.substring(O)];let re=[...o.slice(0,r),{token:Pl,class_or_confidence:null},{token:Ml,class_or_confidence:T==="scores"?1:"label",flag:se},{token:Ol,class_or_confidence:null},...o.slice(r+1)];n(6,v=re.findIndex(({flag:ae})=>ae===se)),re=re.filter(ae=>ae.token.trim()!==""),n(0,o=re.map(({flag:ae,...jl})=>jl)),P(),(x=document.getElementById(`label-input-${v}`))==null||x.focus()}}const m=el();function S(h){var O;!o||h<0||h>=o.length||(n(0,o[h].class_or_confidence=null,o),n(0,o=ul(o)),P(),(O=window.getSelection())==null||O.empty())}function P(){m("change",o),n(6,v=-1),s&&(n(14,i={}),n(3,f={}))}let T;function b(h){n(5,g=h)}function V(){n(5,g="")}async function k(h){p=window.getSelection(),h.key==="Enter"&&B()}function B(){if(p&&(p==null?void 0:p.toString().trim())!==""){const h=p.getRangeAt(0).startOffset,O=p.getRangeAt(0).endOffset;c(h,O)}}function M(h,O,x){m("select",{index:h,value:[O,x]})}const G=h=>b(h),E=h=>b(h),_l=()=>V(),hl=()=>V(),dl=h=>k(h),ml=h=>n(4,r=h),gl=h=>n(4,r=h),bl=h=>n(6,v=h),kl=h=>n(6,v=h),vl=h=>n(6,v=h);function pl(h){o=h,n(0,o)}const wl=(h,O,x)=>{h!==null&&M(O,x,h)},yl=(h,O,x,se)=>{h!==null?(n(6,v=O),M(O,x,h)):k(se)},El=h=>n(4,r=h),Sl=h=>n(4,r=h),Nl=h=>S(h),Il=(h,O)=>{O.key==="Enter"&&S(h)};function Vl(h){o=h,n(0,o)}const Tl=h=>n(4,r=h),Cl=h=>n(4,r=h),Al=h=>n(6,v=h),Bl=(h,O)=>{O.key==="Enter"&&n(6,v=h)},Hl=h=>S(h),Ll=(h,O)=>{O.key==="Enter"&&S(h)};return t.$$set=h=>{"value"in h&&n(0,o=h.value),"show_legend"in h&&n(1,s=h.show_legend),"color_map"in h&&n(14,i=h.color_map),"selectable"in h&&n(2,a=h.selectable)},t.$$.update=()=>{if(t.$$.dirty[0]&16393){if(i||n(14,i={}),o.length>0){for(let h of o)if(h.class_or_confidence!==null)if(typeof h.class_or_confidence=="string"){if(n(7,T="categories"),!(h.class_or_confidence in i)){let O=sl(Object.keys(i).length);n(14,i[h.class_or_confidence]=O,i)}}else n(7,T="scores")}fl(i,f,l,u)}},[o,s,a,f,r,g,v,T,S,P,b,V,k,M,i,G,E,_l,hl,dl,ml,gl,bl,kl,vl,pl,wl,yl,El,Sl,Nl,Il,Vl,Tl,Cl,Al,Bl,Hl,Ll]}class lt extends oe{constructor(e){super(),ie(this,e,et,xl,ne,{value:0,show_legend:1,color_map:14,selectable:2},null,[-1,-1])}}const tt=lt;function nt(t){let e,n;return e=new tl({props:{variant:t[13]?"dashed":"solid",test_id:"highlighted-text",visible:t[5],elem_id:t[3],elem_classes:t[4],padding:!1,container:t[9],scale:t[10],min_width:t[11],$$slots:{default:[at]},$$scope:{ctx:t}}}),{c(){q(e.$$.fragment)},l(l){Z(e.$$.fragment,l)},m(l,o){J(e,l,o),n=!0},p(l,o){const s={};o&8192&&(s.variant=l[13]?"dashed":"solid"),o&32&&(s.visible=l[5]),o&8&&(s.elem_id=l[3]),o&16&&(s.elem_classes=l[4]),o&512&&(s.container=l[9]),o&1024&&(s.scale=l[10]),o&2048&&(s.min_width=l[11]),o&4215623&&(s.$$scope={dirty:o,ctx:l}),e.$set(s)},i(l){n||(w(e.$$.fragment,l),n=!0)},o(l){N(e.$$.fragment,l),n=!1},d(l){K(e,l)}}}function ot(t){let e,n;return e=new tl({props:{variant:"solid",test_id:"highlighted-text",visible:t[5],elem_id:t[3],elem_classes:t[4],padding:!1,container:t[9],scale:t[10],min_width:t[11],$$slots:{default:[_t]},$$scope:{ctx:t}}}),{c(){q(e.$$.fragment)},l(l){Z(e.$$.fragment,l)},m(l,o){J(e,l,o),n=!0},p(l,o){const s={};o&32&&(s.visible=l[5]),o&8&&(s.elem_id=l[3]),o&16&&(s.elem_classes=l[4]),o&512&&(s.container=l[9]),o&1024&&(s.scale=l[10]),o&2048&&(s.min_width=l[11]),o&4215751&&(s.$$scope={dirty:o,ctx:l}),e.$set(s)},i(l){n||(w(e.$$.fragment,l),n=!0)},o(l){N(e.$$.fragment,l),n=!1},d(l){K(e,l)}}}function $e(t){let e,n;return e=new rl({props:{Icon:_e,label:t[8],float:!1,disable:t[9]===!1}}),{c(){q(e.$$.fragment)},l(l){Z(e.$$.fragment,l)},m(l,o){J(e,l,o),n=!0},p(l,o){const s={};o&256&&(s.label=l[8]),o&512&&(s.disable=l[9]===!1),e.$set(s)},i(l){n||(w(e.$$.fragment,l),n=!0)},o(l){N(e.$$.fragment,l),n=!1},d(l){K(e,l)}}}function it(t){let e,n;return e=new al({props:{$$slots:{default:[rt]},$$scope:{ctx:t}}}),{c(){q(e.$$.fragment)},l(l){Z(e.$$.fragment,l)},m(l,o){J(e,l,o),n=!0},p(l,o){const s={};o&4194304&&(s.$$scope={dirty:o,ctx:l}),e.$set(s)},i(l){n||(w(e.$$.fragment,l),n=!0)},o(l){N(e.$$.fragment,l),n=!1},d(l){K(e,l)}}}function st(t){let e,n,l;function o(i){t[20](i)}let s={selectable:t[12],show_legend:t[6],color_map:t[1]};return t[0]!==void 0&&(s.value=t[0]),e=new tt({props:s}),ge.push(()=>ke(e,"value",o)),e.$on("change",t[21]),{c(){q(e.$$.fragment)},l(i){Z(e.$$.fragment,i)},m(i,a){J(e,i,a),l=!0},p(i,a){const r={};a&4096&&(r.selectable=i[12]),a&64&&(r.show_legend=i[6]),a&2&&(r.color_map=i[1]),!n&&a&1&&(n=!0,r.value=i[0],be(()=>n=!1)),e.$set(r)},i(i){l||(w(e.$$.fragment,i),l=!0)},o(i){N(e.$$.fragment,i),l=!1},d(i){K(e,i)}}}function rt(t){let e,n;return e=new _e({}),{c(){q(e.$$.fragment)},l(l){Z(e.$$.fragment,l)},m(l,o){J(e,l,o),n=!0},i(l){n||(w(e.$$.fragment,l),n=!0)},o(l){N(e.$$.fragment,l),n=!1},d(l){K(e,l)}}}function at(t){let e,n,l,o,s,i,a;const r=[{autoscroll:t[2].autoscroll},t[14],{i18n:t[2].i18n}];let u={};for(let c=0;c<r.length;c+=1)u=ll(u,r[c]);e=new nl({props:u}),e.$on("clear_status",t[19]);let f=t[8]&&$e(t);const g=[st,it],p=[];function v(c,m){return c[0]?0:1}return o=v(t),s=p[o]=g[o](t),{c(){q(e.$$.fragment),n=D(),f&&f.c(),l=D(),s.c(),i=z()},l(c){Z(e.$$.fragment,c),n=R(c),f&&f.l(c),l=R(c),s.l(c),i=z()},m(c,m){J(e,c,m),y(c,n,m),f&&f.m(c,m),y(c,l,m),p[o].m(c,m),y(c,i,m),a=!0},p(c,m){const S=m&16388?ol(r,[m&4&&{autoscroll:c[2].autoscroll},m&16384&&il(c[14]),m&4&&{i18n:c[2].i18n}]):{};e.$set(S),c[8]?f?(f.p(c,m),m&256&&w(f,1)):(f=$e(c),f.c(),w(f,1),f.m(l.parentNode,l)):f&&(Q(),N(f,1,1,()=>{f=null}),Y());let P=o;o=v(c),o===P?p[o].p(c,m):(Q(),N(p[P],1,1,()=>{p[P]=null}),Y(),s=p[o],s?s.p(c,m):(s=p[o]=g[o](c),s.c()),w(s,1),s.m(i.parentNode,i))},i(c){a||(w(e.$$.fragment,c),w(f),w(s),a=!0)},o(c){N(e.$$.fragment,c),N(f),N(s),a=!1},d(c){c&&(d(n),d(l),d(i)),K(e,c),f&&f.d(c),p[o].d(c)}}}function xe(t){let e,n;return e=new rl({props:{Icon:_e,label:t[8],float:!1,disable:t[9]===!1}}),{c(){q(e.$$.fragment)},l(l){Z(e.$$.fragment,l)},m(l,o){J(e,l,o),n=!0},p(l,o){const s={};o&256&&(s.label=l[8]),o&512&&(s.disable=l[9]===!1),e.$set(s)},i(l){n||(w(e.$$.fragment,l),n=!0)},o(l){N(e.$$.fragment,l),n=!1},d(l){K(e,l)}}}function ft(t){let e,n;return e=new al({props:{$$slots:{default:[ct]},$$scope:{ctx:t}}}),{c(){q(e.$$.fragment)},l(l){Z(e.$$.fragment,l)},m(l,o){J(e,l,o),n=!0},p(l,o){const s={};o&4194304&&(s.$$scope={dirty:o,ctx:l}),e.$set(s)},i(l){n||(w(e.$$.fragment,l),n=!0)},o(l){N(e.$$.fragment,l),n=!1},d(l){K(e,l)}}}function ut(t){let e,n;return e=new Jl({props:{selectable:t[12],value:t[0],show_legend:t[6],show_inline_category:t[7],color_map:t[1]}}),e.$on("select",t[18]),{c(){q(e.$$.fragment)},l(l){Z(e.$$.fragment,l)},m(l,o){J(e,l,o),n=!0},p(l,o){const s={};o&4096&&(s.selectable=l[12]),o&1&&(s.value=l[0]),o&64&&(s.show_legend=l[6]),o&128&&(s.show_inline_category=l[7]),o&2&&(s.color_map=l[1]),e.$set(s)},i(l){n||(w(e.$$.fragment,l),n=!0)},o(l){N(e.$$.fragment,l),n=!1},d(l){K(e,l)}}}function ct(t){let e,n;return e=new _e({}),{c(){q(e.$$.fragment)},l(l){Z(e.$$.fragment,l)},m(l,o){J(e,l,o),n=!0},i(l){n||(w(e.$$.fragment,l),n=!0)},o(l){N(e.$$.fragment,l),n=!1},d(l){K(e,l)}}}function _t(t){let e,n,l,o,s,i,a;const r=[{autoscroll:t[2].autoscroll},{i18n:t[2].i18n},t[14]];let u={};for(let c=0;c<r.length;c+=1)u=ll(u,r[c]);e=new nl({props:u}),e.$on("clear_status",t[17]);let f=t[8]&&xe(t);const g=[ut,ft],p=[];function v(c,m){return c[0]?0:1}return o=v(t),s=p[o]=g[o](t),{c(){q(e.$$.fragment),n=D(),f&&f.c(),l=D(),s.c(),i=z()},l(c){Z(e.$$.fragment,c),n=R(c),f&&f.l(c),l=R(c),s.l(c),i=z()},m(c,m){J(e,c,m),y(c,n,m),f&&f.m(c,m),y(c,l,m),p[o].m(c,m),y(c,i,m),a=!0},p(c,m){const S=m&16388?ol(r,[m&4&&{autoscroll:c[2].autoscroll},m&4&&{i18n:c[2].i18n},m&16384&&il(c[14])]):{};e.$set(S),c[8]?f?(f.p(c,m),m&256&&w(f,1)):(f=xe(c),f.c(),w(f,1),f.m(l.parentNode,l)):f&&(Q(),N(f,1,1,()=>{f=null}),Y());let P=o;o=v(c),o===P?p[o].p(c,m):(Q(),N(p[P],1,1,()=>{p[P]=null}),Y(),s=p[o],s?s.p(c,m):(s=p[o]=g[o](c),s.c()),w(s,1),s.m(i.parentNode,i))},i(c){a||(w(e.$$.fragment,c),w(f),w(s),a=!0)},o(c){N(e.$$.fragment,c),N(f),N(s),a=!1},d(c){c&&(d(n),d(l),d(i)),K(e,c),f&&f.d(c),p[o].d(c)}}}function ht(t){let e,n,l,o;const s=[ot,nt],i=[];function a(r,u){return r[13]?1:0}return e=a(t),n=i[e]=s[e](t),{c(){n.c(),l=z()},l(r){n.l(r),l=z()},m(r,u){i[e].m(r,u),y(r,l,u),o=!0},p(r,[u]){let f=e;e=a(r),e===f?i[e].p(r,u):(Q(),N(i[f],1,1,()=>{i[f]=null}),Y(),n=i[e],n?n.p(r,u):(n=i[e]=s[e](r),n.c()),w(n,1),n.m(l.parentNode,l))},i(r){o||(w(n),o=!0)},o(r){N(n),o=!1},d(r){r&&d(l),i[e].d(r)}}}function dt(t,e,n){let{gradio:l}=e,{elem_id:o=""}=e,{elem_classes:s=[]}=e,{visible:i=!0}=e,{value:a}=e,r,{show_legend:u}=e,{show_inline_category:f}=e,{color_map:g={}}=e,{label:p=l.i18n("highlighted_text.highlighted_text")}=e,{container:v=!0}=e,{scale:c=null}=e,{min_width:m=void 0}=e,{_selectable:S=!1}=e,{combine_adjacent:P=!1}=e,{interactive:T}=e,{loading_status:b}=e;const V=()=>l.dispatch("clear_status",b),k=({detail:E})=>l.dispatch("select",E),B=()=>l.dispatch("clear_status",b);function M(E){a=E,n(0,a),n(15,P)}const G=()=>l.dispatch("change");return t.$$set=E=>{"gradio"in E&&n(2,l=E.gradio),"elem_id"in E&&n(3,o=E.elem_id),"elem_classes"in E&&n(4,s=E.elem_classes),"visible"in E&&n(5,i=E.visible),"value"in E&&n(0,a=E.value),"show_legend"in E&&n(6,u=E.show_legend),"show_inline_category"in E&&n(7,f=E.show_inline_category),"color_map"in E&&n(1,g=E.color_map),"label"in E&&n(8,p=E.label),"container"in E&&n(9,v=E.container),"scale"in E&&n(10,c=E.scale),"min_width"in E&&n(11,m=E.min_width),"_selectable"in E&&n(12,S=E._selectable),"combine_adjacent"in E&&n(15,P=E.combine_adjacent),"interactive"in E&&n(13,T=E.interactive),"loading_status"in E&&n(14,b=E.loading_status)},t.$$.update=()=>{t.$$.dirty&2&&!g&&Object.keys(g).length&&n(1,g),t.$$.dirty&32769&&a&&P&&n(0,a=ul(a)),t.$$.dirty&65541&&a!==r&&(n(16,r=a),l.dispatch("change"))},[a,g,l,o,s,i,u,f,p,v,c,m,S,T,b,P,r,V,k,B,M,G]}class wt extends oe{constructor(e){super(),ie(this,e,dt,ht,ne,{gradio:2,elem_id:3,elem_classes:4,visible:5,value:0,show_legend:6,show_inline_category:7,color_map:1,label:8,container:9,scale:10,min_width:11,_selectable:12,combine_adjacent:15,interactive:13,loading_status:14})}}export{tt as BaseInteractiveHighlightedText,Jl as BaseStaticHighlightedText,wt as default};
